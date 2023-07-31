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
    def __init__(self, numberRuns, drone, source):
        self.numberRuns = numberRuns
        self.drone = drone
        self.source = source
        self.flight_log = np.array([[drone.xCoord, drone.yCoord, source.radCount([drone.xCoord, drone.yCoord])]])

    def create_uniform_particle_distributor(self, numParticles):
        particles = np.empty(shape=(numParticles, 2))
        #We assume that the prediction is being done in a 10x10 m square, each square we can divide into 100 cms, so we have a total of 10*100 = 1000x1000 grid
        particles[:,0] = uniform(1000,1000,size = numParticles)
        particles[:,1] = uniform(1000,1000,size = numParticles)
        #particles is supposed to represent a numParticles x 2 array, that is basically an array of all the coordinates of all the particles that are produced
        return particles

    def graph_plotter(self, particles, sourceList):
        plt.figure(clear=True)#This clears the figure if it exists before
        plt.scatter(particles[:, 0], particles[:, 1])
        plt.plot(self.flight_log[:,0], self.flight_log[:,1])
        plt.scatter(sourceList[:, 0], sourceList[:,1], c= "red") #Will need to make sure that internally, when sourceList is passed to this function, it is passed as an array
        plt.show()

    def allparticle_weight_average(self, particles, weights):
        #weight is numParticles x 1 array that represents all weights
        #this also smashes multiple clusters together if they exist, so will need to make a new average later that can work with multiple particle clusters
        #one idea is similar to the kmeans clustering algorithm where particles are assigned to clusters based on how close they are to other points

        weighted_x_average = np.sum(particles[:,0] * weights[:])/particles.size
        weighted_y_average = np.sum(particles[:,1] * weights[:])/particles.size
        self.mean_particle_location = [weighted_x_average, weighted_y_average]
    
    def particle_mover(self, particles, weights, prediction_location, distance):
        
        location_change = polar_conversion(self.mean_particle_location, prediction_location, 1)
        particles[:,0] += location_change[0]
        particles[:,1] += location_change[1]
        #have to make sure to remove a particle if it goes outside the bounding box of 10 m, but will have to replenish those particles, this is something that I'll add later
    
    def weight_normalizer(self, weights):
        return weights/np.sum(weights)
    
    def particle_resampler(self, particles, weights):
        #This function is responsbile for making sure that we generate particles closer to a better guess than to a worse guess.
        #This resampler is implemented according to https://robotics.stackexchange.com/questions/479/particle-filters-how-to-do-resampling
        #The answer itself provides a lot of answers to questions that might pop up upon why this code was written the way it was

        normalized_weights = self.weight_normalizer(weights = weights)
        cumulative_sum = np.cumsum(normalized_weights)
        arr_size = normalized_weights.size()
        rand_num_array = np.zeros(shape = (arr_size)) #This generates an empty array that is the size of normalized weights
        #There is perhaps an easier way of doing this where we can first sort the rand_num_array

        particle_pick_array = np.zeros(shape = (arr_size))
        for i in range(arr_size):
            rand_num_array[i] = random.random()

        rand_num_array = np.sort(rand_num_array)
        i, j = 0,0
        while i < arr_size and j < arr_size:
            #We use i as the iterator for rand_num_array, and we use j as the iterator for cumulative_sum
            if rand_num_array[i] < cumulative_sum[j]:
                particle_pick_array[j] +=1
                i +=1
            else:
                j +=1 

        


        return False

    def source_intensity_estimator(self, currLocation,currReading,particles):
        xDiffsquared = (particles[:,0] - currLocation[0])**2 #This calculates (x0-x)^2 for every particle
        yDiffsquared = (particles[:,1] - currLocation[1])**2 #This calculates (y0-y)^2 for every particle
        intensity_array = (xDiffsquared + yDiffsquared) * currReading #Then we sum up these 2 arrays, and then we multiply the resulting array with the currReading to get estimated array for all of the sources
        self.intensity_array = intensity_array
        

    def particle_weight(self, particles,predictedSource):
        #predictedSource is [xCoord, yCoord, naive-strength]
        weights = math.sqrt((particles[:,0] - predictedSource[0])**2 + (particles[:,1] - predictedSource[1])**2) #This just does squared errors, will need to add considerations for the source intensity later as well


        return weights
    
    def run(self):
        results = 0
        numRuns = 0
        
        particles = particleFilter.create_uniform_particle_distributor(250)
            

        for i in range(self.numberRuns):
            #This is where the main loop of the particle filter is
            results +=1
        return results




MultiSourceRadSim()

