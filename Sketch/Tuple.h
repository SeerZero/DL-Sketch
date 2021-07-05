#ifndef TUPLE_H
#define TUPLE_H
#include <cstdint>
struct Flowkey{
    // 8 (4*2) bytes
    uint32_t src_ip;  // source IP address
    uint32_t dst_ip;
	// 4 (2*2) bytes
    uint16_t src_port;
    uint16_t dst_port;
    // 1 bytes
    uint8_t proto;
    bool operator <(const Flowkey & key2)const{
        int value = 0;
        if(src_ip!=key2.src_ip)
            value+=src_ip>key2.src_ip? 10000:-10000;
        if(dst_ip!=key2.dst_ip)
            value+=dst_ip>key2.dst_ip? 1000:-1000;
        if(src_port!=key2.src_port)
            value+=src_port>key2.src_port? 100:-100;
        if(dst_port!=key2.dst_port)
            value+=dst_port>key2.dst_port? 10:-10;
        if(proto!=key2.proto)
            value+=proto>key2.proto? 1:-1;
        return value>0;
    }
    
};

struct Tuple{
    
    struct Flowkey key;

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
};
#endif