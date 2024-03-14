import math
import numpy as np
from scipy.optimize import least_squares
#import pandas as pd
from matplotlib import pyplot as plt
import random

"""
This is a basic description of how the Least Squares method has been implemented in this python file. 
Least Squares is a regression based model, what that means is that it tries to fit data points to a predefined model that we can set ourselves.
Given data points, it tries finding the equation that minimizes the squares of the distance in between the data points and the points modeled
by the equation.
For this specific application we're using Non-Linear Least Squares, because the function that we're trying to regress on has a combination of vectors that 
is non linear. If the reader is trying to figure out why we can use linear LS for polynomials but not for the model we have for radiation counts, the reason
for that is because polynomials are actually linear combinations of vectors, where the vectors are the x^n terms where n is an element of the whole numbers.
Since we have K/((x-x0)^2+(y-y0)^2), the vectors themselves that is the x and y terms are not in linear combinations.

The way LS has been integrated in this program is by predicting where the source is from a singular data point, then travelling partially to where our prediction
is, remeasuring, and then recalculating where the source is. We keep repeating this until the difference in between the prediction of sources is less than a 
certain threshold value. At that point, we will know that we have reached the source, or at least a good approximation of where the source is. 
One problem that I think that LS has that it doesn't feel like it's the most noise resistant, when I have tested it with noise, sometimes it sent the drone off 
in a random direction, however that wasn't too often, more often than not, it converged to a location slightly off the source, but still narrowed it down pretty good.
Will have to test this more with noise to see how much effect noise has on LS.

I still have to test this with multiple sources, but dependent on how noise resistant LS is, we could potentially use this in multisource.


Will update this if I think of anything more to add
Last updated on 08/05/2023

"""
def LeastSquaresOneRun(SourceList, starting_pos, prediction, travel_log, step_size, distance_covered, steps_taken):    

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

    def polarConversion(current_pos, target_pos, distance):
        xdiff = target_pos[0]-current_pos[0]
        ydiff = target_pos[1]-current_pos[1]
        theta = math.atan(ydiff/xdiff)
        if xdiff < 0:
            #This was added because of the inherent limitations of using arctan() since the range of the
            #function is limited to -pi/2 to pi/2
            theta = theta + math.pi
        # if(abs(distance*math.cos(theta)) > target_pos[0] or abs(distance*math.sin(theta)) > target_pos[1]):
        #     return [xdiff, ydiff]
        return [distance*math.cos(theta), distance*math.sin(theta)]


    class Drone:
        #This is just a struct for keeping this data glued together
        xCoord = starting_pos[0]
        yCoord = starting_pos[1]

    class radiationSource:

        def __init__(self, sourceX, sourceY, upperCoefficient):
            self.sourceX = sourceX
            self.sourceY = sourceY
            self.upperCoefficient = upperCoefficient


        def radCount(self, location):#location is passed as an array methinks?
            if(self.sourceX == location[0] and self.sourceY == location[1]):
                
                return 2000
            return (self.upperCoefficient/((self.sourceX - location[0])**2 + (self.sourceY - location[1])**2))
        
        def setIntensity(self, newIntensity):
            self.upperCoefficient = newIntensity

        def getIntensity(self):
            return self.upperCoefficient

        def intensityReducer(self, reduction):
            self.upperCoefficient = self.upperCoefficient * reduction

        def returnCoords(self):
            return [self.sourceX, self.sourceY]

    class radiationMap:
        #This map is meant to model the map of radiation, it returns radiation count based on position from the source
        # def __init__(self, sourceList):
        #     # self.noise = noise
        #     self.sourceList = np.array(sourceList)
        def __init__(self, sourceList, noise):
            self.sourceX = sourceList[0].sourceX
            self.sourceY = sourceList[0].sourceY
            self.upperCoefficient = sourceList[0].upperCoefficient
            self.sourceList = sourceList
            # self.source = radiationSource(sourceX, sourceY, upperCoefficient)
            self.noise = noise

        

        def getTotalRadCount(self, xCoord, yCoord):
            totalRadCount = 0
            for source in self.sourceList:
                totalRadCount += source.radCount([xCoord, yCoord])
            return totalRadCount



        # def getTotalRadCount(self, xCoord, yCoord):
        #     return self.source.radCount([xCoord, yCoord])

            

        
    # source1 = radiationSource(2, 2, 40)
    # source2 = radiationSource(1, 5, 90)
    # source3 = radiationSource(9, 9, 100)
    # sourceList = [source1, source2, source3]

    drone = Drone()
    #random.randint(0,10)
    # radMap = radiationMap(sourceX = 9 , sourceY = 7, upperCoefficient = 1, noise = False)
    radMap = radiationMap(sourceList=SourceList, noise = False)
    
    coordinates = np.array([[drone.xCoord, drone.yCoord, radMap.getTotalRadCount(drone.xCoord, drone.yCoord)]])# the array should have 2 dimensions. 
    
    initial_guess = [1, prediction[0], prediction[1]]


    currCoords = [drone.xCoord, drone.yCoord]
    previousCoords = [drone.xCoord + 1, drone.yCoord + 1]
    
    # prevRes = [0, starting_pos[0], starting_pos[1]]
    prevRes = [0, 0, 0]

    # travel_log = np.array([[prediction[0],prediction[1]]]) #Replace (0,0) with the start position of the drone if it isn't (0,0)
    # travel_log = np.array([[starting_pos[0], starting_pos[1]]])
    travel_log = np.concatenate((travel_log, [[starting_pos[0],starting_pos[1], radMap.getTotalRadCount(starting_pos[0], starting_pos[1]) ]]))
    steps_taken += 1
    result_log = np.array([initial_guess])

    debugSum = 0
    while(math.sqrt((initial_guess[1] - prevRes[0])**2 + (initial_guess[2] - prevRes[1])**2) > 0.000001 ): #this is hard coded right now, we will have to change this to a tolerance value because this is the main loop
        debugSum += math.sqrt((initial_guess[1] - prevRes[0])**2 + (initial_guess[2] - prevRes[1])**2)
        if(debugSum > 60):
            #This is meant to prevent infinite loops from happening, the value of debugSum can be changed depending on testing data
            break
        if(drone.xCoord > 10 or drone.yCoord > 10 or drone.xCoord < -1 or drone.yCoord < -1):
            
            break
        initial_reading = radMap.getTotalRadCount(drone.xCoord, drone.yCoord)
        
        currCoords = np.array([[drone.xCoord, drone.yCoord, initial_reading]])
        extraIncrementArray = polarConversion([drone.xCoord, drone.yCoord],[initial_guess[1], initial_guess[2]],step_size(initial_reading))
        distance_covered += step_size(initial_reading)
        extraCoords = np.array([[drone.xCoord + extraIncrementArray[0], drone.yCoord + extraIncrementArray[1], radMap.getTotalRadCount(drone.xCoord + extraIncrementArray[0], drone.yCoord + extraIncrementArray[1])]])
        
        coordinates = np.concatenate((coordinates, currCoords, extraCoords)) #the argument has to be passed in as a tuple idk why, probably some interface thing to make sure that nothing is modified?

        results = least_squares(calc_residuals, x0 = initial_guess, args=[coordinates])

        #I think we should change our initital guess according to the actual values that are outputted by the least squares method, we could also try using the Levenberg-Marquardt method, but that is a later problem
        prevRes = initial_guess
        initial_guess = results.x

        incrementArray = polarConversion([drone.xCoord, drone.yCoord],[results.x[1], results.x[2]],0.5)
        
        distance_covered += 0.5
        
        previousCoords = [drone.xCoord, drone.yCoord]
        drone.xCoord += incrementArray[0]
        drone.yCoord += incrementArray[1]

        currCoords = [drone.xCoord, drone.yCoord]
        # if(radMap.getTotalRadCount(currCoords[0], currCoords[1]) < radMap.getTotalRadCount(previousCoords[0], previousCoords[1])):
        #     #then we make it go in the opposite direction
        #     #print("SPECIAL CASE HAS BEEN REACHED AND HOPEFULLY THIS WORKS")
        #     courseAngle = math.atan((previousCoords[1]-currCoords[1])/(previousCoords[0]-currCoords[0])) + math.pi
        #     currCoords = previousCoords
        #     #CHANGE THE 2 HERE ACCORDING TO DISTANCE IN POLARCONVERSION, WAS TOO LAZY TO FIGURE OUT ANOTHER WAY OF DOING THIS
        #     currCoords = [currCoords[0] + 0.5*math.cos(courseAngle), currCoords[1] + 0.5*math.sin(courseAngle)]
        
        
        #This just updates the respective logs needed in case of testing/debugging
        travel_log = np.concatenate((travel_log, [[currCoords[0],currCoords[1], radMap.getTotalRadCount(currCoords[0], currCoords[1]) ]]))
        steps_taken += 1
        result_log = np.concatenate((result_log, [results.x]))

        

    currCoords = [results.x[1], results.x[2]]
    # travel_log = np.concatenate((travel_log, [currCoords]))
    travel_log = np.concatenate((travel_log, [[currCoords[0],currCoords[1], radMap.getTotalRadCount(currCoords[0], currCoords[1]) ]]))
    steps_taken += 1
    coordinateError =  math.sqrt((radMap.sourceX - results.x[1])**2 + (radMap.sourceY - results.x[2])**2)
    print("The actual source coordinates are (" + str(radMap.sourceX) +", " + str(radMap.sourceY) +") and the upper coefficient is " + str(radMap.upperCoefficient))
    print("The predicted source coordinates are (" + str(results.x[1]) + ", " + str(results.x[2]) +") and the upper coefficient is " + str(results.x[0]))

    # print(travel_log)
    # print(result_log)
    #Below is code responsible for plotting the path in a graph
    xCoordList = travel_log[:, 0]
    yCoordList = travel_log[:, 1]

    # plt.plot(xCoordList, yCoordList, color = 'blue')
    # plt.scatter(radMap.sourceX, radMap.sourceY, c= "red")
    # plt.show()


    return [results.x[1], results.x[2], results.x[0], travel_log, distance_covered, steps_taken]


# totalCoordinateError = 0
# print("The error in measurement for this run was " + str(LeastSquaresOneRun()))
# for i in range(10):
#     totalCoordinateError += LeastSquaresOneRun()


# print("The average error in 10 measurements is " + str(totalCoordinateError/10))
