import matplotlib.pyplot as plt
import numpy as np
from maps import CreateNormalizedMap
from maps import CreateRandomMap, CreateValueMap, CreatePerlinMap, CreateFractalMap

WhiteNoise = CreateRandomMap(256)
ValueNoise = CreateValueMap(256, 16)
PerlinNoise = CreatePerlinMap(256, 4, True)
FractalNoise = CreateFractalMap(256, [8, 4, 2])

f, axes = plt.subplots(2, 2)
axes[0, 0].imshow(WhiteNoise, cmap = 'gray')
axes[0, 1].imshow(ValueNoise, cmap = 'gray')
axes[1, 0].imshow(PerlinNoise, cmap = 'gray')
axes[1, 1].imshow(FractalNoise, cmap = 'gray')
plt.show()

        
def ShowMap(mat):
    image = plt.imshow(mat, cmap = 'gray')
    plt.show()
