#ifndef CUSKETCH_H 
#define CUSKETCH_H

#include "common.h"

struct CUSketch:public Sketch{
public:
	CUSketch(uint d, uint w);
	~CUSketch();
	void Insert(cuc *str);
	uint Query(cuc *str, bool ml = FALSE);
	void PrintCounter(cuc* str, uint acc_val, uint query_val);

	float Predict(uint *t);
	bool need_analyze(uint * arr, int num) {
		std::sort(arr, arr + num);
		return true;
	}
private:
	HashFunction *hf;
	ushort** sketch;
	uint d;
	uint w;
	uint *t;
};

CUSketch::CUSketch(uint d, uint w):d(d), w(w){
	sketch = new ushort*[d];
	for(uint i = 0; i < d; ++i){
		sketch[i] = new ushort[w]();
	}
	hf = new HashFunction();
	t = new uint[d];
}

CUSketch::~CUSketch(){
	for(uint i = 0; i < d; ++i) delete [] sketch[i];
	delete [] sketch;
	delete hf;
	delete [] t;
}

void CUSketch::Insert(cuc *str){
	uint Min = INF_SHORT;
	for(uint i = 0; i < d; ++i){
		uint cid = hf->Str2Int(str, i)%w;
		t[i] = sketch[i][cid];
		Min = min(Min, t[i]);
	}
    if (Min == INF_SHORT)
        return;
	for(uint i = 0; i < d; ++i){
		if (t[i]==Min){
			uint cid = hf->Str2Int(str, i)%w;
			++sketch[i][cid];
		}
	}
}

uint CUSketch::Query(cuc *str, bool ml){
    uint Min = INF_SHORT;
    for(uint i = 0; i < d; ++i){
        uint cid = hf->Str2Int(str, i)%w;
        t[i] = sketch[i][cid];
        Min = min(Min, t[i]);
    }
	return (uint)Min;

}

void CUSketch::PrintCounter(cuc* str, uint acc_val,  uint query_val){
	for(uint i = 0; i < d; ++i){
		uint cid = hf->Str2Int(str, i)%w;
		t[i] = sketch[i][cid];
	}

    std::sort(t, t+d);
    printf("%u", acc_val);
	printf(" %u", query_val);
    for(uint i = 0; i < d; ++i){
        printf(" %u", t[i]);
    }
    printf("\n");
}


#endif