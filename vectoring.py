import numpy as np


def Fade(t):
    return t**3 * (10 + t * (6 * t - 15))

def Lerp(t, a, b):
    return (b - a) * t + a

def Interpolate(u, v, upleft, downleft, downright, upright):
    return Lerp(u, Lerp(v, upleft, upright), Lerp(v, downleft, downright))

def GetConstantVector(index):
    pull = index % 4
    if pull == 0:
        return [1, 1]
    elif pull == 1:
        return [-1, 1]
    elif pull == 2:
        return [-1, -1]
    else:
        return [1, -1]
    
def GetPermutation(freq):
    perm = np.arange(np.int32(freq**2))
    np.random.shuffle(perm)
    return np.reshape(perm, (freq,freq))