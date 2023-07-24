import numpy as np
from scipy.stats import norm, uniform
from matplotlib import pyplot as plt
import random
from pfilter import ParticleFilter, gaussian_noise, squared_error, independent_sample
import math



class radiationSource:

    def __init__(self, sourceX, sourceY, upperCoefficient):
        self.sourceX = sourceX
        self.sourceY = sourceY
        self.upperCoefficient = upperCoefficient


    def radCount(self, location):#location is passed as an array methinks?
        if(self.sourceX == location[0] and self.sourceY == location[1]):
            return 2000
        return self.upperCoefficient/((self.sourceX - location[0])**2 + (self.sourceY - location[1])**2)




class Drone:
    xCoord = 0
    yCoord = 0





class radiationMap:

    def __init__(self, noise, sourceOne, sourceTwo, sourceThree, sourceFour, sourceFive):
        self.noise = noise
        self.sourceList = [sourceOne, sourceTwo, sourceThree, sourceFour, sourceFive]
    
    def getTotalRadCount(self, location):
        totalRadCount = 0
        for source in self.sourceList:
            totalRadCount += source.radCount(location)
        if(self.noise):
            totalRadCount += random.random()/10000
        return totalRadCount

class Drone:
        #This is just a struct for keeping this data glued together
        xCoord = 0
        yCoord = 0

def MultiSourceRadSim():
    source1 = radiationSource(random.randint(0,10),random.randint(0,10),random.randint(1,10))
    source2 = radiationSource(random.randint(0,10),random.randint(0,10),random.randint(1,10))
    source3 = radiationSource(random.randint(0,10),random.randint(0,10),random.randint(1,10))
    source4 = radiationSource(random.randint(0,10),random.randint(0,10),random.randint(1,10))
    source5 = radiationSource(random.randint(0,10),random.randint(0,10),random.randint(1,10))
    columns = ["radCount","x", "y"]# These are the names of the columns that we use to represent the state vectors, we can change this later after the particle filter works

    prior_fn = independent_sample([uniform(loc = 0, scale = 10).rvs, uniform(loc = 0, scale = 10).rvs])
    distance = 5 #I'm just hard coding the speed of the aircraft as 5
    targetCoords = [5,5]



    def dynamics_change(x, target):
        xp = np.array(x)
        theta = math.arctan((target[1]-drone.yCoord)/(target[0]-drone.yCoord))
        xp[0] += distance*math.cos(theta)
        xp[1] += distance*math.sin(theta)
        return xp

    def observation_function(internal_state):
        internal_radCount = 0
        internal_radCount += internal_state[:,0]/((internal_state[1] - drone.xCoord)**2 + (internal_state[2] - drone.yCoord)**2)



        return internal_radCount
    

    def weight_function():




        return False
    









    placeHolderVar = 3
    radMap = radiationMap(source1, source2, source3, source4, source5)
    drone = Drone()

    pf = ParticleFilter(prior_fn = prior_fn, observe_fn= observation_function, n_particles=250, resample_proportion=0.1, column_names= columns)


    while(True):#replace this with the actual convergence criteria later
        currCoords = [drone.xCoord, drone.yCoord]
        currReading = radMap.getTotalRadCount(currCoords)
        internal_state = [[1,5,5]]

        pf.update(observed=observation_function(internal_state))
        #Now that the measurement is taken, we generate a pdf to estimate where particles are. Move and then we reestimate where the particles go


