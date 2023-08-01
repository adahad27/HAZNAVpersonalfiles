import numpy as np
from scipy.stats import norm, uniform
from matplotlib import pyplot as plt
import random
#from pfilter import ParticleFilter, gaussian_noise, squared_error, independent_sample
import math
import particles
from particles import distributions as dists
from particles import state_space_models as ssm
from particles.collectors import Moments




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


class predictionModel(ssm.StateSpaceModel):
    def PX0(self):

        return dists.Normal()
        


    def PX(self):
        return dists.Normal()

    def PY(self):
        return dists.Normal()



def MultiSourceRadSim():
    source1 = radiationSource(random.random(),random.random(),random.randint(1,10))
    drone = Drone()

    pf = particleFilter(1, drone, source1) #The input to this is how many times you want the algorithm to be run, the drone object, and the source list which I'm currently passing in as just one object
    pf.run(2000) #The input to this is how many particles you want


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
        particles[:,0] = uniform.rvs(0,1,size = numParticles)
        particles[:,1] = uniform.rvs(0,1,size = numParticles)
        #particles is supposed to represent a numParticles x 2 array, that is basically an array of all the coordinates of all the particles that are produced
        return particles

    def graph_plotter(self, particles, sourceList):
        plt.figure(clear=True)#This clears the figure if it exists before
        

        plt.scatter(particles[:, 0], particles[:, 1])
        #plt.plot(self.flight_log[:,0], self.flight_log[:,1], c = "green")
        plt.scatter(sourceList.sourceX, sourceList.sourceY, c= "red") #Will need to make sure that internally, when sourceList is passed to this function, it is passed as an array
        plt.show()

    def allparticle_weight_average(self, particles, weights, useWeight):
        #weight is numParticles x 1 array that represents all weights
        #this also smashes multiple clusters together if they exist, so will need to make a new average later that can work with multiple particle clusters
        #one idea is similar to the kmeans clustering algorithm where particles are assigned to clusters based on how close they are to other points
        if useWeight:
            weights_to_use = np.ones(np.shape(weights))
        weights_to_use = weights
        weighted_x_average = np.sum(particles[:,0] * weights_to_use[:])/particles.size
        weighted_y_average = np.sum(particles[:,1] * weights_to_use[:])/particles.size
        self.mean_particle_location = [weighted_x_average, weighted_y_average]
    
    
    
    def weight_normalizer(self, weights):
        return weights/np.sum(weights)
    
    def particle_resampler(self, particles, weights):
        #This function is responsbile for making sure that we generate particles closer to a better guess than to a worse guess.
        #This resampler is implemented according to https://robotics.stackexchange.com/questions/479/particle-filters-how-to-do-resampling
        #The answer itself provides a lot of answers to questions that might pop up upon why this code was written the way it was

        normalized_weights = self.weight_normalizer(weights = weights)
        cumulative_sum = np.cumsum(normalized_weights)
        arr_size = normalized_weights.size

        rand_num_array = np.random.rand(arr_size) 
        #This generates an array of random numbers that is arr_size long
        rand_num_array = np.sort(rand_num_array)
        

        particle_pick_array = np.zeros(shape = (arr_size))
        #This generates an array of zeros, which is supposed to represent what particles we are picking
        #For instance the array [1,3,4] would mean that we are picking the 1st particle once, the 2nd particle 3 times, and the 3rd particle 4 times
        #The particle that is being picked is being picked from the N x 2 particles array

        
        
        i, j = 0,0
        while i < arr_size and j < arr_size:
            #We use i as the iterator for rand_num_array, and we use j as the iterator for cumulative_sum
            if rand_num_array[i] < cumulative_sum[j]:
                particle_pick_array[j] +=1
                i +=1
            else:
                j +=1 
        #at this point, particle pick array has how we're going to sample the original weight particles
        particle_array_to_return = np.zeros(shape= (arr_size,2)) # since this is the value that we're going to return, it needs to be in N x 2

        
        insert_num = 0


        #The following nested for loop is meant to take the indexes that we're supposed to copy from the particle_pick_array, and stores those particles in 
        #the particle_array_to_return array
        #The function then returns the particle_array_to return that is to be used as the new particles array
        
        i,j = 0,0
        for i in range(arr_size):
            for j in range(int(particle_pick_array[i])):
                
                particle_array_to_return[int(j+insert_num),:] = particles[i,:]
            insert_num += particle_pick_array[i]

        
        particles = particle_array_to_return
        weights = np.ones(arr_size)/arr_size
        return particles

    def source_intensity_estimator(self, currLocation,currReading,particles):
        xDiffsquared = (particles[:,0] - currLocation[0])**2 #This calculates (x0-x)^2 for every particle
        yDiffsquared = (particles[:,1] - currLocation[1])**2 #This calculates (y0-y)^2 for every particle
        intensity_array = (xDiffsquared + yDiffsquared) * currReading #Then we sum up these 2 arrays, and then we multiply the resulting array with the currReading to get estimated array for all of the sources
        return intensity_array
        

    def particle_weight(self, particles, sourceFound):
        #predictedSource is [xCoord, yCoord, naive-strength]
        initial_reading = self.source.radCount([self.drone.xCoord, self.drone.yCoord])
        initial_intensity_estimation = self.source_intensity_estimator([self.drone.xCoord, self.drone.yCoord], initial_reading, particles)
        
        #predictedSource = [0,0,0]
        #For the intensity difference idea, first we have to sample a point from the existing distribution
        particle_index = random.randint(0, np.shape(particles)[0]-1) #np.shape(particles) returns an N x 2 tuple, of which we only care about the N

        particle_of_interest = particles[particle_index,:]
        #We then store the particle that we have randomly sampled

        coordinate_change = polar_conversion([self.drone.xCoord,self.drone.yCoord], particle_of_interest, 0.5)
        self.drone.xCoord += 0.5 #coordinate_change[0]
        self.drone.yCoord += 0.5 #coordinate_change[1]

        curr_reading = self.source.radCount([self.drone.xCoord, self.drone.yCoord])
        self.flight_log = np.concatenate((self.flight_log, [[self.drone.xCoord,self.drone.yCoord, curr_reading]]))
        curr_intensity_estimation = self.source_intensity_estimator([self.drone.xCoord, self.drone.yCoord], curr_reading, particles)

        #Here we create the intensity_difference_array, and then we square the array so we don't have negative weights
        #intensity_difference_array = curr_intensity_estimation - initial_intensity_estimation
        
        # if 0 in intensity_difference_array:
        #     sourceFound = True
        #     return intensity_difference_array
        # intensity_difference_array[:] = ((intensity_difference_array[:])**2)
        # intensity_difference_array = self.weight_normalizer(intensity_difference_array)
        # intensity_difference_array = 1 - intensity_difference_array

        count_estimate = initial_intensity_estimation/((particles[:,0] - self.drone.xCoord)**2 + (particles[:,1] - self.drone.yCoord)**2)
        count_estimate -= curr_reading
        count_estimate = np.absolute(count_estimate)

        new_index = np.argmin(np.absolute(count_estimate)) #This is selecting the closest value we get to 0
        
        rangeNums = np.where(np.logical_and(count_estimate < 10 , count_estimate > -10)) #This is selecting the range of values of differences that we get that are between -10 and 10
        negativeNums = np.where(count_estimate < 0)
        zero_index = np.where(np.logical_and(count_estimate < 1, count_estimate > -1)) #Same goes for this one, except the range of values of differences has been limited
        
        
        count_estimate = self.weight_normalizer(1-self.weight_normalizer(count_estimate))
        print(np.amax(count_estimate))
        print(np.amin(count_estimate))
        # plt.scatter(particles[rangeNums, 0], particles[rangeNums,1],c = "yellow")
        # plt.scatter(particles[negativeNums,0],particles[negativeNums,1], c="green")
        # plt.scatter(particles[new_index, 0], particles[new_index, 1], c = "black")
        # plt.scatter(particles[zero_index, 0], particles[zero_index, 1], c = "cyan")
        # plt.scatter(self.source.sourceX, self.source.sourceY, c = "red")

        # ninty_above = np.where(count_estimate > 0.99)
        # eighty_above = np.where(np.logical_and(count_estimate > 0.8, count_estimate < 0.9))
        # seventy_above = np.where(np.logical_and(count_estimate > 0.7, count_estimate < 0.8))
        # sixty_above = np.where(np.logical_and(count_estimate > 0.6, count_estimate < 0.7))
        # fifty_above = np.where(np.logical_and(count_estimate > 0.5, count_estimate < 0.6))
        # print(np.size(ninty_above))
        # plt.scatter(particles[ninty_above, 0], particles[ninty_above,1], c = "yellow")
        # plt.scatter(particles[eighty_above, 0], particles[eighty_above,1], c = "green")
        # plt.scatter(particles[seventy_above, 0], particles[seventy_above,1], c = "black")
        # plt.scatter(particles[sixty_above, 0], particles[sixty_above,1], c = "cyan")
        # plt.scatter(particles[fifty_above, 0], particles[fifty_above,1], c = "magenta")
        # plt.scatter(self.source.sourceX, self.source.sourceY, c = "red")

        plt.plot(self.flight_log[:,0], self.flight_log[:,1])
        plt.show()
        return count_estimate
        #The reason why we subtract the difference from 1 is because when we do the difference, a bigger difference means that the prediction was worse,
        #and if we want to return this as a weight, then we need to make sure that the bigger value is better, hence we subtract it from 1

        #Theoretically speaking, if all goes how I'm imaging while writing this code, then intensity_difference_array 
        #Should become the weights for the particles, 


        #weights = math.sqrt((particles[:,0] - predictedSource[0])**2 + (particles[:,1] - predictedSource[1])**2) #This just does squared errors, will need to add considerations for the source intensity later as well

        #self.flight_log = np.concatenate((self.flight_log, [[self.drone.xCoord, self.drone.yCoord, curr_reading]]))
        return intensity_difference_array
    
    def run(self, particleNum):
        
        self.numRuns = 0
        
        particles = self.create_uniform_particle_distributor(numParticles=particleNum)
        # plt.scatter(particles[:,0], particles[:,1])
        
        sourceFound = False
        for i in range(self.numberRuns):
            #This is where the main loop of the particle filter is
            weights = self.particle_weight(particles, sourceFound)
            if sourceFound:
                print("WE FOUND THE SOURCE BITCHES")
                break


            particles = self.particle_resampler(particles, weights)
            self.numRuns +=1
            
            

        #self.graph_plotter(particles, self.source)
        self.allparticle_weight_average(particles, weights, False)
        # print("The actual position was (" + str(self.source.sourceX) +", " + str(self.source.sourceY)+")")
        # print("The predicted position was (" + str(self.mean_particle_location[0]) +", " + str(self.mean_particle_location[1])+")")
        




MultiSourceRadSim()

