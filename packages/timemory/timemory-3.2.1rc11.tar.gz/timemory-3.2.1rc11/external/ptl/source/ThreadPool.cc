//
// MIT License
// Copyright (c) 2020 Jonathan R. Madsen
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED
// "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
// LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
// ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//
// ---------------------------------------------------------------
//  Tasking class implementation
//
// Class Description:
//
// This file creates a class for an efficient thread-pool that
// accepts work in the form of tasks.
//
// ---------------------------------------------------------------
// Author: Jonathan Madsen (Feb 13th 2018)
// ---------------------------------------------------------------

#include "PTL/ThreadPool.hh"
#include "PTL/Globals.hh"
#include "PTL/ThreadData.hh"
#include "PTL/UserTaskQueue.hh"
#include "PTL/VUserTaskQueue.hh"

#include <cstdlib>

using namespace PTL;

//======================================================================================//

inline intmax_t
ncores()
{
    return static_cast<intmax_t>(Thread::hardware_concurrency());
}

//======================================================================================//

ThreadPool::thread_id_map_t ThreadPool::f_thread_ids;

//======================================================================================//

namespace
{
ThreadData*&
thread_data()
{
    return ThreadData::GetInstance();
}
}  // namespace

//======================================================================================//

bool ThreadPool::f_use_tbb = false;

//======================================================================================//
// static member function that calls the member function we want the thread to
// run
void
ThreadPool::start_thread(ThreadPool* tp, thread_data_t* _data, intmax_t _idx)
{
    auto _thr_data = std::make_shared<ThreadData>(tp);
    {
        AutoLock lock(TypeMutex<ThreadPool>(), std::defer_lock);
        if(!lock.owns_lock())
            lock.lock();
        if(_idx < 0)
            _idx = f_thread_ids.size();
        f_thread_ids[std::this_thread::get_id()] = _idx;
        Threading::SetThreadId(_idx);
        _data->emplace_back(_thr_data);
    }
    thread_data() = _thr_data.get();
    tp->record_entry();
    tp->execute_thread(thread_data()->current_queue);
    tp->record_exit();
}

//======================================================================================//
// static member function that checks enabling of tbb library
bool
ThreadPool::using_tbb()
{
    return f_use_tbb;
}

//======================================================================================//
// static member function that initialized tbb library
void
ThreadPool::set_use_tbb(bool enable)
{
#if defined(PTL_USE_TBB)
    f_use_tbb = enable;
#else
    ConsumeParameters<bool>(enable);
#endif
}

//======================================================================================//

const ThreadPool::thread_id_map_t&
ThreadPool::get_thread_ids()
{
    return f_thread_ids;
}

//======================================================================================//

uintmax_t
ThreadPool::get_this_thread_id()
{
    auto _tid = ThisThread::get_id();
    {
        AutoLock lock(TypeMutex<ThreadPool>(), std::defer_lock);
        if(!lock.owns_lock())
            lock.lock();
        if(f_thread_ids.find(_tid) == f_thread_ids.end())
        {
            auto _idx          = f_thread_ids.size();
            f_thread_ids[_tid] = _idx;
        }
    }
    return f_thread_ids[_tid];
}

//======================================================================================//

ThreadPool::ThreadPool(const size_type& pool_size, VUserTaskQueue* task_queue,
                       bool _use_affinity, affinity_func_t _affinity_func)
: m_use_affinity(_use_affinity)
, m_pool_state(std::make_shared<std::atomic_short>(thread_pool::state::NONINIT))
, m_task_queue(task_queue)
, m_affinity_func(std::move(_affinity_func))
{
    auto master_id = get_this_thread_id();
    if(master_id != 0 && m_verbose > 1)
        std::cerr << "ThreadPool created on non-master slave" << std::endl;

    thread_data() = new ThreadData(this);

    // initialize after get_this_thread_id so master is zero
    this->initialize_threadpool(pool_size);

    if(!m_task_queue)
        m_task_queue = new UserTaskQueue(m_pool_size);
}

//======================================================================================//

ThreadPool::~ThreadPool()
{
    if(m_alive_flag->load())
    {
        std::cerr << "Warning! ThreadPool was not properly destroyed! Call "
                     "destroy_threadpool() before deleting the ThreadPool object to "
                     "eliminate this message."
                  << std::endl;
        m_pool_state->store(thread_pool::state::STOPPED);
        m_task_lock->lock();
        m_task_cond->notify_all();
        m_task_lock->unlock();
        for(auto& itr : m_threads)
            itr.join();
        m_threads.clear();
    }
}

//======================================================================================//

bool
ThreadPool::is_initialized() const
{
    return !(m_pool_state->load() == thread_pool::state::NONINIT);
}

//======================================================================================//

