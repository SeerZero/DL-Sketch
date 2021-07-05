#ifndef Data_H
#define Data_H
#include "Sketch.h"
#include "Tuple.h"
using namespace std;


vector<Tuple> tuple_list;
vector<Flowkey> flowkey_list;
map<Flowkey,uint> flowkey_count;
vector<double>pre_ep;

string toString(int x){
    string s;
    stack<char>stk;
	do{stk.push('0'+x%10);x/=10;}while(x!=0);
    while(!stk.empty()){s+=stk.top();stk.pop();}
    return s;
}

Tuple Get_tuple(ifstream & fin){
    Tuple t;
	fin>>t.key.src_ip;
    fin>>t.key.dst_ip;
    fin>>t.key.src_port;
    fin>>t.key.dst_port;
	int tmp;
	fin>>tmp;
	t.key.proto = (unsigned char)tmp;
    fin>>t.size;
    fin>>t.tcp_ack;
	fin>>t.tcp_seq;
    fin>>tmp;
	t.tcp_flag = (unsigned char)tmp;
    fin>>t.pkt_ts;
	fin>>tmp;
    t.ip_hdr_size = (unsigned char)tmp;
	fin>>tmp;
	t.tcp_hdr_size = (unsigned char)tmp;
	return t;	
}


void Insert_and_Print(int epoch, int sampling_para, string output_dir, int sk_type, int sk_r, int sk_c){
    string sk_name[] = {"cmsk","cusk","psk"};
    void * sketch = CreateSketch(sk_type, sk_r, sk_c);
    for(int i=0;i<tuple_list.size();i++){
        Insert(sketch, 0, (cuc*)&(tuple_list[i].key));
    }
    string outputfile = output_dir + "sp" + toString(sampling_para) +"_ep" +toString(epoch) + "_" + sk_name[sk_type] +"_" + toString(sk_r) + ".sketch";
    const char *p = outputfile.data();
    double sum_diff = 0;
    double sum_real = 0;
    freopen(p,"w",stdout);
    for(int k=0;k<flowkey_list.size();k++){
        double t = Query(sketch, sk_type, (cuc*)&(flowkey_list[k]));
        sum_real += t;
        t = t - flowkey_count[flowkey_list[k]];
        sum_diff += t > 0 ? t : -t;
        PrintCounter(sketch, 0, (cuc*)&(flowkey_list[k]), flowkey_count[flowkey_list[k]], Query(sketch, sk_type, (cuc*)&(flowkey_list[k])));
    }
    //fclose(stdout);
    freopen("/dev/tty", "w", stdout);
    pre_ep.push_back((sum_real - sum_diff)/sum_real);
}


int Get_Data(int epoch, int sampling_para, string input_dir, int output){
    tuple_list.clear();
	flowkey_list.clear();
	flowkey_count.clear();
    string filename = input_dir + "ep_" + toString(epoch) + ".data";
	ifstream fin(filename);
	int cnt = 0;
	while(fin.peek()!=EOF){
		Tuple t = Get_tuple(fin);
		cnt ++;
		if(cnt % sampling_para != 0)continue;
		tuple_list.push_back(t);
		if(flowkey_count.count(t.key) == 0){
			flowkey_count[t.key] = 1;
			flowkey_list.push_back(t.key);
		}else{
			flowkey_count[t.key]++;
		}
	}
	fin.close();
    if(output)
        cout<<"sp_para:"<<sampling_para<<" epoch:"<<epoch<<" "<<" tuple_num:"<<tuple_list.size()<<" flowkey_num:"<<flowkey_list.size()<<endl;
    return flowkey_list.size();
}


void write_precision(int sampling_para, string output_dir, int sk_type, int sk_r, int sk_c){
    string sk_name[] = {"cmsk","cusk","psk"};
    string filename = output_dir + "precision_sp" +toString(sampling_para) + "_" + sk_name[sk_type] + "_"+ toString(sk_r)+"_" + toString(sk_c) + ".csv";
    ofstream fout(filename);
    fout<<"epoch,precision";
    double sum = 0;
    for(int i=0;i<pre_ep.size();i++){
        sum += pre_ep[i];
        fout<<i<<','<<pre_ep[i]<<endl;
    }
    fout<<"mean,"<<sum/double(pre_ep.size())<<endl;
    cout<<"precision_mean,"<<sum/double(pre_ep.size())<<endl;
}

int run(int max_epoch,int sampling_para, string input_dir, string output_dir, int sk_type,int sk_r, int sk_c, int is_simpling){
    // Simulate servers and switches, insert the flows into the sketch
    for(int i = 0; i < max_epoch; i++){ 
        Get_Data(i, sampling_para, input_dir, 1);
        Insert_and_Print(i, sampling_para, output_dir, sk_type, sk_r, sk_c);
    }
    write_precision(sampling_para, output_dir, sk_type, sk_r, sk_c);

    
    // Sampling 10 seconds of traffic to determine the ratio of the two sketh columns
    double ret = 0;
    if(is_simpling != 0){
        cout<<"calc ratio"<<flush;
        for(int i = 0; i < 5; i++){
            cout<<'.'<<flush;
            ret += double(Get_Data(i, sampling_para, input_dir, 0)) / double(Get_Data(i, is_simpling, input_dir, 0));
        }
        ret /= 5.0; 
    }
    ret = int(ret);
    cout<<endl;
    return ret;
}

#endif