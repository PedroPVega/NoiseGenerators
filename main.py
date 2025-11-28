from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy as np
from maps import CreateRandomMap, CreateValueMap, CreateFractalMap, CreateVoronoiMap
from ploting_utilities import ShowMap, ShowFourNoises

def GenerateFourNoises():
    start = timer()
    VoronoiNoise = CreateVoronoiMap(256, 8)
    one = timer()
    print("Elapsed time :", one - start)

    ValueNoise = CreateValueMap(256, 16)
    two = timer()
    print("Elapsed time :", two - one)

    PerlinNoise = CreateFractalMap(256, [4])
    three = timer()
    print("Elapsed time :", three - two)

    FractalNoise = CreateFractalMap(256, [2, 4, 8])
    four = timer()
    print("Elapsed time :", four - three)
    
    return [VoronoiNoise, ValueNoise, PerlinNoise, FractalNoise]


ShowFourNoises(GenerateFourNoises(), ["Voronoi noise sample", 
                                      "Value noise sample", 
                                      "Perlin noise sample", 
                                      "Fractal noise sample"])
