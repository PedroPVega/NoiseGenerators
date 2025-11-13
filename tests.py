
from maps import CreateValueMap, CreatePerlinMap, CreateFractalMap
from ploting_utilities import ShowFourNoises

def TestSeedValueNoises():
    Noise1 = CreateValueMap(256, 16, seed = 12345678)
    Noise2 = CreateValueMap(256, 16, seed = 12345678)
    Noise3 = CreateValueMap(256, 16, seed = 12345678)
    Noise4 = CreateValueMap(256, 16, seed = 12345678)
    noises = [Noise1, Noise2, Noise3, Noise4]
    return noises

def TestSeedPerlinNoises():
    Noise1 = CreatePerlinMap(256, 4, normalize = True, seed = 12345678)
    Noise2 = CreatePerlinMap(256, 4, normalize = True, seed = 12345678)
    Noise3 = CreatePerlinMap(256, 4, normalize = True, seed = 12345678)
    Noise4 = CreatePerlinMap(256, 4, normalize = True, seed = 12345678)
    noises = [Noise1, Noise2, Noise3, Noise4]
    return noises

def TestSeedFractalNoises():
    Noise1 = CreateFractalMap(256, [2, 4, 8, 16], seed = 123456789)
    Noise2 = CreateFractalMap(256, [2, 4, 8, 16], seed = 123456789)
    Noise3 = CreateFractalMap(256, [2, 4, 8, 16], seed = 123456789)
    Noise4 = CreateFractalMap(256, [2, 4, 8, 16], seed = 123456789)
    noises = [Noise1, Noise2, Noise3, Noise4]
    return noises

titles = ["first", 
          "second", 
          "third", 
          "fourth"]

# ShowFourNoises(TestSeedValueNoises(), titles)
# ShowFourNoises(TestSeedPerlinNoises(), titles)
ShowFourNoises(TestSeedFractalNoises(), titles)