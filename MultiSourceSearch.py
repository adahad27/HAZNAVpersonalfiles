import numpy as np
from scipy.stats import norm, uniform
from matplotlib import pyplot as plt
import random
from sklearn.cluster import MeanShift, KMeans
import math
from LeastSquaresSearch import LeastSquaresOneRun



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
    # if(abs(distance*math.cos(theta)) > target_pos[0] or abs(distance*math.sin(theta)) > target_pos[1]):
    #     return [xdiff, ydiff]
    return [distance*math.cos(theta), distance*math.sin(theta)]

def distance(location1, location2):
    return ((location1[0] - location2[0])**2 + (location1[1] - location2[1])**2)**0.5


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

    def __init__(self, sourceList):
        # self.noise = noise
        self.sourceList = np.array(sourceList)
    def getSources(self):
        return self.sourceList
    
    def getTotalRadCount(self, location, locatedSourceList):
        totalRadCount = 0
        #return self.sourceList[1].radCount(location)
        for source in self.sourceList:
            totalRadCount += source.radCount(location)
        # for locatedSource in locatedSourceList:
        #     tempVar = locatedSource.radCount(location)
            
        #     totalRadCount -= locatedSource.radCount(location)
            
            
            
        
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
        # radSrc = radiationSource(5,5,1)

class Cell:

    def __init__(self, coordinates, dist) -> None:
        #centerCoordinates is the coordinate of the center of the square
        #dist is the horizontal distance between the center of the square, and the edge.
        self.centerCoordinate = coordinates
        self.dist = dist
        self.weight = 0
        self.visited = False

    def __eq__(self, cell):
        return self.centerCoordinate[0] == cell.centerCoordinate[0] and self.centerCoordinate[1] == cell.centerCoordinate[1] and self.dist == cell.dist and self.weight == cell.weight
    
    def inCell(self, location):
        if(abs(location[0] - self.centerCoordinate[0]) <= self.dist and abs(location[1] - self.centerCoordinate[1]) <= self.dist):
            return True
        else:
            return False
    
    def calculateWeight(self, location, droneLocation, sourceList):
        weight = 100
        """Still need to add the weighting function here."""
        return weight
    
    def addWeight(self, weight):
        self.weight += weight

class Grid:

    def __init__(self, numCells) -> None:
        self.numCells = numCells
        self.cellList = np.array([])
        x_intervals = np.linspace(0, 9, numCells)
        y_intervals = np.linspace(0, 9, numCells)
        distance = (x_intervals[1] - x_intervals[0])/2
        for x in x_intervals:
            for y in y_intervals:
                self.cellList = np.concatenate((self.cellList, np.array([Cell([x + distance, y + distance], distance)])))
    
    def addWeight(self, clusters, droneLocation, sourceList):
        for cluster in clusters:
            for cell in self.cellList:
                if cell.inCell(cluster) and cell.weight >= 0:
                    cell.addWeight(cell.calculateWeight(cluster, droneLocation, sourceList))
                    break

    def maxCell(self):
        maxWeight = 0
        maxCell = self.cellList[0]
        for cell in self.cellList:
            if cell.weight > maxWeight:
                maxWeight = cell.weight
                maxCell = cell
        return maxCell
    
    def reduceWeight(self, cell):
        
        for Cell in self.cellList:
            if(distance(cell.centerCoordinate, Cell.centerCoordinate) < 1):
                Cell.weight = -1

    def sourceWeightReduction(self, location):
        """This function basically sets any cell within 2 units of a source to have a weight of 0.
        The radius could be changed dynamically in the future, but the reason we're doing this is because
        when the algorithm is converging, a lot of the particles will be near the source location, so instead
        of having to trial and error through the clusters formed by these particles, we can just set them to 0,
        because we know it's a likely chance that they will just lead to the same source."""
        for cell in self.cellList:
            if(distance(cell.centerCoordinate, location) < 2):
                cell.weight = -1


    def allVisited(self):    
        for cell in self.cellList:
            if not cell.visited:
                return False
        return True

#These are the controls for running the particle filter under the MultiSourceRadSim() function.
#You will have to declare the particleFilter as an object before using it. 
#In the construction of the filter, you will have to pass in a drone object, and the list of sources that you want to simulate as well.
#Preferably with the list of sources being randomly generated so that a double blind simulation can be performed




