#ifndef __TUPLE_H__
#define __TUPLE_H__

#include <stdint.h>

typedef struct __attribute__ ((__packed__)) FlowKey {
	// 8 (4*2) bytes
    uint32_t src_ip;  
    uint32_t dst_ip;
	// 4 (2*2) bytes
    uint16_t src_port;
    uint16_t dst_port;
    // 1 bytes
    uint8_t proto;
} flow_key_t;

typedef struct __attribute__((__packed__)) Tuple {
    flow_key_t key;

    // 8 bytes
	int32_t size;			// inner IP datagram length (header + data)

    // 9 bytes
    uint32_t tcp_ack;  
    uint32_t tcp_seq;  
    uint8_t tcp_flag;

	// 8 bytes
	double pkt_ts;				// timestamp of the packet
    uint8_t ip_hdr_size;
    uint8_t tcp_hdr_size;

} tuple_t;

#endif
