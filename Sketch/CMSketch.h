#ifndef CMSKETCH_H
#define CMSKETCH_H

#include "common.h"

struct CMSketch:public Sketch{
public:
	CMSketch(uint d, uint w);
	~CMSketch();
	void Insert(cuc *str);
	uint Query(cuc *str, bool ml = FALSE);
	void PrintCounter(cuc* str, uint acc_val, uint query_val);

private:
	HashFunction *hf;
	ushort** sketch;
	uint d;
	uint w;
	uint *t;
};

CMSketch::CMSketch(uint d, uint w):d(d), w(w){
	sketch = new ushort*[d];
	for(uint i = 0; i < d; ++i){
		 sketch[i] = new ushort[w]();
	}
	hf = new HashFunction();
	t = new uint[d];
}

CMSketch::~CMSketch(){
	for(uint i = 0; i < d; ++i) delete [] sketch[i];
	delete [] sketch;
	delete hf;
	delete [] t;
}

void CMSketch::Insert(cuc *str){
    for (uint i = 0; i < d; ++i){
        uint cid = hf->Str2Int(str, i) % w;
        if (sketch[i][cid] == -1) {
            return;
        }
		++sketch[i][cid];
	}
}

uint CMSketch::Query(cuc *str, bool ml){

	uint Min = INF_SHORT;
	for(uint i = 0; i < d; ++i){
		uint cid = hf->Str2Int(str, i)%w;
		t[i] = sketch[i][cid];
		Min = min(Min, t[i]);
	}

	return (uint)Min;

}

void CMSketch::PrintCounter(cuc* str, uint acc_val, uint query_val){
	for(uint i = 0; i < d; ++i){
		uint cid = hf->Str2Int(str, i)%w;
		t[i] = sketch[i][cid];
	}
	std::sort(t, t + d);
	printf("%u", acc_val);
	printf(" %u", query_val);
	for(uint i = 0; i < d; ++i){
		printf(" %u", t[i]);
	}
	printf("\n");
}



#endif