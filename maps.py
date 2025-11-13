import numpy as np
import time
from vectoring import Fade, Lerp, Interpolate, GetPermutation, GetConstantVector

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

def CreateValueMap(size, nb_poles, seed : None): 
    # TODO : Simplify the nested loops
    squareSize = size // nb_poles
   
    hash = GetPermutation(nb_poles, seed)

    mat = np.zeros((size,size))
    for x in range(nb_poles):
        for y in range(nb_poles):
            for z in range(squareSize):
                for t in range(squareSize):
                    mat[squareSize*x + z, squareSize*y + t] = Interpolate(Fade(z / squareSize), 
                                                                          Fade(t / squareSize), 
                                                                          hash[x, y], 
                                                                          hash[(x+1)%nb_poles, y], 
                                                                          hash[(x+1)%nb_poles,(y+1)%nb_poles], 
                                                                  hash[x,(y+1)%nb_poles])
    return mat

def CreatePerlinMap(size, freq, normalize, seed : None):
    # create image grid 100 * 100
    imag = np.zeros((size,size), dtype = float)

    # create grid with every pseudo-random generated gradient vector
    gradientGrid = GetPermutation(freq, seed)
    cellLength = size // freq

    # create vector of shape 4,1 ; it will be useful later
    dotProducts = np.zeros((4,), dtype = float)
    
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
            topLeft = [fx, fy]
            bottomLeft = [fx - cellLength, fy]
            bottomRight = [fx - cellLength, fy - cellLength]
            topRight = [fx, fy - cellLength]
            relativeVectors = np.array([topLeft, bottomLeft, bottomRight, topRight])
            relativeVectors = relativeVectors / cellLength

            # retreive gradient vectors from the four corners
            ix_wrap = (ix + 1) % freq
            iy_wrap = (iy + 1) % freq
            #print(ix, iy)
            #time.sleep(0.001)
            gradTopLeft = GetConstantVector(gradientGrid[ix, iy])
            gradBottomLeft = GetConstantVector(gradientGrid[ix_wrap, iy])
            gradBottomRight = GetConstantVector(gradientGrid[ix_wrap, iy_wrap])
            gradTopRight = GetConstantVector(gradientGrid[ix, iy_wrap])
            gradVectors = [gradTopLeft, gradBottomLeft, gradBottomRight, gradTopRight]

            # calculate every dot product
            for i in range(4):
                dotProducts[i] = np.dot(relativeVectors[i], gradVectors[i])

            # calculate interpolation of 4 corners with Fade
            interpol = Interpolate(Fade(fx/cellLength), Fade(fy/cellLength), dotProducts[0], dotProducts[1], dotProducts[2], dotProducts[3])

            # asign value
            imag[x, y] = interpol

    if normalize: 
        max = np.max(imag)
        min = np.min(imag)
        imag = (imag - min) / (max - min)
        
    return imag

def CreateFractalMap(size, freqs, seed : None):
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
