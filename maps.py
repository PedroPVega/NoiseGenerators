import numpy as np
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

def CreateValueMap(size, nb_poles): 
    # TODO : Simplify the nested loops
    squareSize = size // nb_poles
    hash = np.arange(nb_poles*nb_poles)
    np.random.shuffle(hash)
    hash = np.reshape(hash, (-1,nb_poles))
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

def CreatePerlinMap(size, freq, normalize):
    # create image grid 100 * 100
    imag = np.zeros((size,size), dtype = float)

    # create grid with every pseudo-random generated gradient vector
    gradientGrid = GetPermutation(freq)

    # create vector of shape 4,1 ; it will be useful later
    dotProducts = np.zeros((4,), dtype = float)
    
    # foreach point in the image x, y
    for x in range(size):
        for y in range(size):
            # get latice cell coords
            ix = x // freq
            iy = y // freq

            # get fractional part inside cell
            fx = x % freq
            fy = y % freq

            # compute the vectors to the four corners
            topLeft = [fx, fy]
            bottomLeft = [fx - freq, fy]
            bottomRight = [fx - freq, fy - freq]
            topRight = [fx, fy - freq]
            relativeVectors = np.array([topLeft, bottomLeft, bottomRight, topRight])
            relativeVectors = relativeVectors / freq

            # retreive gradient vectors from the four corners
            ix_wrap = (ix + 1) % freq
            iy_wrap = (iy + 1) % freq
            gradTopLeft = GetConstantVector(gradientGrid[ix, iy])
            gradBottomLeft = GetConstantVector(gradientGrid[ix_wrap, iy])
            gradBottomRight = GetConstantVector(gradientGrid[ix_wrap, iy_wrap])
            gradTopRight = GetConstantVector(gradientGrid[ix, iy_wrap])
            gradVectors = [gradTopLeft, gradBottomLeft, gradBottomRight, gradTopRight]

            # calculate every dot product
            for i in range(4):
                dotProducts[i] = np.dot(relativeVectors[i], gradVectors[i])

            # calculate interpolation of 4 corners with Fade
            interpol = Interpolate(Fade(fx/freq), Fade(fy/freq), dotProducts[0], dotProducts[1], dotProducts[2], dotProducts[3])

            # asign value
            imag[x, y] = interpol

    if normalize: 
        max = np.max(imag)
        min = np.min(imag)
        imag = (imag - min) / (max - min)
        
    return imag