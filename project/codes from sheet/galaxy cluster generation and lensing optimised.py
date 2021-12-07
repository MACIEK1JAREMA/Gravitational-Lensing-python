# trying to optimise lensing a galaxy cluster

import numpy as np
import matplotlib.pyplot as plt
import project.lensing_function as lensing
from numba import jit
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.2
eps = 0
size = 2048
dom = 3  # abs() of domain of r values (normally -1, 1 --> 1)
max_a = 0.32  # maximum galaxy scale-length, in pixels
minor_max = 80  # max minor axis in pixels
gal_N = 70  # number of galaxies to generate in source image

# ############################################################################
# Generate a random galaxy cluser
# ############################################################################

# define a function that will generate image of galaxy cluster
# use numba jit to improve efficiency of used loops.
@jit(nopython=True)
def calc_image(gal_N, size, max_a, minor_max, minor_major_multiplier=5, seeded=1234):
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


# start the timer for function
start_f = timeit.default_timer()

image = calc_image(gal_N, size, max_a, minor_max, minor_major_multiplier=4, seeded=143)

# return time to run the function
stop_f = timeit.default_timer()
print('Time to generate source image was: {:.4f}'.format(stop_f - start_f) + ' s')
print('\n')

# ############################################################################
# Lens and present the  end result
# ############################################################################

# set up a figure, axis
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# set up visuals for each axis
ax1.set_aspect('equal')
ax2.set_aspect('equal')
plt.xticks([])  # take off the axis ticks for both, no need for images
plt.yticks([])
plt.sca(ax1)
plt.xticks([])
plt.yticks([])

# plot the soure image
ax1.imshow(image/255)

# plot the lensed image
image_lens = lensing.lens(image, rc, eps, dom)
ax2.imshow(image_lens/255)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')

# %%
