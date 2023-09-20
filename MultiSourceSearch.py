import numpy as np
from scipy.stats import norm, uniform, poisson
from matplotlib import pyplot as plt
import random
from sklearn.cluster import MeanShift

import math




#The purpose of this function is to figure out what coordinates to go to if you want to travel a certain
#distance in a certain direction
def polar_conversion(current_pos, target_pos, distance):
    xdiff = target_pos[0]-current_pos[0]
    ydiff = target_pos[1]-current_pos[1]
    theta = math.atan(ydiff/xdiff)
    if xdiff < 0:
        #This was added because of the inherent limitations of using arctan() since the range of the
        #function is limited to -pi/2 to pi/2
        theta = theta + math.pi
    return [distance*math.cos(theta), distance*math.sin(theta)]



class radiationSource:

    def __init__(self, sourceX, sourceY, upperCoefficient):
        self.sourceX = sourceX
        self.sourceY = sourceY
        self.upperCoefficient = upperCoefficient


    def radCount(self, location):#location is passed as an array methinks?
        if(self.sourceX == location[0] and self.sourceY == location[1]):
            return 2000
        return (self.upperCoefficient/((self.sourceX - location[0])**2 + (self.sourceY - location[1])**2))
    
    def returnCoords(self):
        return [self.sourceX, self.sourceY]


class radiationMap:

    def __init__(self, sourceList):
        # self.noise = noise
        self.sourceList = np.array(sourceList)
    
    def getTotalRadCount(self, location):
        totalRadCount = 0
        for source in self.sourceList:
            totalRadCount += source.radCount(location)
        # if(self.noise):
        #     totalRadCount += random.random()/10000
        return totalRadCount

    def getCoordArray(self):
        narray = np.zeros(shape = (self.sourceList.size,2))
        for i in range(self.sourceList.size):
            narray[i,:] = self.sourceList[i].returnCoords()
        
        return narray
class Drone:
        #This is just a struct for keeping this data glued together
        xCoord = 0
        yCoord = 0










#These are the controls for running the particle filter under the MultiSourceRadSim() function.
#You will have to declare the particleFilter as an object before using it. 
#In the construction of the filter, you will have to pass in a drone object, and the list of sources that you want to simulate as well.
#Preferably with the list of sources being randomly generated so that a double blind simulation can be performed




def MultiSourceRadSim():
    #radiationSource(random.random() * 10 ,random.random() * 10, random.randint(1,10))
    source1 = radiationSource(5,5,1)
    source2 = radiationSource(8,7,1)
    sourceList = [source1, source2]




    source1 = radiationSource(5,6,90)
    source2 = radiationSource(1,9,20)
    source3 = radiationSource(2,7,40)
    source4 = radiationSource(6,4,70)
    source5 = radiationSource(3,8,20)


    # source1 = radiationSource(random.random() * 10, random.random() * 10, random.randint(20,60))
    # source2 = radiationSource(random.random() * 10, random.random() * 10, random.randint(20,60))
    # source3 = radiationSource(random.random() * 10, random.random() * 10, random.randint(20,60))
    # source4 = radiationSource(random.random() * 10, random.random() * 10, random.randint(20,60))
    # source5 = radiationSource(random.random() * 10, random.random() * 10, random.randint(20,60))

    sourceList = [source1, source2, source3, source4, source5]

    ourRadMap = radiationMap(sourceList= sourceList)




    drone = Drone()

    pf = particleFilter(drone, ourRadMap) #The input to this is how many times you want the algorithm to be run, the drone object, and the source list which I'm currently passing in as just one object
    pf.run(10000) #The input to this is how many particles you want

 





