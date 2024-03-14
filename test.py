from MultiSourceSearch import radiationSource
from MultiSourceSearch import radiationMap
from MultiSourceSearch import Drone
import math
import numpy as np
from scipy.optimize import least_squares
from matplotlib import pyplot as plt
import random
from sklego.linear_model import LADRegression



"""
This is being written as it was discovered that the particle filter is able to sequentially detect
radiation sources given the intensity of a previous radiation sources. This file is to test the
idea that we can recreate the intensity of the located radiation source by making some measurements
close to it, and then using linear regression on it to calculate the approximation of the radiation
source.
"""

def NLS(beta, coordinates):
        
    return beta[0]/(((coordinates[:,0]-beta[1])**2)+ (coordinates[:,1]-beta[2])**2)

def calc_residuals(beta, coordinates):
    y_pred = NLS(beta, coordinates)
    return np.subtract(y_pred, coordinates[:,2])


def testSim():
    source1 = radiationSource(5,5,1)
    source2 = radiationSource(8,7,3)
    source3 = radiationSource(3,1,4)
    sourceList = [source1, source2, source3]

    ourRadMap = radiationMap(sourceList= sourceList)




    drone = Drone()
    simRun(ourRadMap)



def simRun(radMap):
    #Okay let's just assume that the source that we located for the first time is source1
    #Let's just get 4 readings, each within 0.5 a meter of the radiation source, and regress upon those
    reading1 = radMap.getTotalRadCount([4.5,5])
    #print(reading1)
    reading2 = radMap.getTotalRadCount([5,4.5])
    #print(reading2)
    reading3 = radMap.getTotalRadCount([5.5,5])
    #print(reading3)
    reading4 = radMap.getTotalRadCount([5,5.5])
    #print(reading4)
    #So since our formula looks like count = lambda*(k), where lambda = 1/r^2, we need to create a linear regression for that.
    #Then we manipulate our equation s.t. count/lambda = k. Since our lambda will remain constant (because we are measuring on a circle)
    # Now we have to decide how we're going to apply least squares to this.
    # So we have a constant distance, and the r^2 value should approximately be (0.5)^2 = 0.25.
    
    y = np.array([reading1, reading2, reading3, reading4])
    
    y=y*((4.5-5)**2+(5-5)**2)
    #Okay at this point, we have divided the counts by the r^2 value, and we should have a rough estimation
    #I guess we could take the median of the array? It is outlier resistant, however I'm not sure how accurate it would be. But as long as it is a rough approximation, I think that we can do something with it.
    intensity = np.median(y)
    print(y)
    print(intensity)






testSim()