def MultiSourceRadSim():
    #radiationSource(random.random() * 10 ,random.random() * 10, random.randint(1,10))
    source1 = radiationSource(5,7,30)
    source2 = radiationSource(8,5,30)
    source3 = radiationSource(2,3,40)
    

    # source1 = radiationSource(random.random() * 10, random.random() * 10, random.randint(10,100))
    # source2 = radiationSource(random.random() * 10, random.random() * 10, random.randint(10,100))
    # source3 = radiationSource(random.random() * 10, random.random() * 10, random.randint(10,100))
    
    sourceList = [source1, source2, source3]
    # source4 = radiationSource(random.random() * 10, random.random() * 10, random.randint(1,10))
    # source5 = radiationSource(random.random() * 10, random.random() * 10, random.randint(1,10))
    # sourceList = [source1, source2, source3, source4, source5]
    print([source1.sourceX, source1.sourceY, source1.upperCoefficient])
    print([source2.sourceX, source2.sourceY, source2.upperCoefficient])
    print([source3.sourceX, source3.sourceY, source3.upperCoefficient])
    ourRadMap = radiationMap(sourceList= sourceList)




    drone = Drone()

    pf = particleFilter(drone, ourRadMap) #The input to this is how many times you want the algorithm to be run, the drone object, and the source list which I'm currently passing in as just one object
    pf.run(30000) #The input to this is how many particles you want

 





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

Update 1: Sequentially locating sources has become significantly more realistic. The particle filter has to be used as a subroutine to find
a singular source, and after locating that one source, we can continue locating the other sources, using the information that we have already collected.
This means that locating multiple sources has become much more realistic, however, there is still more work to be done 
with the path planning of the drone itself to make sure that it is not running a terrible path.
Last updated this on 10/27/2023



