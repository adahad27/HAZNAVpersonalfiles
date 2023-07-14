/*MAIN AUTHORS: Abhishek Dahad(adahad@umich.edu)
PURPOSE: Autonomously decide what IRADs should do in the case of detecting or not detecting a source.
MASTER FIXLIST:
1.) Okay figure out how to use kalman filters in c++, screw this matlab shit(https://github.com/hmartiro/kalman-cpp)
2.) Figure out whether random search, rectilinear search is better, or a third secret thing(for now we're just going with random)
3.) WRITE READABLE CODE
4.) Probably try developing own kalman filter(I just think it'll be really cool to do it myself honestly)
5.) Figure out how to interface with detectors on the drone. Will need it to send commands
6.) Honestly we need to figure out how the program is going to run, will it take in input dynamically, 
or we rerun main everytime a new measurement is taken. I think it might be more efficient if it takes in input dynamically,
because then we don't have to deal with so much creation and deletion of dynamically allocated memory.
7.)*/


#include <iostream>
#include "BlindSearch.h"
#include "InformedSearch.h"
#include "TelemetryReader.h"
#include <cassert>

using namespace std;
//For the first iteration of the algorithm, we assume that the geofence is a square, and we also assume that there is only one source
// We will also use matlab's autonomous navigation algorithm for kalman filtering for now, unless I figure out later how to actually write a kalman filter
// We will assume that takeReading() and getCurrPos() are implemented methods.





/* General Description: This program is supposed to continously take in inputs from telemetry to devise where the drone should go next. The algorithm 
should have 2 broad modes, one is for single source detection, and the other one is for radiation mapping, which type it needs will be passed in as a 
parameter for now. This drone will also only be searching in a square area. */
int main(int argc, char** argv){
	bool sourceLocated = false;
	pair<double, double> currPos = {0,0};
	if(argc == 2 && string(argv[1]).compare("mapping") == 0){
		assert(false);
		rectilinearGridChecking(true);
	}
	else{
		while(!sourceLocated){
		if(getRadiationReading() == 0){
			concentricCircleChecking();
		}
		informedSearcher(getCurrReading(), sourceLocated);

	}
	currPos = {0,0} ;//at this point in the program, the drone has found the source, and will now return to the origin
	}
	
	

	}
	
	


