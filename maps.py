import numpy as np
import time
from vectoring import Fade, Lerp, Interpolate, GetPermutation, GetCornerVectors, GetRelativeVectors

def CreateRandomMap(size):
    return np.random.random((size,size))

def CreateNormalizedMap():
    mat = np.zeros((256,256))
    for i in range (mat.shape[0]):
        for j in range (mat.shape[1]):
            n = np.random.randn()
            n += 1
            n /= 2
            c = int(np.round(n*256))
            mat[i,j] = c
    return mat

def CreateValueMap(size, nb_poles, seed = None): 
    squareSize = size // nb_poles
   
    hash = GetPermutation(nb_poles, seed)

    mat = np.zeros((size,size))
    
    for x in range(size):
        for y in range(size):
            ix = x // nb_poles
            iy = y // nb_poles
            z = x % squareSize
            t = y % squareSize
            mat[x, y] = Interpolate(Fade(z / squareSize), 
                                            Fade(t / squareSize), 
                                            hash[ix, iy], 
                                            hash[(ix+1)%nb_poles, iy], 
                                            hash[(ix+1)%nb_poles, (iy+1)%nb_poles], 
                                            hash[ix, (iy+1)%nb_poles])
    return mat

def CreatePerlinMap(size, freq, normalize, seed = None):
    '''
    # foreach point in the image x, y
    for x in range(size):
        for y in range(size):
            # get latice cell coords
            ix = x // cellLength
            iy = y // cellLength

            # get fractional part inside cell
            fx = x % cellLength
            fy = y % cellLength

            # compute the vectors to the four corners
            relativeVectors = GetRelativeVectors(fx, fy, cellLength)

            # retreive gradient vectors from the four corners
            ix_wrap = (ix + 1) % freq
            iy_wrap = (iy + 1) % freq 

            gradVectors = GetCornerVectors(gradientGrid, ix, ix_wrap, iy, iy_wrap)

            # calculate every dot product
            for i in range(4):
                dotProducts[i] = np.dot(relativeVectors[i], gradVectors[i])

            # calculate interpolation of 4 corners with Fade
            interpol = Interpolate(Fade(fx/cellLength), Fade(fy/cellLength), dotProducts[0], dotProducts[1], dotProducts[2], dotProducts[3])

            # asign value
            imag[x, y] = interpol
    '''
    # create image grid 100 * 100
    imag = np.zeros((size,size), dtype = float)

    # create grid with every pseudo-random generated gradient vector
    gradientGrid = GetPermutation(freq, seed)
    cellLength = size // freq

    # create vector of shape 4,1 ; it will be useful later
    dotProducts = np.zeros((4,), dtype = float)
    
    for coord in range(size**2):
        # get latice cell coords
        x = coord // size
        y = coord % size
        ix = x // cellLength
        iy = y // cellLength

        # get fractional part inside cell
        fx = x % cellLength
        fy = y % cellLength

        # compute the vectors to the four corners
        relativeVectors = GetRelativeVectors(fx, fy, cellLength)

        # retreive gradient vectors from the four corners
        ix_wrap = (ix + 1) % freq
        iy_wrap = (iy + 1) % freq 

        gradVectors = np.array(GetCornerVectors(gradientGrid, ix, ix_wrap, iy, iy_wrap))

        # calculate every dot product
        dotProducts = np.dot(relativeVectors, gradVectors.T)
        dotProducts = np.diag(dotProducts)

        # calculate interpolation of 4 corners with Fade
        interpol = Interpolate(Fade(fx/cellLength), Fade(fy/cellLength), dotProducts[0], dotProducts[1], dotProducts[2], dotProducts[3])

        # asign value
        imag[x, y] = interpol


    if normalize: 
        max = np.max(imag)
        min = np.min(imag)
        imag = (imag - min) / (max - min)
        
    return imag

def CreateFractalMap(size, freqs, seed = None):
    # Create image grid
    imag = np.zeros((size,size), dtype = float)

    # For each frequence :
    dilatation = 1
    for f in freqs:
        # Create normalized perlin map of that frequence
        perlin = CreatePerlinMap(size, f, True, seed)

        # Add the new perlin map to the grid
        imag += (1/dilatation) * perlin

        # Dilute next perlin noise
        dilatation = dilatation + 1

    # Normalize the image
    max = np.max(imag)
    min = np.min(imag)
    imag = (imag - min) / (max - min)

    return imag
