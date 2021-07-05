#include "Data.h"

using namespace std;

string input_dir = "../data/generator/";
string output_dir = "../data/sketch/";
//parameter
int sampling_para = 1;  //sampling one among sampling_para
int max_epoch = 0;		//epoch number
int sk_type = 0;		//sketch type: 0 CM 1 CU 2 P 
int sk_r = 0;			//row of sketch
int sk_c = 0;			//column of sketch

int main(){
	// Parameter Input
	cout<<"max_epoch, sampling_para, sk_type, sk_r, sk_c"<<endl;
	ifstream fin("sketch_para.txt");
	fin>>max_epoch>>sampling_para>>sk_type>>sk_r>>sk_c;	
	fin.close();
    
	// Simulate switche, insert the flows into the sketch
	cout<<"switch"<<endl;
	cout<<max_epoch<<' '<<1<<' '<<sk_type<<' '<<sk_r<<' '<<sk_c<<endl;
	int sc = run(max_epoch, 1, input_dir, output_dir, sk_type, sk_r, sk_c, sampling_para);
	cout<<sc<<endl;
	// Simulate server, insert the flows into the sketch
	cout<<"server"<<endl;
	cout<<max_epoch<<' '<<sampling_para<<' '<<sk_type<<' '<<sk_r<<' '<<sk_c / sc<<endl;
	run(max_epoch, sampling_para, input_dir, output_dir, sk_type, sk_r, sk_c / sc, 0);
	return 0;
}