void
ThreadPool::set_affinity(intmax_t i, Thread& _thread)
{
    try
    {
        NativeThread native_thread = _thread.native_handle();
        intmax_t     _pin          = m_affinity_func(i);
        if(m_verbose > 0)
        {
            std::cout << "Setting pin affinity for thread " << _thread.get_id() << " to "
                      << _pin << std::endl;
        }
        Threading::SetPinAffinity(_pin, native_thread);
    } catch(std::runtime_error& e)
    {
        std::cout << "Error setting pin affinity" << std::endl;
        std::cerr << e.what() << std::endl;  // issue assigning affinity
    }
}

//======================================================================================//

ThreadPool::size_type
ThreadPool::initialize_threadpool(size_type proposed_size)
{
    //--------------------------------------------------------------------//
    // return before initializing
    if(proposed_size < 1)
        return 0;

    //--------------------------------------------------------------------//
    // store that has been started
    if(!m_alive_flag->load())
        m_pool_state->store(thread_pool::state::STARTED);

#if defined(PTL_USE_TBB)
    //--------------------------------------------------------------------//
    // handle tbb task scheduler
    if(f_use_tbb || m_tbb_tp)
    {
        m_tbb_tp                               = true;
        m_pool_size                            = proposed_size;
        tbb_global_control_t*& _global_control = tbb_global_control();
        // delete if wrong size
        if(m_pool_size != proposed_size)
        {
            delete _global_control;
            _global_control = nullptr;
        }

        if(!_global_control)
        {
            _global_control = new tbb_global_control_t(
                tbb::global_control::max_allowed_parallelism, proposed_size + 1);
            if(m_verbose > 0)
            {
                std::cout << "ThreadPool [TBB] initialized with " << m_pool_size
                          << " threads." << std::endl;
            }
        }

        // create task group (used for async)
        if(!m_tbb_task_group)
            m_tbb_task_group = new tbb_task_group_t();
        return m_pool_size;
    }
#endif

    m_alive_flag->store(true);

    //--------------------------------------------------------------------//
    // if started, stop some thread if smaller or return if equal
    if(m_pool_state->load() == thread_pool::state::STARTED)
    {
        if(m_pool_size > proposed_size)
        {
            while(stop_thread() > proposed_size)
                ;
            if(m_verbose > 0)
            {
                std::cout << "ThreadPool initialized with " << m_pool_size << " threads."
                          << std::endl;
            }
            if(!m_task_queue)
            {
                m_delete_task_queue = true;
                m_task_queue        = new UserTaskQueue(m_pool_size);
            }
            return m_pool_size;
        }
        else if(m_pool_size == proposed_size)  // NOLINT
        {
            if(m_verbose > 0)
            {
                std::cout << "ThreadPool initialized with " << m_pool_size << " threads."
                          << std::endl;
            }
            if(!m_task_queue)
            {
                m_delete_task_queue = true;
                m_task_queue        = new UserTaskQueue(m_pool_size);
            }
            return m_pool_size;
        }
    }

    //--------------------------------------------------------------------//
    // reserve enough space to prevent realloc later
    {
        AutoLock _task_lock(*m_task_lock);
        m_is_joined.reserve(proposed_size);
    }

    if(!m_task_queue)
        m_task_queue = new UserTaskQueue(proposed_size);

    auto this_tid = get_this_thread_id();
    for(size_type i = m_pool_size; i < proposed_size; ++i)
    {
        // add the threads
        try
        {
            // create thread
            Thread thr{ ThreadPool::start_thread, this, &m_thread_data,
                        this_tid + i + 1 };
            // only reaches here if successful creation of thread
            ++m_pool_size;
            // store thread
            m_main_threads.push_back(thr.get_id());
            // list of joined thread booleans
            m_is_joined.push_back(false);
            // set the affinity
            if(m_use_affinity)
                set_affinity(i, thr);
            // store
            m_threads.emplace_back(std::move(thr));
        } catch(std::runtime_error& e)
        {
            std::cerr << e.what() << std::endl;  // issue creating thread
            continue;
        } catch(std::bad_alloc& e)
        {
            std::cerr << e.what() << std::endl;
            continue;
        }
    }
    //------------------------------------------------------------------------//

    AutoLock _task_lock(*m_task_lock);

    // thread pool size doesn't match with join vector
    // this will screw up joining later
    if(m_is_joined.size() != m_main_threads.size())
    {
        std::stringstream ss;
        ss << "ThreadPool::initialize_threadpool - boolean is_joined vector "
           << "is a different size than threads vector: " << m_is_joined.size() << " vs. "
           << m_main_threads.size() << " (tid: " << std::this_thread::get_id() << ")";

        throw std::runtime_error(ss.str());
    }

    if(m_verbose > 0)
    {
        std::cout << "ThreadPool initialized with " << m_pool_size << " threads."
                  << std::endl;
    }

    return m_main_threads.size();
}

