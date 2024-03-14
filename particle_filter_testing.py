from scipy.stats import uniform, norm, poisson
import numpy as np
from matplotlib import pyplot as plt
import random
from sklearn.cluster import MeanShift
import math


# while (abs(self.unweighted_average - self.previous_unweighted_average) < 0.001):
#     break



list = [
[2,2],
[5,2],
[8,2],
[8,5],
[8,8],
[8,5],
[3,8],
[3,6],
[3,3],
[6,3],
[6,7],
[5,7],
[5,5]

]

ms = MeanShift()

ms.fit(list)

print(ms.cluster_centers_)
plt.scatter(ms.cluster_centers_[:,0], ms.cluster_centers_[:,1])
plt.show()
