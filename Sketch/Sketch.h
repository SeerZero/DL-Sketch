#ifndef SKETCH_H
#define SKETCH_H

#include "CMSketch.h"
#include "CUSketch.h"
#include "PSketch.h"

// Initialize a sketch
// 0--CM
// 1--CU
// 2--P
void* CreateSketch(uint type, uint d, uint w){
	void* ptr = NULL;
	switch(type){
		case 0: {ptr = (void*)new CMSketch(d, w); break;} 
		case 1: {ptr = (void*)new CUSketch(d, w); break;}
		case 2: {ptr = (void*)new PSketch(d, w); break;}
		default: {printf("Wrong Parameter!\n"); break;}
	}
	return ptr;
}

//Insert str to sketch
void Insert(void *ptr, uint type, cuc* str){
	switch(type){
		case 0: {CMSketch *my_cm = (CMSketch*)ptr; my_cm->Insert(str); break; }
		case 1: {CUSketch *my_cu = (CUSketch*)ptr; my_cu->Insert(str); break;}
		case 2: {PSketch *my_p = (PSketch*)ptr; my_p->Insert(str); break;}
		default: {printf("Wrong Parameter!\n"); break;}
	}
}

//Query str in sketch
uint Query(void *ptr, uint type, cuc* str){
	uint res = 0;
	switch(type){
		case 0: {CMSketch *my_cm = (CMSketch*)ptr; res = my_cm->Query(str); break;}
		case 1: {CUSketch *my_cu = (CUSketch*)ptr; res = my_cu->Query(str); break;}
		case 2: {PSketch *my_p = (PSketch*)ptr; res = my_p->Query(str); break;}
		default: {printf("Wrong Parameter!\n"); break;}
	}
	return res;
}

//PrintCounter in sketch
void PrintCounter(void *ptr, uint type, cuc* str,uint acc_val, uint query_val){
	uint res = 0;
	switch(type){
		case 0: {CMSketch *my_cm = (CMSketch*)ptr; my_cm->PrintCounter(str, acc_val, query_val); break;}
		case 1: {CUSketch *my_cu = (CUSketch*)ptr; my_cu->PrintCounter(str, acc_val, query_val); break;}
		case 2: {PSketch *my_p = (PSketch*)ptr; my_p->PrintCounter(str, acc_val, query_val); break;}
		default: {printf("Wrong Parameter!\n"); break;}
	}
}

#endif