"""
This is a basic description on how particle filters work. This is not meant to be comprehensive description about it
but just enough to help the reader get a basic idea of how they work.
Particle Filters are used to approximate state-space systems, which a state-space system is any system whose state,
i.e. some measurements of the system that you want to measure/predict. In our case, the system is the radiation map and 
the counts associated with the distribution of the radiation sources. Typically in literature concerning the filter, you 
want to predict something called the state vector, which is pretty much just a vector of what you want to predict, so in our case
it would be something like this for single source: [xCoord of source, yCoord of source, activity of source]. Another thing of note
about our particle filter is that the state-space system we're using it in is static for the most part, i.e., the state vector that
we're trying to predict doesn't change. (Assumption on the part of the activity because this does not account for decay)

Now for how a particle filter actually works, the algorithm behind it is actually very intuitive and not too bad for complexity,
although certain literature makes it almost impossible to understand. YouTube videos on the topic are your friend, I've linked a 
few recommendations at the bottom to get your feet wet. 
The particles in the particle filter are meant to represent guesses of the state vector that are basically sprinkled about, and we rule
these guesses out with a series of measurements.

The algorithm starts out with taking a measurement, and then assigning weights to each particle/each guess based on how likely it is to be the 
state vector. A higher weight on a particle means that it is better "guess" for where the state vector is, so on for lower weights. 
If you're wondering how this ties in with the bayesian probability that is in theory, the way that works is that the weights are actually supposed
to be the probabilities themselves, the weight of a particle is the probability that it is the correct guess given the measurement we just collected,
but also all previous measurements as well. 
This is known as the prediction step(I think?)

The next part of the algorithm is something called resampling, where you systematically trim the guesses so that the particles with the lower 
weights die out, and the particles with the higher weights live on. This is done because we want the filter to converge to places where the probability
of having a source is high, and we don't want the filter to just fizzle out randomly. There is another thing to take care of here called 
sample impoverishment, which basically means that overtime, the amount of particles that you have decrease, which is something you don't want to happen.
Why you don't want this to happen is that it will mess up how the weighing works and in general, the less particles you have, the less guesses you have.
Another thing about this step is that when you do resample, when you're trimming bad guesses, you will have to replace them with something else to avoid 
sample impoverishment, and you actually just end up replacing them with good guesses. But the thing about this is that if there are no good guesses to 
start with, then the algorithm won't converge properly because there was no way to lead the particles there. 
This is known as the correction step(I think?)

Now the filter itself works by basically repeatedly applying these 2 steps to narrow down the list of guesses so that we can actually get a good guess on 
where the state vector is present. A few words about the tuning of the filter, the number of particles that you use is very very important, a high number of 
particles means we have a much much better chance of having the particles spawn on a good spot, and then from there we can reach the source, however a higher 
number also runs into the cost of having much more calculations to do.

Here are a few YouTube recommendations:
1.) Particle Filter explained without using equations: https://youtu.be/aUkBa1zMKv4
2.) Particle Filter Explained With Python Code: https://youtu.be/7Z9fEpJOJdc
3.) Particle Filter - 5 Minutes with Cyril: https://youtu.be/YBeVDxTHiYM
4.) Particle Filters | Robot Localization: https://youtu.be/ydC0mE0ZYSA
These are all great short videos to get your feet wet with particle filters if you've never dealt with them before.
If you want some more indepth explanations, then I would recommend watching other lectures by Cyril Stachniss, he is
an excellent teacher and offers invaluable insight.
I would also personally not recommend reading theory, there is a lot of notation and other jargon that can be incredibly
overwhelming if you don't actually understand what a particle filter does at a core level


There are libaries that you can potentially use to implement a particle filter if you ever wanted to implement one by yourself, however
I personally thought that the libraries over complicated what is supposed to be a simple process. However there are some good things in them that you can 
take advantage of such as offering MCMC which could be used to improve our own particle filter.
Another thing about particle filters is that I believe they will be much easier to adapt to multisource situations than regression options 
such as using least squares simply because a particle filter can have multimodal distributions, which we can use to predict where multiple sources are
simultaneously.


Last updated this on 08/03/2023



"""













