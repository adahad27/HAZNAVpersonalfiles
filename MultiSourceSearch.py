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

    prior_fn = independent_sample([uniform(loc = 50, scale = 10).rvs,uniform(loc = 0, scale = 10).rvs, uniform(loc = 0, scale = 10).rvs])
    distance = 5 #I'm just hard coding the speed of the aircraft as 5
    targetCoords = [5,5]



    def dynamics_change(x, **kwargs):
        
        return x

    def observation_function(internal_state, **kwargs):
        
        internal_radCount = 0
        internal_radCount = internal_state[:,0]/((internal_state[:,1] - drone.xCoord)**2 + (internal_state[:,2] - drone.yCoord)**2)
        return internal_radCount
        
        
    def noise_function(x, **kwargs):
        return x

        
    

    def weight_function(observed, actual_state):
        print(actual_state.shape)
        #source = radiationSource(actual_state[1], actual_state[2], actual_state[0])
        returnArray = (actual_state-observed)**2
        return returnArray


        
    










    radMap = radiationMap(True, source1, source2, source3, source4, source5)
    drone = Drone()
    particleNum = 250
    pf = ParticleFilter(
        prior_fn = prior_fn,
        n_particles=particleNum,
        dynamics_fn= dynamics_change, 
        observe_fn=observation_function,
        weight_fn= weight_function, 
        noise_fn = noise_function,
        resample_proportion=0.1, 
        column_names= columns)
    

    for i in range(100):#replace this with the actual convergence criteria later
        currCoords = [drone.xCoord, drone.yCoord]
        currReading = radMap.getTotalRadCount(currCoords)
        internal_state = np.array([[1,5,5]])
        readingArray = currReading*np.ones(particleNum)
        pf.update(observed = internal_state)
        
    #     #Now that the measurement is taken, we generate a pdf to estimate where particles are. Move and then we reestimate where the particles go
    print((pf.map_state))




MultiSourceRadSim()