//======================================================================================//

ThreadPool::size_type
ThreadPool::destroy_threadpool()
{
    // Note: this is not for synchronization, its for thread communication!
    // destroy_threadpool() will only be called from the main thread, yet
    // the modified m_pool_state may not show up to other threads until its
    // modified in a lock!
    //------------------------------------------------------------------------//
    m_pool_state->store(thread_pool::state::STOPPED);

    //--------------------------------------------------------------------//
    // handle tbb task scheduler
#if defined(PTL_USE_TBB)
    if(m_tbb_task_group)
    {
        auto _func = [&]() { m_tbb_task_group->wait(); };
        if(m_tbb_task_arena)
            m_tbb_task_arena->execute(_func);
        else
            _func();
        delete m_tbb_task_group;
        m_tbb_task_group = nullptr;
    }
    if(m_tbb_task_arena)
    {
        delete m_tbb_task_arena;
        m_tbb_task_arena = nullptr;
    }
    if(m_tbb_tp && tbb_global_control())
    {
        tbb_global_control_t*& _global_control = tbb_global_control();
        delete _global_control;
        _global_control = nullptr;
        m_tbb_tp        = false;
        std::cout << "ThreadPool [TBB] destroyed" << std::endl;
    }
#endif

    if(!m_alive_flag->load())
        return 0;

    //------------------------------------------------------------------------//
    // notify all threads we are shutting down
    m_task_lock->lock();
    m_task_cond->notify_all();
    m_task_lock->unlock();
    //------------------------------------------------------------------------//

    if(m_is_joined.size() != m_main_threads.size())
    {
        std::stringstream ss;
        ss << "   ThreadPool::destroy_thread_pool - boolean is_joined vector "
           << "is a different size than threads vector: " << m_is_joined.size() << " vs. "
           << m_main_threads.size() << " (tid: " << std::this_thread::get_id() << ")";

        throw std::runtime_error(ss.str());
    }

    for(size_type i = 0; i < m_is_joined.size(); i++)
    {
        //--------------------------------------------------------------------//
        //
        if(i < m_threads.size())
            m_threads.at(i).join();

        //--------------------------------------------------------------------//
        // if its joined already, nothing else needs to be done
        if(m_is_joined.at(i))
            continue;

        //--------------------------------------------------------------------//
        // join
        if(std::this_thread::get_id() == m_main_threads[i])
            continue;

        //--------------------------------------------------------------------//
        // thread id and index
        auto _tid = m_main_threads[i];

        //--------------------------------------------------------------------//
        // erase thread from thread ID list
        if(f_thread_ids.find(_tid) != f_thread_ids.end())
            f_thread_ids.erase(f_thread_ids.find(_tid));

        //--------------------------------------------------------------------//
        // it's joined
        m_is_joined.at(i) = true;
    }

    m_thread_data.clear();
    m_threads.clear();
    m_main_threads.clear();
    m_is_joined.clear();

    m_alive_flag->store(false);

    auto start   = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration<double>{};
    // wait maximum of 30 seconds for threads to exit
    while(m_thread_active->load() > 0 && elapsed.count() < 30)
    {
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        elapsed = std::chrono::steady_clock::now() - start;
    }

    auto _active = m_thread_active->load();

    if(get_verbose() >= 0)
    {
        if(_active == 0)
        {
            std::cout << "ThreadPool destroyed" << std::endl;
        }
        else
        {
            std::cout << "ThreadPool destroyed but " << _active
                      << " threads might still be active (and cause a termination error)"
                      << std::endl;
        }
    }

    if(m_delete_task_queue)
    {
        delete m_task_queue;
        m_task_queue = nullptr;
    }

    return 0;
}

//======================================================================================//

ThreadPool::size_type
ThreadPool::stop_thread()
{
    if(!m_alive_flag->load() || m_pool_size == 0)
        return 0;

    //------------------------------------------------------------------------//
    // notify all threads we are shutting down
    m_task_lock->lock();
    m_is_stopped.push_back(true);
    m_task_cond->notify_one();
    m_task_lock->unlock();
    //------------------------------------------------------------------------//

    // lock up the task queue
    AutoLock _task_lock(*m_task_lock);

    while(!m_stop_threads.empty())
    {
        auto tid = m_stop_threads.front();
        // remove from stopped
        m_stop_threads.pop_front();
        // remove from main
        for(auto itr = m_main_threads.begin(); itr != m_main_threads.end(); ++itr)
        {
            if(*itr == tid)
            {
                m_main_threads.erase(itr);
                break;
            }
        }
        // remove from join list
        m_is_joined.pop_back();
    }

    m_pool_size = m_main_threads.size();
    return m_main_threads.size();
}

//======================================================================================//

