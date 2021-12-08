# drawing a sphere function
from numba import jit
import numpy as np

@jit(nopython=True)
# define a function that will draw spherical regions around point in pixels
def draw_sphere(body_size, image_s, index, color):
    '''
    Draws a spherical body on the provided image in pixels
    Parameters:
    --------------
    body - size of body (radius) in pizels, int.
    image_s - size x size x 3 array, image will be plotted on it.
    color - tuple of size 3, gives flat RGB color of shpere.
    
    Returns:
    --------------
    image as size x size x 3 array
    
    '''
    
    # make sure given image is square:
    assert len(image_s[0, :, 0]) == len(image_s[:, 0, 0]), 'Need a square Image'
    
    # from given array get size
    size = len(image_s[0, :, 0])
    
    # loop over i and j, for a square around the object
    for i in range(2*body_size+1):
        # get x rel. to star centre and current x index
        x = -body_size + i
        ind_1 = int(size/2) - body_size + i
        for j in range(2*body_size+1):
            # get y rel. to star centre and current y index
            y = -body_size + j
            ind_2 = index - body_size + j
            # check if current point is outside the ellipse:
            if ((x/body_size)**2 + (y/body_size)**2) <= 1 and (ind_1 >= 0 and ind_1 < size) and (ind_2 >= 0 and ind_2 < size):
                image_s[ind_1, ind_2, :] = color
    
    # return the image with source drawn, to user
    return image_s



# define a function that will generate image of galaxy cluster
# use numba jit to improve efficiency of used loops.
@jit(nopython=True)
def gal_image(gal_N, size, max_a, minor_max, minor_major_multiplier=5, seeded=1234):
    '''
    Generates a pixelated image of galaxies
    
    Parameters:
    ---------------
        gal_N - int - number of galaxies
        size - int - side length of square image to create
        max_a - float - maximum decay costant for flux, in pixels
        minor_max - int - maximum semi-minor axis size, in pixels
        
    kwargs:
    ---------------
        minor_major_multiplier - int - max ratio between minor and major axis
    
    returns:
    ---------------
    image, as size x size x 3 array
    
    '''
    
    # set the seed for repeatable results
    np.random.seed(seeded)
    
    # randomly generate galaxy properties:

    # fluxes in each RGB band (inetegers), as tuple to append to the pixels
    f0r = np.random.randint(0, 255, gal_N)
    f0g = np.random.randint(0, 255, gal_N)
    f0b = np.random.randint(0, 255, gal_N)
    f0 = np.vstack((f0r, f0g, f0b))
    
    # pixel center indexes
    x_centr, y_centr = np.random.randint(0, size, gal_N), np.random.randint(0, size, gal_N)
    
    # decay a, unit = pixels:
    a = np.random.rand(gal_N) * max_a
    
    # minor axis
    minor = np.random.randint(1, minor_max+1, gal_N)
    
    # angle of major axis to horizontal (radians)
    theta = np.random.rand(gal_N) * np.pi
    
    # begin empty source image array
    image = np.zeros((size, size, 3))
    
    # precalculate costly functions for all values at once
    cosine = np.cos(theta)
    sine = np.sin(theta)
    
    # loop over generating each galaxy with these properties
    for gal in range(gal_N):
        # get major axis, here to ensure major > minor
        major = np.random.randint(minor[gal], minor_major_multiplier*minor_max)
        
        # loop ver all values in square (i and j) of side length = major
        for i in range(2*major+1):
            # get x rel. to center
            x = -major + i
            
            for j in range(2*major+1):
                # get y rel. to center
                y = -major + j
                
                # rotation transformed coordinates
                xp = x*cosine[gal] - y*sine[gal]
                yp = x*sine[gal] + y*cosine[gal]
                
                # check if current point is inside the ellipse and add its pixel data accordinly
                # careful about image edges
                if (xp/minor[gal])**2 + (yp/major)**2 <= 1 and (x_centr[gal]+i >= 0 and x_centr[gal]+i < size) and (y_centr[gal]+j >= 0 and y_centr[gal]+j < size):
                    image[x_centr[gal]+i, y_centr[gal]+j, :] += (f0[:, gal] * np.exp(-np.sqrt((xp/minor[gal])**2 + ((yp/major)**2))/a[gal]))
                    # correct for rollover:
                    for check in range(3):
                        if image[x_centr[gal]+i, y_centr[gal]+j, check] > 255:
                            image[x_centr[gal]+i, y_centr[gal]+j, check] = 255
    
    # return image to user
    return image
