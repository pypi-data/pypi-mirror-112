// MIT License
//
// Copyright (c) 2020, The Regents of the University of California,
// through Lawrence Berkeley National Laboratory (subject to receipt of any
// required approvals from the U.S. Dept. of Energy).  All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

/** \file runtime/insert.hpp
 * \headerfile runtime/insert.hpp "timemory/runtime/insert.hpp"
 * Provides implementation for initialize, enumerate_components which regularly
 * change as more features are added
 *
 */

#pragma once

#include "timemory/runtime/types.hpp"

#include <initializer_list>
#include <string>
#include <type_traits>

namespace tim
{
//======================================================================================//

template <size_t Idx, typename Type, template <size_t, typename> class Bundle,
          typename EnumT = int>
inline void
insert(Bundle<Idx, Type>& obj, std::initializer_list<EnumT> components)
{
    insert(obj, std::vector<EnumT>(components));
}

//--------------------------------------------------------------------------------------//

template <size_t Idx, typename Type, template <size_t, typename> class Bundle>
inline void
insert(Bundle<Idx, Type>& obj, const std::initializer_list<std::string>& components)
{
    insert(obj, enumerate_components(components));
}

//--------------------------------------------------------------------------------------//
//
/// this is for initializing with a container of string
//
template <size_t Idx, typename Type, template <size_t, typename> class Bundle,
          typename... ExtraArgs, template <typename, typename...> class Container>
inline void
insert(Bundle<Idx, Type>& obj, const Container<std::string, ExtraArgs...>& components)
{
    insert(obj, enumerate_components(components));
}

//--------------------------------------------------------------------------------------//
//
/// this is for initializing with a string
//
template <size_t Idx, typename Type, template <size_t, typename> class Bundle>
inline void
insert(Bundle<Idx, Type>& obj, const std::string& components)
{
    insert(obj, enumerate_components(tim::delimit(components)));
}

//--------------------------------------------------------------------------------------//

template <
    size_t Idx, typename Type, template <size_t, typename> class Bundle,
    template <typename, typename...> class Container, typename Intp,
    typename... ExtraArgs,
    typename std::enable_if<std::is_integral<Intp>::value ||
                                std::is_same<Intp, TIMEMORY_NATIVE_COMPONENT>::value,
                            int>::type>
void
insert(Bundle<Idx, Type>& obj, const Container<Intp, ExtraArgs...>& components)
{
    for(auto itr : components)
        runtime::insert(obj, itr);
}

//--------------------------------------------------------------------------------------//

template <size_t Idx, typename Type, template <size_t, typename> class Bundle,
          template <typename, typename...> class Container, typename... ExtraArgs>
void
insert(Bundle<Idx, Type>& obj, const Container<const char*, ExtraArgs...>& components)
{
    std::vector<std::string> _components;
    _components.reserve(components.size());
    for(auto itr : components)
        _components.emplace_back(std::string(itr));
    insert(obj, _components);
}

//--------------------------------------------------------------------------------------//

template <size_t Idx, typename Type, template <size_t, typename> class Bundle>
void
insert(Bundle<Idx, Type>& obj, const int ncomponents, const int* components)
{
    for(int i = 0; i < ncomponents; ++i)
        runtime::insert(obj, components[i]);
}

//======================================================================================//

}  // namespace tim

//======================================================================================//
