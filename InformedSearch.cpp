

#include <iostream>
#include <string>
#include <time.h>
#include <stdlib.h>
#include <cassert>
#include <vector>
#include <cmath>
#include <math.h>
#include "TelemetryReader.h"
/* Another todo list for informed search specifically:
1.) Do the ROS 2 tutorial so you can learn how to use the API to send commands
2.) Learn how to do sinusoidal regression because that's probably how we're going to implement this version of HAZNAV. We'll probably use a python library for this
3.) Consider edge case for what happens when the drone moves in a circle and actually goes from finding a reading to not finding a reading */


/* Description of informedSearch:
Once it detects a reading, it basically flies in a 1/8th circle, and determines if the radiation readings are decreasing, if they are, then it goes around the
other way, and tries detecting a local maxima, once it finds one, it then flies in that direction again trying to detect a local maxima. Once it detects a 
local maxima travelling in a straight line, the final local maxima that is detected will be a very good approximation of where the source is.
The more data points that are collected, i.e. the more the drone stops, the more accurate the sinusoidal curve fitting will be. Which means that calculating
the local maxima will also be more accurate. Also include something that makes sure that the local maxima that is detected is less than the detector
reading from where the calculation circle is made. */
double regressionFunction(std::pair<double, double> data){
	
	return -1;
}
void informedSearcher(std::pair<int,int> currPos, bool &sourceFound){
	double internalTurnRadius = 5; /*This was pretty arbitrarily set, I have no idea what number to put here. This means that the circumference is 10pi.
	If the circumference is 10pi, we can measure the radiation at every pi/2. We can make  */
	
	double distTravel = 0.5;
	std::pair<int,int> standardPoint = currPos;
	double circumference = internalTurnRadius*2*M_PI;
	int numPoints = circumference/distTravel;
	std::pair<double, double>* dataLog = new std::pair<double, double>[numPoints];//this is creating a dynamic array that we will use to store data for the regression analysis.
	for(int i = 0; i < numPoints; ++i){
		std::cout << currPos.first + internalTurnRadius*cos(2*M_PI/numPoints * i) <<" "<< currPos.second + internalTurnRadius*sin(2*M_PI/numPoints * i)<<std::endl;
		
		dataLog[i].first = 2*M_PI/numPoints * i;
		dataLog[i].second = getRadiationReading();
		
	}
	double yaw = regressionFunction(*dataLog);
	//This is the yaw that the drone should turn in
	//The most the drone should go forward is 10m, because we are guaranteed that the source will be within 10m
	
	std::cout << yaw << std::endl;
	std::pair<double, double> secondaryDataLog[50];
	for(int j = 0; j < 50; ++j){
		currPos.first += cos(yaw)/pow(2,0.5);
		currPos.second += sin(yaw)/pow(2,0.5);
		secondaryDataLog[j].first = pow(pow(currPos.first- standardPoint.first, 2) + pow(currPos.second - standardPoint.second, 2), 0.5);//I guess we can calculate the eucliean distance between the new point and the center point from where everything was calculated.
		secondaryDataLog[j].second = getRadiationReading();
	}
	sourceFound = true;
	
}

/* A high level overview, is that it basically takes in terms in csv format, or just through an input stream, and then uses regression to fit a sinusoidal
curve to it. Once we have the best fit curve, we can simply optimize the function to find where the local maxima is. This will return the key where the 
maxima was found*/