"""













"""This is the class for the particle filter."""
class particleFilter():
    def __init__(self, drone, givenRadMap):
        
        self.drone = drone
        self.weight = np.array([])
        self.radmap = givenRadMap
        self.current_average = np.array([0,0])
        self.previous_average = np.array([0,0])
        self.restartFilter = False
        self.locatedSources = np.array([])
        self.flight_log = np.array([[drone.xCoord, drone.yCoord, self.radmap.getTotalRadCount([drone.xCoord, drone.yCoord],self.locatedSources)]])
        self.grid = Grid(10)
        self.fromClusterCell = False

    """This function is responsible for creating the particles at the start of every filtering run"""
    def create_uniform_particle_distributor(self, numParticles):
        particles = np.empty(shape=(numParticles, 2))
        
        particles[:,0] = uniform.rvs(0,10,size = numParticles)
        particles[:,1] = uniform.rvs(0,10,size = numParticles)
        return particles
        
        



    #This function is used to plot all the important stuff like the best guess, or the flight path, etc.
    def graph_plotter_clusterless(self, particles, map):      
         #Will need to make sure that internally, when sourceList is passed to this function, it is passed as an array
        plt.plot(self.flight_log[:,0], self.flight_log[:,1]) #This prints the travel path of the drone
        
        
        plt.scatter(particles[self.weight > np.median(self.weight), 0], particles[self.weight > np.median(self.weight), 1], c = "cyan")
        plt.scatter(particles[self.weight > 0.90, 0], particles[self.weight > 0.90, 1], c = "green")
        
        plt.scatter(map.getCoordArray()[:,0], map.getCoordArray()[:,1], c= "red")
        plt.show()

    def graph_plotter(self, particles, map, ms):
        plt.plot(self.flight_log[:,0], self.flight_log[:,1])
        plt.scatter(particles[self.weight > np.percentile(self.weight, 90), 0], particles[self.weight > np.percentile(self.weight, 90), 1], c = "green")
        plt.scatter(map.getCoordArray()[:,0], map.getCoordArray()[:,1], c= "red")
        plt.scatter(ms.cluster_centers_[:,0], ms.cluster_centers_[:,1], c = "black")
        plt.show()





    """This function is responsible for taking the weight of the particles and can do it based on their weight, or without their weight."""
    def allparticle_weight_average(self, particles, weights, useWeight):
        """Weight is a numParticles x 1 vector that represents all weights."""
        if not useWeight:
            weights_to_use = np.ones(np.shape(weights))/(np.shape(weights))
        else:
            weights_to_use = self.weight_normalizer(weights)
        weighted_x_average = np.sum(particles[:,0] * weights_to_use[:])
        weighted_y_average = np.sum(particles[:,1] * weights_to_use[:])
        self.mean_particle_location = [weighted_x_average, weighted_y_average]
        return np.array([weighted_x_average, weighted_y_average])










    def weight_normalizer(self, weights):
        if(weights.size !=0):
            if(np.sum(weights) == 0):
                return np.zeros(weights.size)
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
        rand_num_array = np.sort(rand_num_array)
        particle_pick_array = np.zeros(shape = (arr_size))     
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
    def particle_weight(self, particles):
        initial_reading = self.radmap.getTotalRadCount([self.drone.xCoord, self.drone.yCoord], self.locatedSources)
        #If you want to change the intensity reducer value, then change the variable below.
        reductionValue = 0.975
        
        print(initial_reading)
        """ This is to prevent negative counts from occuring when you subtract contributed counts from a source. """
        while(initial_reading < 0):
            self.locatedSources[self.locatedSources.size - 1].upperCoefficient = self.locatedSources[self.locatedSources.size - 1].upperCoefficient * reductionValue
            initial_reading = self.radmap.getTotalRadCount([self.drone.xCoord, self.drone.yCoord], self.locatedSources)
            print("we do some reducing with the initial value")
            if(self.locatedSources[self.locatedSources.size - 1].upperCoefficient < 0.0000000001):
                self.locatedSources = np.delete(self.locatedSources, self.locatedSources.size-1)
                initial_reading = self.radmap.getTotalRadCount([self.drone.xCoord, self.drone.yCoord], self.locatedSources)
                continue
        
        initial_intensity_estimation = self.source_intensity_estimator([self.drone.xCoord, self.drone.yCoord], initial_reading, particles)
        minWeight = 0.999
        """ The following if else block is responsible for determining where the drone is going to fly.
        If it has prior weights, then it does kmeans clustering to figure out where to go, and if it doesn't, 
        then it pretty much uses the heighest weight point for its estimation. """

        if(self.weight.size != 0):
            particle_of_interest = particles[np.argmax(self.weight), :]
            goodWeights = np.where(self.weight > minWeight)
            while(len(goodWeights[0]) == 0):
                minWeight-=0.001
                goodWeights = np.where(self.weight > minWeight)
            kmeans = KMeans(n_clusters=1, random_state=0,n_init="auto").fit((particles[goodWeights, :])[0])
            particle_of_interest = kmeans.cluster_centers_[0]
            if(self.locatedSources.size > 0):
                for source in self.locatedSources:
                    #If the distance between where we're aiming for and the sources is within a radius of 1.5
                    if (distance(particle_of_interest, source.returnCoords()) <= 1.5):
                        """Then we have 2 cases, one where it came from a cluster cell, and one where it did not. The only difference between the 2 cases is when we come from a cluster cell, 
                        we need to make sure that we reweight the cells in the surrounding area to have a lower weight. In both cases, we move it towards the highest weight cluster cell in our grid
                        and rerun the particle filter algo."""
                        if(self.fromClusterCell):
                            self.grid.reduceWeight(self.clusterCell)
                        self.clusterCell = self.grid.maxCell()
                        self.clusterCell.visited = True
                        self.fromClusterCell = True
                        self.drone.xCoord = self.clusterCell.centerCoordinate[0]
                        self.drone.yCoord = self.clusterCell.centerCoordinate[1]
                        self.restartFilter = True
                        self.flight_log = np.concatenate((self.flight_log, [[self.drone.xCoord,self.drone.yCoord, self.radmap.getTotalRadCount([self.drone.xCoord, self.drone.yCoord], self.locatedSources)]]))
        else:
            particle_index = random.randint(0, np.shape(particles)[0]-1) #np.shape(particles) returns an N x 2 tuple, of which we only care about the N
            particle_of_interest = particles[particle_index,:]






        
        coordinate_change = polar_conversion([self.drone.xCoord,self.drone.yCoord], particle_of_interest, 1/(math.sqrt(initial_reading)))
        self.restartFilter =  False
        self.drone.xCoord += coordinate_change[0]
        self.drone.yCoord += coordinate_change[1]
        curr_reading = self.radmap.getTotalRadCount([self.drone.xCoord, self.drone.yCoord], self.locatedSources)
        
        self.flight_log = np.concatenate((self.flight_log, [[self.drone.xCoord,self.drone.yCoord, curr_reading]]))
        """ This is estimating how much the count changes after we move the drone, and then mapping the 
        difference to a probability. """
        count_estimate = initial_intensity_estimation/((particles[:,0] - self.drone.xCoord)**2 + (particles[:,1] - self.drone.yCoord)**2)
        count_estimate -= curr_reading
        count_estimate[:] = 3*np.absolute(norm.cdf(-1*abs(count_estimate[:]), loc = 0, scale = 3))
        #This is needed for the convergence condition for the while loop in the run function
        self.previous_average = self.current_average
        self.current_average = self.allparticle_weight_average(particles, count_estimate, True)
        if(self.locatedSources.size > 0):
            for index, element in enumerate(count_estimate):
                for source in self.locatedSources:
                    if(distance(particles[index], source.returnCoords()) < 1.5):
                        count_estimate[index] = 0
        
        self.weight = count_estimate
        return count_estimate





    #The purpose of this function is that given a location of a probable source, is to take 4 measurements, and then return what it thinks the intensity value is from that.
    def located_source_estimator(self, location, offset):
        """ The location of the source will be stored in the 'location' array. All we have to do is take 4 measurements in around it, and then return the intensity off of that.
            The function also uses something called the offset, which will be used in changing how far the 4 measurements will be in distance from the source.
            Since we're also taking measurements at different locations, we will have to make sure that we update the travel log properly. """
        self.drone.xCoord = location[0] + offset
        self.drone.yCoord = location[1]
        readingOne = self.radmap.getTotalRadCount([location[0] + offset, location[1]], self.locatedSources)
        
        self.flight_log = np.concatenate((self.flight_log, [[location[0] + offset, location[1], readingOne]]))
        
        self.drone.xCoord = location[0] 
        self.drone.yCoord = location[1] + offset
        readingTwo = self.radmap.getTotalRadCount([location[0] , location[1]+ offset], self.locatedSources)
        self.flight_log = np.concatenate((self.flight_log, [[location[0] , location[1]+ offset, readingTwo]]))

        self.drone.xCoord = location[0] - offset
        self.drone.yCoord = location[1]
        readingThree = self.radmap.getTotalRadCount([location[0] - offset, location[1]], self.locatedSources)
        self.flight_log = np.concatenate((self.flight_log, [[location[0] - offset, location[1], readingThree]]))

        self.drone.xCoord = location[0] 
        self.drone.yCoord = location[1] - offset
        readingFour = self.radmap.getTotalRadCount([location[0] , location[1]- offset], self.locatedSources)
        self.flight_log = np.concatenate((self.flight_log, [[location[0] , location[1]- offset, readingFour]]))

        estimationArray = np.array([readingOne, readingTwo, readingThree, readingFour])
        estimationArray = estimationArray * ((offset)**2)
        return np.max(estimationArray)




    #This is the function that you actually use to run the filter. There is a while loop inside that runs until 
    #convergence of theh particles.
    def run(self, particleNum):
        self.numRuns = 0
        counter = 0
        while(not self.grid.allVisited()):
            counter = counter + 1
            particles = self.create_uniform_particle_distributor(numParticles=particleNum)
            
            self.current_average = self.allparticle_weight_average(particles, np.ones(shape = (particles.shape[0])) / particles.shape[0], True)
            self.weight = np.array([])
            weights = np.array([])
            #The while loop here locates a source.
            self.restartTotal = False
            while (math.sqrt((self.current_average[0] - self.previous_average[0])**2 + (self.current_average[1] - self.previous_average[1])**2) > 0.001):
                
                weights = self.particle_weight(particles)
                
                ms = MeanShift(bandwidth = 0.5)
                
                

                if(self.restartFilter):
                    self.restartTotal = True
                    break
                particles = self.particle_resampler(particles, weights)
                self.numRuns +=1
                
                if(np.sum(weights > np.percentile(weights, 99.5)) > 0):
                    ms.fit(particles[weights > np.percentile(weights, 99.5)])
                    self.grid.addWeight(ms.cluster_centers_, [self.drone.xCoord, self.drone.yCoord], self.locatedSources)
                    self.graph_plotter(particles, self.radmap, ms)
                else:
                    self.graph_plotter_clusterless(particles, self.radmap)
            


            if(self.restartTotal):
                continue
            self.drone.xCoord, self.drone.yCoord = LeastSquaresOneRun(self.radmap.getSources(), [self.drone.xCoord, self.drone.yCoord], [particles[np.argmax(self.weight), 0], particles[np.argmax(self.weight), 1]])
            
            
            """Will add a function here which reroutes to cells."""
            
            locatedSourceX, locatedSourceY = self.drone.xCoord, self.drone.yCoord
            approximatedIntensity = self.located_source_estimator([self.drone.xCoord, self.drone.yCoord], 0.5)
            # The reason why there is a -5 there, is because the last 4 locations to be added were the ones that we forced when we were flying around the source
            if(self.locatedSources.size == 0):
                self.locatedSources = np.array([radiationSource(locatedSourceX, locatedSourceY, approximatedIntensity)])
            else:
                self.locatedSources = np.concatenate((self.locatedSources, [radiationSource(locatedSourceX, locatedSourceY, approximatedIntensity)]))  
            print(approximatedIntensity)
            self.grid.sourceWeightReduction([locatedSourceX, locatedSourceY])
            self.clusterCell = self.grid.maxCell()
            self.clusterCell.visited = True
            self.fromClusterCell = True
            self.drone.xCoord = self.clusterCell.centerCoordinate[0]
            self.drone.yCoord = self.clusterCell.centerCoordinate[1]
            self.flight_log = np.concatenate((self.flight_log, [[self.drone.xCoord,self.drone.yCoord, self.radmap.getTotalRadCount([self.drone.xCoord, self.drone.yCoord], self.locatedSources)]]))
            
            self.graph_plotter_clusterless(particles, self.radmap)
            

        for source in self.locatedSources:
            print([source.sourceX, source.sourceY, source.upperCoefficient])
        
        
        


#Just calling the function once to execture the function and check how it runs.

MultiSourceRadSim()

