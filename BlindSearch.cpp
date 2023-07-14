
/*This is the C++ file that contains the actual code for the BlindSearch algorithms*/
//For now, instead of using a custom stream to output to, we use the placeholder cout for stream output
#include <fstream>
#include <iostream>
#include "TelemetryReader.h"
using namespace std;

// RandomGridChecking is meant to simulate the drone going to random squares on the grid, and then checking if it has a radiation measurement there
// This function should guarantee that the drone does not visit a square that it has visited before.
// This function is probably not going to be used at all over rectilinear and concentric circles, becaucse concentric circles guarantees more consistent resultants
bool randomGridChecking(bool** visitedSquare, int square1DNum){ 
	srand(time(NULL));
	int xCoord = rand()%square1DNum;
	srand(time(NULL));
	int yCoord = rand()%square1DNum;
	while(visitedSquare[xCoord][yCoord]){
		//So while the random coordinates being generated are part of the visited squares, we keep generating random squares to visit
		srand(time(NULL));
		int xCoord = rand()%square1DNum;
		srand(time(NULL));
		int yCoord = rand()%square1DNum;
	}
	//That means at this point in the control flow, we have finally found a square that has not been reached before
	visitedSquare[xCoord][yCoord] = true; //First we set it to true, which implies that we have now visited the square
	/* So now we need to make sure that we can change the drone's position to go to the randomly generated square */
	
	
	

	return false;

}


// RectilinearGridChecking is meant to simulate the drone going literally up and down the squares on the grid, the most exhaustive search method
// However, this is also the slowest method, I will write this just in case we want to use it.
// This should also use a method that can detect radiation from the detector on the drone.
// We'll also put a CSV recording mode in this method depending on the parameters passed in main.
bool rectilinearGridChecking(bool recording){
	ofstream outfile;
	pair<int,int> horizontalMotion(10,0);
	pair<int,int> upMotion(0,10);
	pair<int,int> downMotion(0,-10);
	pair<int,int> currPos(0,0);
	int step = 0;
	while(currPos.first != 290 && currPos.second !=0){ //the reasons these are the end conditions of the while loop is because of the specific drawing I made.
		currPos.first += horizontalMotion.first;
		++step;
		if(step > 0){
			currPos.first+= horizontalMotion.first;
		}
		getRadiationReading();
		for(int i = 0; i < 30; ++i){
			getRadiationReading();
			currPos.second += upMotion.second;
		}
		currPos.second+= horizontalMotion.first;
		for(int i = 0; i < 30; ++i){
			getRadiationReading();
			currPos.second+= downMotion.second;
		}
	}
	return false;
}
/* ConcentricGridChecking is meant to simulate the drone quite literally making concentric circles around the center of the field, while this is not as 
exhaustive as rectilinear, it covers ~79.5% of the field with only 42.44% of the total distance needed to travel in rectilinear, which is a much higher jump 
in efficiency. (Remember, curvilinear is always going to be better than rectilinear, or any flight path with corners because with corners, you are overscanning
the area by the corners.) */
bool concentricCircleChecking(){
	/* we should probably get the center of the circle as a paramter for the function, but for now, we'll just assume that the field is 300x300, so
	the center is (150,150). We should also take the output stream as a parameter so that we can send to the output stream. For now, we will assume 
	the output stream is the terminal*/
	pair<int,int> center(150,150);
	double radius = 140;
	while(radius > 0){
		std::cout << radius << " " << center.first <<" "<< center.second << std::endl;
		radius-=20;
		if(getRadiationReading() != 0){//Figure out how to get radiation reading for this break, IT'S VERY VERY IMPORTANT.
			return true;
		}
	}
	/* If control flow reaches this point, that means that the source was not detected in the circle, we have 4 areas to check. Least likely area is bottom left.
	we know that the best path is curvilinear, so we can't have rectilinear search in the 4 areas. What we can do is create more concetric circles, but this time
	they grow outwards instead of growing inwards.*/
	radius = 160;
	while(radius < 240){
		std::cout << radius << " " << center.first <<" "<< center.second  << std::endl;
		radius += 20;
		if(getRadiationReading() != 0){//Figure out how to get radiation reading for this break, IT'S VERY VERY IMPORTANT.
			return true;
		}
	}
	return false; // I don't actually know when this will be reached, probably only if the source is quite literally in the corner.
	
}

/*The way blind search algorithms should be implemented is that the grid being processed with code should emulate the
Cartesian plane, in the sense that the coordinates start at the bottom left of the screen, and values increase as you go up,
or as you go right.*/


// *IMPLEMENT OTHER BLIND SEARCH ALGORITHMS IF NEEDED HERE*