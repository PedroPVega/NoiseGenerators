import matplotlib.pyplot as plt
import numpy as np
from maps import CreateRandomMap, CreateValueMap, CreatePerlinMap, CreateFractalMap
from ploting_utilities import ShowMap, ShowFourNoises

def GenerateFourNoises():
    WhiteNoise = CreateRandomMap(256)
    ValueNoise = CreateValueMap(256, 16)
    PerlinNoise = CreatePerlinMap(256, 4, True)
    FractalNoise = CreateFractalMap(256, [2, 4, 8])
    noises = [WhiteNoise, ValueNoise, PerlinNoise, FractalNoise]
    return noises

'''
ShowFourNoises(GenerateFourNoises(), ["White noise sample", 
                                      "Value noise sample", 
                                      "Perlin noise sample", 
                                      "Fractal noise sample"])
'''