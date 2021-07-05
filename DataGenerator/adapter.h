#ifndef __ADAPTER_H__
#define __ADAPTER_H__

#include "tuple.h"
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>


typedef struct {
    unsigned char* trace_buf;
    unsigned char* ptr;
    unsigned long long cnt;
    unsigned long long cur;
} adapter_t;


adapter_t* adapter_init(const char* file, unsigned long long buf_size) {
    adapter_t* ret = (adapter_t*)calloc(1, sizeof(adapter_t));

    ret->trace_buf = (unsigned char*)calloc(buf_size, sizeof(unsigned char));
    ret->ptr = ret->trace_buf;
    
	FILE* input = fopen(file, "rb");

    uint8_t* p = ret->trace_buf;
    while (1) {
        if (p+sizeof(tuple_t) <= ret->trace_buf+buf_size) {
            int r = fread (p, sizeof(tuple_t), 1, input); 
            if (r != 1) {
                break;
            }
            ret->cnt++;
            p = p + sizeof(tuple_t);
        }
        else {
            break;
        }
    }
    fclose(input);
    return ret;
}

void adapter_destroy(adapter_t* adapter) {
    free(adapter->trace_buf);
}

int adapter_next(adapter_t* adapter, tuple_t* p) {
    if (adapter->cur == adapter->cnt) {
        return -1;
    }

    adapter->cur++;
    memcpy(p, adapter->ptr, sizeof(tuple_t));
    adapter->ptr += sizeof(tuple_t);

    return 0;
}

void adapter_reset(adapter_t* adapter) {
    adapter->cur =0;
    adapter->ptr = adapter->trace_buf;
}

const char* strconcat(const char* a, const char* b) {

}

#endif