#The class that defines how the particle filter will be used. The function that will be used to run the
#filter is literally called .run()
class particleFilter():
    def __init__(self, drone, sourceList):
        
        self.drone = drone
        self.weight = np.array([])
        self.sourceList = sourceList
        self.current_average = np.array([0,0])
        self.previous_average = np.array([0,0])
        self.flight_log = np.array([[drone.xCoord, drone.yCoord]])







    #This function distributes particles uniformly over the coordinate system for our initial guesses of
    #the system.
    def create_uniform_particle_distributor(self, numParticles):
        particles = np.empty(shape=(numParticles, 2))
        
        particles[:,0] = uniform.rvs(0,10,size = numParticles)
        particles[:,1] = uniform.rvs(0,10,size = numParticles)
        
        return particles
        rows = np.where(np.logical_or(np.logical_or(particles[:,0] > 6, particles[:,0] <4),np.logical_or(particles[:,1] > 6, particles[:,1] <4)))
        return particles[rows]
        
        







    #This function is used to plot all the important stuff like the best guess, or the flight path, etc.
    def graph_plotter(self, particles, map, ms, weights):      
        good_weights = np.where(weights > 0.9)
        plt.scatter(particles[good_weights][:, 0], particles[good_weights][:, 1], c = "green")
        #plt.plot(self.flight_log[:,0], self.flight_log[:,1], c = "green")
        plt.scatter(map.getCoordArray()[:,0], map.getCoordArray()[:,1], c= "red") #Will need to make sure that internally, when sourceList is passed to this function, it is passed as an array
        plt.plot(self.flight_log[:,0], self.flight_log[:,1]) #This prints the travel path of the drone
        plt.scatter(ms.cluster_centers_[:,0], ms.cluster_centers_[:,1], c = "black")
        plt.show()








    #This function calculates the average position of all the particles, and can do it based on weight or without being based on weight
    def allparticle_weight_average(self, particles, weights, useWeight):
        #weight is numParticles x 1 array that represents all weights
        #this also smashes multiple clusters together if they exist, so will need to make a new average later that can work with multiple particle clusters
        #one idea is similar to the kmeans clustering algorithm where particles are assigned to clusters based on how close they are to other points
        if useWeight:
            weights_to_use = np.ones(np.shape(weights))/(np.shape(weights))
        weights_to_use = self.weight_normalizer(weights)
        weighted_x_average = np.sum(particles[:,0] * weights_to_use[:])
        weighted_y_average = np.sum(particles[:,1] * weights_to_use[:])
        self.mean_particle_location = [weighted_x_average, weighted_y_average]
        return np.array([weighted_x_average, weighted_y_average])
    






    
    def weight_normalizer(self, weights):
        if(weights.size !=0):
            # if(np.sum(weights) == 0):
            #     print(np.amin(weights))
            #     assert False
            return abs(weights/np.sum(weights))
        return -1
    






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











    #This calculates the source activity/intensity for every guess on the board all at once.
    def source_intensity_estimator(self, currLocation,currReading,particles):
        xDiffsquared = (particles[:,0] - currLocation[0])**2 #This calculates (x0-x)^2 for every particle
        yDiffsquared = (particles[:,1] - currLocation[1])**2 #This calculates (y0-y)^2 for every particle
        intensity_array = (xDiffsquared + yDiffsquared) * currReading #Then we sum up these 2 arrays, and then we multiply the resulting array with the currReading to get estimated array for all of the sources
        return intensity_array
        









    #This function is responsible for weighing the particles and also moving the drone to places 
    def particle_weight(self, particles, initial_reading, curr_reading, initial_pos, curr_pos):
        #predictedSource is [xCoord, yCoord, naive-strength]
        #initial_reading = self.sourceList.getTotalRadCount([self.drone.xCoord, self.drone.yCoord])
        
        initial_intensity_estimation = self.source_intensity_estimator(initial_pos, initial_reading, particles)
        
        
        # if(self.weight.size != 0):
        #     #particle_of_interest = particles[np.argmax(self.weight), :]
        #     ninty_above = np.where(self.weight > 0.90)
        #     particle_of_interest = np.median(particles[ninty_above],axis = 0)
            

            
        # else:
        #     particle_index = random.randint(0, np.shape(particles)[0]-1) #np.shape(particles) returns an N x 2 tuple, of which we only care about the N
        #     particle_of_interest = particles[particle_index,:]
        #     particle_of_interest = [5,5]
        
        # # particle_of_interest = [random.random() * 10, random.random()*10]
        
        # coordinate_change = polar_conversion([self.drone.xCoord,self.drone.yCoord], particle_of_interest, 1)#/(math.sqrt(initial_reading))
        # self.drone.xCoord += coordinate_change[0]
        # self.drone.yCoord += coordinate_change[1]

        # curr_reading = self.sourceList.getTotalRadCount([self.drone.xCoord, self.drone.yCoord])
        # self.flight_log = np.concatenate((self.flight_log, [[self.drone.xCoord,self.drone.yCoord, curr_reading]]))
        
        #This is estimating how much the count changes after we move the drone, and then mapping the
        #difference to a probability.
        count_estimate = initial_intensity_estimation/((particles[:,0] - self.drone.xCoord)**2 + (particles[:,1] - self.drone.yCoord)**2)
        #count_estimate[:] = poisson.pmf(initial_intensity_estimation[:],curr_reading)

        count_estimate -= curr_reading
        count_estimate[:] = count_estimate[:]
        count_estimate[:] = 2*np.absolute(norm.cdf(-1*abs(count_estimate[:]), loc = 0, scale = 30))



        #This is needed for the convergence condition for the while loop in the run function
        self.previous_average = self.current_average
        # print(np.sum(count_estimate))
        self.current_average = self.allparticle_weight_average(particles, count_estimate, True)
        # print(type(self.previous_average))
        # print(type(self.current_average))
        self.weight = count_estimate



        return count_estimate
            


    def move(self, isFixed ,list):
        
        #This is where we put in fixed path planning, maybe have something where we can try patterns, but I can't imagine we'll do something other than spirals
        if isFixed:
            move_coordinates_list = np.array(list)
            
            #So we have 2 possible ideas, the first coordinate could be (0,0) or the first coordinate could be the actual coordinate
            #Let's just have it start with (0,0)
            initial_intensity = self.sourceList.getTotalRadCount([self.drone.xCoord, self.drone.yCoord])
            initial_pos = [self.drone.xCoord, self.drone.yCoord]

            

            curr_intensity = self.sourceList.getTotalRadCount(move_coordinates_list[self.numRuns+1, :])
            self.drone.xCoord = move_coordinates_list[self.numRuns, 0]
            self.drone.yCoord = move_coordinates_list[self.numRuns, 1]
            curr_pos = [self.drone.xCoord, self.drone.yCoord]
            self.flight_log = np.concatenate((self.flight_log, [[self.drone.xCoord,self.drone.yCoord]]))

            return initial_intensity, curr_intensity, initial_pos, curr_pos
        
        #We can implement dynamic planning here
        else:


            return False



















    #This is the function that you actually use to run the filter. There is a while loop inside that runs until 
    #convergence of theh particles.
    def run(self, particleNum):
        
        self.numRuns = 0
        
        particles = self.create_uniform_particle_distributor(numParticles=particleNum)
        
        ms = MeanShift(bandwidth=0.5)
        
        # The main loop runs until the difference in the averages of the particles converge to a position.
        # We can then return the average as we know that the position returned is our best guess for 
        # where the source(s) is located.
        self.current_average = self.allparticle_weight_average(particles, np.ones(shape = (particles.shape[0])) / particles.shape[0], True)
        # print(self.current_average)
        # print(self.previous_average)
        
        while (True):#math.sqrt((self.current_average[0] - self.previous_average[0])**2 + (self.current_average[1] - self.previous_average[1])**2) > 0.001
            ourList = [#These are the coordinates that I drew out to draw the spiral
                    [2,2],
                    [5,2],
                    [8,2],
                    [8,5],
                    [8,8],
                    [5,8],
                    [3,8],
                    [3,6],
                    [3,3],
                    [6,3],
                    [6,7],
                    [5,7],
                    [5,5]
                    ]
            initial_reading, curr_reading, initial_pos, curr_pos = self.move(True, list=ourList)
            weights = self.particle_weight(particles, initial_reading, curr_reading, initial_pos, curr_pos)

            particles = self.particle_resampler(particles, weights)
            self.numRuns +=1
            
            
            if(self.numRuns == 4):
                good_weights = np.where(weights > 0.90)

                #print(type(good_weights))
                #print((particles[good_weights, :])[0])
                ms.fit((particles[good_weights, :])[0])
                
                # #cluster_centers = ms.cluster_centers_
                # #print(cluster_centers.size)
                # plt.scatter(particles[good_weights,0], particles[good_weights,1])
                


                # ninty_above = np.where(weights > 0.90)
                # eighty_above = np.where(np.logical_and(weights > 0.8, weights < 0.9))
                # seventy_above = np.where(np.logical_and(weights > 0.7, weights < 0.8))
                # sixty_above = np.where(np.logical_and(weights > 0.6, weights < 0.7))
                # fifty_above = np.where(np.logical_and(weights > 0.5, weights < 0.6))
                
                # plt.scatter(particles[ninty_above, 0], particles[ninty_above,1], c = "cyan")
                # plt.scatter(particles[eighty_above, 0], particles[eighty_above,1], c = "yellow")
                # # plt.scatter(particles[seventy_above, 0], particles[seventy_above,1], c = "black")
                # # plt.scatter(particles[sixty_above, 0], particles[sixty_above,1], c = "green")
                # # plt.scatter(particles[fifty_above, 0], particles[fifty_above,1], c = "magenta")
                break
            
            
        self.graph_plotter(particles, self.sourceList, ms, weights)
        
        
        # print("The actual position was (" + str(self.source.sourceX) +", " + str(self.source.sourceY)+")")
        # print("The predicted position was (" + str(self.mean_particle_location[0]) +", " + str(self.mean_particle_location[1])+")")
        # print("The algorithm converged in " + str(self.numRuns) + " steps")
        


























#Just calling the function once to execture the function and check how it runs.

MultiSourceRadSim()

