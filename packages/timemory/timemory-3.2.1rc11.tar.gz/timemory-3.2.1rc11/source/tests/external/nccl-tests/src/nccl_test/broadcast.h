
#pragma once

#include "nccl_test/common.h"

void
BroadcastGetBuffSize(size_t* sendcount, size_t* recvcount, size_t count, int nranks);

testResult_t
BroadcastRunTest(struct threadArgs* args, int root, ncclDataType_t type,
                 const char* typeName, ncclRedOp_t op, const char* opName);

struct testEngine broadcastEngine = { BroadcastGetBuffSize, BroadcastRunTest };
