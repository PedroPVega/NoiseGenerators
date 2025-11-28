import numpy as np
import time
from vectoring import Fade, Interpolate, GetPermutation, GetCornerVectors, GetRelativeVectors

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
    # create image grid 100 * 100
    imag = np.zeros((size**2,), dtype = float)

    # create grid with every pseudo-random generated gradient vector
    gradientGrid = GetPermutation(freq, seed)
    cellLength = size // freq

    # create vector of shape 4,1 ; it will be useful later
    dotProducts = np.zeros((4,), dtype = float)

    for coord in range(size**2):
        # get latice cell coords
        ix = (coord // size) // cellLength
        iy = (coord % size) // cellLength

        # get fractional part inside cell
        fx = (coord // size) % cellLength
        fy = (coord % size) % cellLength

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
        imag[coord] = interpol


    if normalize: 
        max = np.max(imag)
        min = np.min(imag)
        imag = (imag - min) / (max - min)
        
    return imag

def CreateFractalMap(size, freqs, seed = None):
    # Create image grid
    imag = np.zeros((size**2,), dtype = float)

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
    return imag.reshape(size, size)

def CreateVoronoiMap(size, freqs, seed = None):
    # set seed if chosen
    if seed: np.random.seed(seed)

    # place nuclei
    voronoi = np.zeros((size, size))
    nucleus_coords = np.zeros((freqs,freqs,2))
    number_of_cells = freqs
    size_of_cells = 256 // freqs
    for i in range(number_of_cells):
        for j in range(number_of_cells):
            x = np.random.randint(0, size_of_cells)
            y = np.random.randint(0, size_of_cells)
            nucleus_coords[i, j] = [i*size_of_cells + x, j*size_of_cells + y]
            voronoi[i*size_of_cells + x, j*size_of_cells + y] = 0

    # calculate distances to nuclei
    for x in range(size):
        for y in range(size):
            distances = np.subtract(np.array([x, y]), nucleus_coords.reshape(-1, 2))
            distances = np.multiply(distances, distances)
            distances = np.sqrt(np.sum(distances, axis = 1))
            voronoi[x, y] = np.min(distances)
    
    # normalize
    max = np.max(voronoi)
    min = np.min(voronoi)
    voronoi = (voronoi - min) / (max - min)

    return voronoi