#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/stat.h> 
#include "adapter.h"

char tmp[105];
int main () {
    const char* filename = "../data/caida/data.bin";
    const char* output_path = "../data/generator/";
    unsigned long long buf_size = 3000000000;
    int interval_len = 1000;
    int max_epoch = 100;
    adapter_t* adapter = adapter_init(filename, buf_size);
    tuple_t t;
    FILE* data;
    FILE* simpling;
    mkdir(output_path, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
    unsigned long long start_time = 0;
    uint32_t epoch = 0;
    int simp_now = 0;
    while (1) {
        if (adapter_next(adapter, &t) == -1) {
            break;
        }
        unsigned long long pkt_time = (unsigned long long)(t.pkt_ts*1000);
        if (start_time == 0) {
            start_time = pkt_time;
            char tmp[150]="";
            sprintf(tmp, "%s/%s%u%s", output_path, "ep_",epoch,".data");
            data = fopen(tmp, "w");
        }
        if (pkt_time - start_time > interval_len) {
            epoch++;
            printf("epoch %d finish\n", epoch);
            if (epoch == max_epoch) {
                break;
            }
            char tmp[150]="";
            sprintf(tmp, "%s/%s%u%s", output_path, "ep_",epoch,".data");
            data = fopen(tmp, "w");
            start_time = pkt_time;
        }
        fprintf(data, "%u %u %u %u %u %d %u %u %u %f %u %u\n",t.key.src_ip,t.key.dst_ip,t.key.src_port,
            t.key.dst_port,t.key.proto,t.size,
            t.tcp_ack,t.tcp_seq,t.tcp_flag,
            t.pkt_ts,t.ip_hdr_size,t.tcp_hdr_size);
    }
    adapter_destroy(adapter);
    return 0;
}
