import numpy as np
import scipy
from matplotlib import pyplot as plt


class radiationSource:

    def __init__(self, sourceX, sourceY, upperCoefficient):
        self.sourceX = sourceX
        self.sourceY = sourceY
        self.upperCoefficient = upperCoefficient


    def radCount(self, location):#location is passed as an array methinks?
        return self.upperCoefficient/((self.sourceX - location[0])**2 + (self.sourceY - location[1])**2)










class radiationMap:

    def __init__(self, sourceOne, sourceTwo, sourceThree, sourceFour, sourceFive):
        self.sourceList = [sourceOne, sourceTwo, sourceThree, sourceFour, sourceFive]
    
    def getTotalRadCount(self, location):
        totalRadCount = 0
        for source in self.sourceList:
            totalRadCount += source.radCount(location)

        return totalRadCount




