#include <iostream>
#include <string>
#include <cmath>
#include <fstream>
#include <cassert>
#include <stdlib.h>
#include <time.h>

using namespace std;


int main(int argc, char** argv){
	assert(argc == 8);
	
	ofstream fout;
	fout.open(argv[1]); //this creates the CSV, or overwrites the previous CSV
	
	//the following statements just stores the inputs from the program as values to use later
	double sourceXCoord = stod(argv[2])+1;
	double sourceYCoord = stod(argv[3])+1;
	int squareDimension = stoi(argv[4]);
	double upperCoeffiecient = stod(argv[5]);
	bool noisy = stoi(argv[6]);
	bool isRandom = stoi(argv[7]);
	double noise;
	double numToPrint;
	srand(time(NULL));
	
	if(isRandom){//change this to an option where you only take one parameter and it's random, or it takes multiple parameters for a set source location
		
		squareDimension = rand() % 1000 +1;
		sourceXCoord = rand() % squareDimension + 1;
		sourceYCoord = rand() % squareDimension + 1;
		
	}
	
	int currX;
	int currY;
	
	//nested for loop actually handles writing to the CSV
	for(int i = 0; i < squareDimension+1; ++i){
		
		currX = i+1;
		for(int j = 0; j < squareDimension +1; ++j){
			
			if(i == 0 || j == 0){
				if(i == 0 && j == 0){
				fout << "coordinates";
			}
			if(i != 0 && j ==0){
				fout << i;
				
			}
			else if(i == 0 && j != 0){
				fout << j;
			} 
			if(j!=squareDimension){
				fout<<",";
			}
			}
			
			else{
				currY = j+1;
			numToPrint = upperCoeffiecient/(pow((currX-sourceXCoord),2) + pow((currY-sourceYCoord),2));
			if(currX-sourceXCoord == 0 && currY-sourceYCoord == 0){//if we're literally on top of the source
				numToPrint = 2000;
			}
			if(noisy){
				noise = ((double)rand()) / RAND_MAX;
				numToPrint += noise; //there is probably a way to make this cleaner code, someone figure it out
			}
			fout << numToPrint;
			
			if(j!=squareDimension){
				fout <<",";
			}
			}
			
			
			
			
		}
		fout << endl;
	}
	fout.close();
	
	
	
	return 0;
}