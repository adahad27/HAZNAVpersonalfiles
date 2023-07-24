import math
import numpy as np
from scipy.optimize import least_squares
#import pandas as pd
from matplotlib import pyplot as plt
import random


def LeastSquaresOneRun():    

    def NLS(beta, coordinates):
        
        return beta[0]/(((coordinates[:,0]-beta[1])**2)+ (coordinates[:,1]-beta[2])**2)

    def calc_residuals(beta, coordinates):
        y_pred = NLS(beta, coordinates)
        return np.subtract(y_pred, coordinates[:,2])





    def polarConversion(xCoord, yCoord, distance):
        #The parameters for this function are the predicted values from least squares
        #this function aims to return coordinates to travel to from the predicted values
        #it takes in the predicted values, decides what bearing to go in, and then returns the coordinates of the bearing after having travelled 'x' distance. In this case, 'hypotenuse' = x
        #as of yet, x is an arbitrary value of 3, this could be changed dynamically or set statically later after further testing
        courseAngle = math.atan(yCoord/xCoord)
        
        hypotenuse = distance
        xCoordIncrement = hypotenuse * math.cos(courseAngle)
        yCoordIncrement = hypotenuse * math.sin(courseAngle)
        return [xCoordIncrement, yCoordIncrement]



    class Drone:
        #This is just a struct for keeping this data glued together
        xCoord = 0
        yCoord = 0

    class radiationMap:
        #This map is meant to model the map of radiation, it returns radiation count based on position from the source
        def __init__(self, sourceX, sourceY, upperCoefficient, noise):
            self.sourceX = sourceX
            self.sourceY = sourceY
            self.noise = noise
            self.upperCoefficient = upperCoefficient
            

        def getRadCount(self, xCoord, yCoord):
            if(xCoord == self.sourceX and yCoord == self.sourceY):
                return 2000
                #Setting the max of the value so that when the drone reaches here, it doesn't bug out
            else:
                noiseContribution = 0
                if(self.noise):
                    noiseContribution = random.random()/100
                return self.upperCoefficient/((xCoord-self.sourceX)**2 + (yCoord-self.sourceY)**2) + noiseContribution


    drone = Drone()
    #random.randint(0,10)
    radMap = radiationMap(sourceX = 9 , sourceY = 7, upperCoefficient = 1, noise = False)

    coordinates = np.array([[drone.xCoord, drone.yCoord, radMap.getRadCount(drone.xCoord, drone.yCoord)]])# the array should have 2 dimensions. 
    
    initial_guess = [1, 5, 5]


    currCoords = [drone.xCoord, drone.yCoord]
    previousCoords = [drone.xCoord + 1, drone.yCoord + 1]
    
    prevRes = [0, 0, 0]

    travel_log = np.array([[0,0]]) #Replace (0,0) with the start position of the drone if it isn't (0,0)
    result_log = np.array([initial_guess])

    debugSum = 0
    while(math.sqrt((initial_guess[1] - prevRes[0])**2 + (initial_guess[2] - prevRes[1])**2) > 0.000001 ): #this is hard coded right now, we will have to change this to a tolerance value because this is the main loop
        debugSum += math.sqrt((initial_guess[1] - prevRes[0])**2 + (initial_guess[2] - prevRes[1])**2)
        if(debugSum > 60):
            #This is meant to prevent infinite loops from happening, the value of debugSum can be changed depending on testing data
            break
        if(drone.xCoord > 10 or drone.yCoord > 10 or drone.xCoord < -1 or drone.yCoord < -1):
            
            break
        
        
        currCoords = np.array([[drone.xCoord, drone.yCoord, radMap.getRadCount(drone.xCoord, drone.yCoord)]])
        extraIncrementArray = polarConversion(initial_guess[1], initial_guess[2],0.5)
        extraCoords = np.array([[drone.xCoord + extraIncrementArray[0], drone.yCoord + extraIncrementArray[1], radMap.getRadCount(drone.xCoord + extraIncrementArray[0], drone.yCoord + extraIncrementArray[1])]])
        
        coordinates = np.concatenate((coordinates, currCoords, extraCoords)) #the argument has to be passed in as a tuple idk why, probably some interface thing to make sure that nothing is modified?

        results = least_squares(calc_residuals, x0 = initial_guess, args=[coordinates])

        #I think we should change our initital guess according to the actual values that are outputted by the least squares method, we could also try using the Levenberg-Marquardt method, but that is a later problem
        prevRes = initial_guess
        initial_guess = results.x

        incrementArray = polarConversion(results.x[1], results.x[2],0.5)
        
        
        
        previousCoords = [drone.xCoord, drone.yCoord]
        drone.xCoord += incrementArray[0]
        drone.yCoord += incrementArray[1]
        currCoords = [drone.xCoord, drone.yCoord]
        if(radMap.getRadCount(currCoords[0], currCoords[1]) < radMap.getRadCount(previousCoords[0], previousCoords[1])):
            #then we make it go in the opposite direction
            #print("SPECIAL CASE HAS BEEN REACHED AND HOPEFULLY THIS WORKS")
            courseAngle = math.atan((previousCoords[1]-currCoords[1])/(previousCoords[0]-currCoords[0])) + math.pi
            currCoords = previousCoords
            #CHANGE THE 2 HERE ACCORDING TO DISTANCE IN POLARCONVERSION, WAS TOO LAZY TO FIGURE OUT ANOTHER WAY OF DOING THIS
            currCoords = [currCoords[0] + 0.5*math.cos(courseAngle), currCoords[1] + 0.5*math.sin(courseAngle)]
        
        
        #This just updates the respective logs needed in case of testing/debugging
        travel_log = np.concatenate((travel_log, [currCoords]))
        result_log = np.concatenate((result_log, [results.x]))

        

    currCoords = [results.x[1], results.x[2]]
    travel_log = np.concatenate((travel_log, [currCoords]))
    coordinateError =  math.sqrt((radMap.sourceX - results.x[1])**2 + (radMap.sourceY - results.x[2])**2)
    print("The actual source coordinates are (" + str(radMap.sourceX) +", " + str(radMap.sourceY) +") and the upper coefficient is " + str(radMap.upperCoefficient))
    print("The predicted source coordinates are (" + str(results.x[1]) + ", " + str(results.x[2]) +") and the upper coefficient is " + str(results.x[0]))

    # print(travel_log)
    # print(result_log)
    #Below is code responsible for plotting the path in a graph
    xCoordList = travel_log[:, 0]
    yCoordList = travel_log[:, 1]

    plt.plot(xCoordList, yCoordList)
    plt.scatter(radMap.sourceX, radMap.sourceY, c= "red")
    plt.show()


    return coordinateError


totalCoordinateError = 0
print("The error in measurement for this run was " + str(LeastSquaresOneRun()))
# for i in range(10):
#     totalCoordinateError += LeastSquaresOneRun()


# print("The average error in 10 measurements is " + str(totalCoordinateError/10))
