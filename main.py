import matplotlib.pyplot as plt
import numpy as np
from maps import CreateNormalizedMap
from maps import CreateRandomMap
from maps import CreateValueMap
from maps import CreatePerlinMap

PerlinNoise = CreatePerlinMap(256, 32, True)
ValueNoise = CreateValueMap(256, 32)
WhiteNoise = CreateRandomMap(256)

f, axes = plt.subplots(1, 3)
axes[0].imshow(WhiteNoise, cmap = 'gray')
axes[1].imshow(ValueNoise, cmap = 'gray')
axes[2].imshow(PerlinNoise, cmap = 'gray')
plt.show()

        
def ShowMap(mat):
    image = plt.imshow(mat, cmap = 'gray')
    plt.show()