ThreadPool::task_queue_t*&
ThreadPool::get_valid_queue(task_queue_t*& _queue) const
{
    if(!_queue)
        _queue = new UserTaskQueue{ static_cast<intmax_t>(m_pool_size) };
    return _queue;
}
//======================================================================================//

void
ThreadPool::execute_thread(VUserTaskQueue* _task_queue)
{
    // how long the thread waits on condition variable
    // static int wait_time = GetEnv<int>("PTL_POOL_WAIT_TIME", 5);

    ++(*m_thread_awake);

    // initialization function
    m_init_func();

    ThreadId    tid  = ThisThread::get_id();
    ThreadData* data = thread_data();
    // auto        thread_bin = _task_queue->GetThreadBin();
    // auto        workers    = _task_queue->workers();

    auto start   = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration<double>{};
    // check for updates for 60 seconds max
    while(!_task_queue && elapsed.count() < 60)
    {
        elapsed = std::chrono::steady_clock::now() - start;
        data->update();
        _task_queue = data->current_queue;
    }

    if(!_task_queue)
    {
        --(*m_thread_awake);
        throw std::runtime_error("No task queue was found after 60 seconds!");
    }

    assert(data->current_queue != nullptr);
    assert(_task_queue == data->current_queue);

    // essentially a dummy run
    if(_task_queue)
    {
        data->within_task = true;
        auto _task        = _task_queue->GetTask();
        if(_task)
        {
            (*_task)();
        }
        data->within_task = false;
    }

    // threads stay in this loop forever until thread-pool destroyed
    while(true)
    {
        static thread_local auto p_task_lock = m_task_lock;

        //--------------------------------------------------------------------//
        // Try to pick a task
        AutoLock _task_lock(*p_task_lock, std::defer_lock);
        //--------------------------------------------------------------------//

        auto leave_pool = [&]() {
            auto _state      = [&]() { return static_cast<int>(m_pool_state->load()); };
            auto _pool_state = _state();
            if(_pool_state > 0)
            {
                // stop whole pool
                if(_pool_state == thread_pool::state::STOPPED)
                {
                    if(_task_lock.owns_lock())
                        _task_lock.unlock();
                    return true;
                }
                // single thread stoppage
                else if(_pool_state == thread_pool::state::PARTIAL)  // NOLINT
                {
                    if(!_task_lock.owns_lock())
                        _task_lock.lock();
                    if(!m_is_stopped.empty() && m_is_stopped.back())
                    {
                        m_stop_threads.push_back(tid);
                        m_is_stopped.pop_back();
                        if(_task_lock.owns_lock())
                            _task_lock.unlock();
                        // exit entire function
                        return true;
                    }
                    if(_task_lock.owns_lock())
                        _task_lock.unlock();
                }
            }
            return false;
        };

        // We need to put condition.wait() in a loop for two reasons:
        // 1. There can be spurious wake-ups (due to signal/ENITR)
        // 2. When mutex is released for waiting, another thread can be woken up
        //    from a signal/broadcast and that thread can mess up the condition.
        //    So when the current thread wakes up the condition may no longer be
        //    actually true!
        while(_task_queue->empty())
        {
            auto _state = [&]() { return static_cast<int>(m_pool_state->load()); };
            auto _size  = [&]() { return _task_queue->true_size(); };
            auto _empty = [&]() { return _task_queue->empty(); };
            auto _wake  = [&]() { return (!_empty() || _size() > 0 || _state() > 0); };

            if(leave_pool())
                return;

            if(_task_queue->true_size() == 0)
            {
                if(m_thread_awake && m_thread_awake->load() > 0)
                    --(*m_thread_awake);

                // lock before sleeping on condition
                if(!_task_lock.owns_lock())
                    _task_lock.lock();

                // Wait until there is a task in the queue
                // Unlocks mutex while waiting, then locks it back when signaled
                // use lambda to control waking
                m_task_cond->wait(_task_lock, _wake);

                if(_state() == thread_pool::state::STOPPED)
                    return;

                // unlock if owned
                if(_task_lock.owns_lock())
                    _task_lock.unlock();

                // notify that is awake
                if(m_thread_awake && m_thread_awake->load() < m_pool_size)
                    ++(*m_thread_awake);
            }
            else
                break;
        }

        // release the lock
        if(_task_lock.owns_lock())
            _task_lock.unlock();

        //----------------------------------------------------------------//

        // leave pool if conditions dictate it
        if(leave_pool())
            return;

        // activate guard against recursive deadlock
        data->within_task = true;
        //----------------------------------------------------------------//

        // execute the task(s)
        while(!_task_queue->empty())
        {
            auto _task = _task_queue->GetTask();
            if(_task)
            {
                (*_task)();
            }
        }
        //----------------------------------------------------------------//

        // disable guard against recursive deadlock
        data->within_task = false;
        //----------------------------------------------------------------//
    }
}

//======================================================================================//
