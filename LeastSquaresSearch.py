import math
import numpy as np
from scipy.optimize import least_squares
import pandas as pd
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




    data = pd.read_csv(r"testfileout1.csv", index_col= "coordinates")
    #Had to put absolute path on my local computer here, this is only temporary for now.
    #r infront of a string means raw string, so no escape sequnces are used

    #row2 = data.iloc[99,99]


    class Drone:
        xCoord = 0
        yCoord = 0

    class radiationMap:
        
        def __init__(self, sourceX, sourceY, upperCoefficient):
            self.sourceX = sourceX
            self.sourceY = sourceY
            
            self.upperCoefficient = upperCoefficient
            

        def getRadCount(self, xCoord, yCoord):
            if(xCoord == self.sourceX and yCoord == self.sourceY):
                return 2000
            else:
                return self.upperCoefficient/((xCoord-self.sourceX)**2 + (yCoord-self.sourceY)**2)


    drone = Drone()
    radMap = radiationMap(sourceX = random.randint(0,10), sourceY = random.randint(0,10), upperCoefficient = random.randint(1,10))

    coordinates = np.array([[drone.xCoord, drone.yCoord, radMap.getRadCount(drone.xCoord, drone.yCoord)]])# the array should have 2 dimensions. 
    #1st column of this array contains x values, 2nd column of this array contains y values
    #we will continously have to append values to this to regress on
    # coords = np.array([[1,0,data.iloc[1,0]], [0,1,data.iloc[0,1]], [1,1,data.iloc[1,1]]])
    # coordinates = np.concatenate((coordinates, coords))
    #print(coordinates[:,0])# this returns the xCoords
    #print(coordinates[:,1])# this returns the yCoords
    # print(coordinates)
    #okay so now we have data stored in an array that is n x 3
    initial_guess = [1, 5, 5]


    currCoords = [drone.xCoord, drone.yCoord]
    previousCoords = [drone.xCoord + 1, drone.yCoord + 1]
    # results = least_squares(calc_residuals, x0 = initial_guess, args = [coordinates]) #the reason why we have to store it in square brackets here is because there is an unpacking operator, but we don't want it to unpack the coordinates array, so we wrap it in another array, so that the coordinates array is sent as is
    # print(results.x)
    # print(data.shape)
    prevResults = [0, 0, 0]
    
    while(math.sqrt((currCoords[0] - previousCoords[0])**2 + (currCoords[1] - previousCoords[1])**2) > 0.000001 ): #this is hard coded right now, we will have to change this to a tolerance value because this is the main loop
        
        if(drone.xCoord + 1 >= 10 or drone.yCoord + 1 >= 10):
            
            break
        
        
        currCoords = np.array([[drone.xCoord, drone.yCoord, radMap.getRadCount(drone.xCoord, drone.yCoord)]])
        extraIncrementArray = polarConversion(initial_guess[1], initial_guess[2],2)
        extraCoords = np.array([[drone.xCoord + extraIncrementArray[0], drone.yCoord + extraIncrementArray[1], radMap.getRadCount(drone.xCoord + extraIncrementArray[0], drone.yCoord + extraIncrementArray[1])]])
        # eastCoords = np.array([[drone.xCoord + 1, drone.yCoord, data.iloc[drone.xCoord + 1,drone.yCoord]]])
        # southCoords = np.array([[drone.xCoord, drone.yCoord + 1, data.iloc[drone.xCoord,drone.yCoord+1]]])
        # southeastCoords = np.array([[drone.xCoord + 1, drone.yCoord + 1, data.iloc[drone.xCoord,drone.yCoord+1]]])
        
        #this is creating an array of measurements to the east, south, and south east, so 4 measurements in total, I know this looks long, but I promise the thought behind it was not that complicated

        coordinates = np.concatenate((coordinates, currCoords, extraCoords)) #the argument has to be passed in as a tuple idk why, probably some interface thing to make sure that nothing is modified?

        results = least_squares(calc_residuals, x0 = initial_guess, args=[coordinates])

        #I think we should change our initital guess according to the actual values that are outputted by the least squares method, we could also try using the Levenberg-Marquardt method, but that is a later problem

        initial_guess = results.x

        incrementArray = polarConversion(results.x[1], results.x[2],2)
        
        
        
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
            currCoords = [currCoords[0] + 2*math.cos(courseAngle), currCoords[1] + 2*math.sin(courseAngle)]
        

        


    coordinateError =  math.sqrt((radMap.sourceX - results.x[1])**2 + (radMap.sourceY - results.x[2])**2)
    print("The actual source coordinates are (" + str(radMap.sourceX) +", " + str(radMap.sourceY) +") and the upper coefficient is " + str(radMap.upperCoefficient))
    print("The predicted source coordinates are (" + str(results.x[1]) + ", " + str(results.x[2]) +") and the upper coefficient is " + str(results.x[0]))



    #Below is code responsible for plotting the path in a graph
    xCoordList = coordinates[:, 0]
    yCoordList = coordinates[:, 1]

    plt.plot(xCoordList, yCoordList)
    plt.scatter(radMap.sourceX, radMap.sourceY, c= "red")
    plt.show()


    return coordinateError
    

    # plotting_csv = data.to_numpy()

    # fig, ax = plt.subplots()
    # im = ax.imshow(plotting_csv)

    # plt.colorbar(im)


    # fig.tight_layout()

    # plt.show()


totalCoordinateError = 0
print("The error in measurement for this run was " + str(LeastSquaresOneRun()))
# for i in range(10):
#     totalCoordinateError += LeastSquaresOneRun()


# print("The average error in 10 measurements is " + str(totalCoordinateError/10))
