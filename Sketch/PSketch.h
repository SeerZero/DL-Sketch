#ifndef PSKETCH_H
#define PSKETCH_H

#include "common.h"

struct PSketch:public Sketch{
public:
	PSketch(uint d, uint w);
	~PSketch();
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

PSketch::PSketch(uint d, uint w):d(d), w(w){
	srand(time(0));
	sketch = new ushort*[d];
	for(uint i = 0; i < d; ++i){
		 sketch[i] = new ushort[w]();
		 
	}
	hf = new HashFunction();
	t = new uint[d];
}

PSketch::~PSketch(){
	for(uint i = 0; i < d; ++i) delete [] sketch[i];
	delete [] sketch;
	delete hf;
	delete [] t;
}

void PSketch::Insert(cuc *str){
	uint i = rand()%d;
	uint cid = hf->Str2Int(str, i)%w;
	if (sketch[i][cid] == -1) {
        return;
    }
	++sketch[i][cid];
}

uint PSketch::Query(cuc *str, bool ml){
	uint sum = 0;
	for(uint i = 0; i < d; ++i){
		uint cid = hf->Str2Int(str, i)%w;
		sum += sketch[i][cid];
	}
	return sum;
}

void PSketch::PrintCounter(cuc* str, uint acc_val, uint query_val) {
	 
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