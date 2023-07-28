import numpy as np
from scipy.stats import norm, uniform
from matplotlib import pyplot as plt
import random
from pfilter import ParticleFilter, gaussian_noise, squared_error, independent_sample
import math




def polar_conversion(current_pos, target_pos, distance):
    xdiff = target_pos[0]-current_pos[0]
    ydiff = target_pos[1]-current_pos[1]
    theta = math.atan(ydiff/xdiff)
    
    return [distance*math.cos(theta), distance*math.sin(theta)]



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


class particle():
    def __init__(self, position, weight):
        self.position = position
        self.weight = weight
    def send(self, newPosition):
        self.position = newPosition

    def reweight(self, newWeight):
        self.weight = newWeight    




class particleFilter():
    def __init__(self, numberRuns):
        self.numberRuns = numberRuns

    def create_uniform_particle_distributor(self, numParticles):
        particles = np.empty(shape=(numParticles, 2))
        #We assume that the prediction is being done in a 10x10 m square, each square we can divide into 100 cms, so we have a total of 10*100 = 1000x1000 grid
        particles[:,0] = uniform(1000,1000,size = numParticles)
        particles[:,1] = uniform(1000,1000,size = numParticles)
        #particles is supposed to represent a numParticles x 2 array, that is basically an array of all the coordinates of all the particles that are produced
        return particles

    

    def allparticle_weight_average(self, particles, weights):
        #weight is numParticles x 1 array that represents all weights
        #this also smashes multiple clusters together if they exist, so will need to make a new average later that can work with multiple particle clusters
        #one idea is similar to the kmeans clustering algorithm where particles are assigned to clusters based on how close they are to other points

        weighted_x_average = np.sum(particles[:,0] * weights[:])/particles.size
        weighted_y_average = np.sum(particles[:,1] * weights[:])/particles.size
        self.mean_particle_location = [weighted_x_average, weighted_y_average]
    
    def particle_updater(self, particles, weights, prediction_location, distance):
        
        location_change = polar_conversion(self.mean_particle_location, prediction_location, 1)
        particles[:,0] += location_change[0]
        particles[:,1] += location_change[1]
        #have to make sure to remove a particle if it goes outside the bounding box of 10 m, but will have to replenish those particles, this is something that I'll add later
    
    def particle_weight(self, drone_location):
        
        


        

    def run(self):
        results = 0
        for i in range(self.numberRuns):
            results += 1

        return results




MultiSourceRadSim()

