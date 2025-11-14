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
    
def GetCornerVectors(grad_grid, ix, ix_wrap, iy, iy_wrap):
    gradTopLeft = GetConstantVector(grad_grid[ix, iy])
    gradBottomLeft = GetConstantVector(grad_grid[ix_wrap, iy])
    gradBottomRight = GetConstantVector(grad_grid[ix_wrap, iy_wrap])
    gradTopRight = GetConstantVector(grad_grid[ix, iy_wrap])
    return [gradTopLeft, gradBottomLeft, gradBottomRight, gradTopRight]

def GetRelativeVectors(fx, fy, cellLength):
    topLeft = [fx, fy]
    bottomLeft = [fx - cellLength, fy]
    bottomRight = [fx - cellLength, fy - cellLength]
    topRight = [fx, fy - cellLength]
    relativeVectors = np.array([topLeft, bottomLeft, bottomRight, topRight])
    return relativeVectors / cellLength
    
def GetPermutation(freq, seed):
    if seed: np.random.seed(seed)
    perm = np.arange(np.int32(freq**2))
    np.random.shuffle(perm)
    return np.reshape(perm, (freq,freq))