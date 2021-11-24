# generating a random galaxy cluster and lensing it 

import numpy as np
import matplotlib.pyplot as plt
import timeit
import attempts.stage3.function_lens as lensing

# %%

np.random.seed(1234)

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.7
eps = 0
dom = 10  # abs() of domain of r values (normally -1, 1 --> 1)
size = 400
max_a = 5  # maximum galaxy scale-length, in pixels
# set max minor axis in pixels
minor_max = 30

# ############################################################################
# Generate a random galaxy cluser
# ############################################################################

# choose number of galaxies to generate
gal_N = 20

# being  an empty image array, with RGB
image = np.zeros((size, size, 3))

# generate the galaxies one by one: (for now, could vectorise later)
for gal in range(gal_N):
    # randomly generate f_0 in each RGB band, make sure these are integers
    # put these in a tuple to append to the pixel
    f0r = np.random.rand() * 255
    f0g = np.random.rand() * 255
    f0b = np.random.rand() * 255
    f0 = (f0r, f0g, f0b)
    
    # randomly generate a centre pixel indexes and tuple together
    x_centr, y_centr = np.random.randint(0, size), np.random.randint(0, size)
    
    # randomly generate a, in units of pixels:
    a = np.random.randint(1, max_a)
    
    # randomly generate minor and major axis
    minor = np.random.randint(1, minor_max)
    major = np.random.randint(minor, 6*minor_max) # ensure, major is larger than minor
    
    # randomly generate angle of major axis to horizontal, in radians
    theta = np.random.rand() * np.pi
    
    # put in the centre pixel with its flux
    image[x_centr, y_centr, :] = f0
    
    # loop ver all values in square of side major
    for i in range(2*major+1):
        for j in range(2*major+1):
            # get x and y from these:
            x = -major + i
            y = -major + j
            # cehck if current point is outside the ellipse:
            if ((x*np.cos(theta) - y*np.sin(theta))/minor)**2 + ((x*np.sin(theta) + y*np.cos(theta))/major)**2 > 1:
                pass
            else:
                # its in ellipse, add its pixel data accordinly
                # careful about image edges
                try:
                    image[x_centr+i, y_centr+j, :] = tuple(flux * np.exp(-np.sqrt((((x*np.cos(theta) - y*np.sin(theta))/minor)**2 + ((x*np.sin(theta) + y*np.cos(theta))/major)**2))/a) for flux in f0)
                except IndexError:
                    pass


# plot the soure image
plt.imshow(image/255)

# ############################################################################
# Lens and present the result
# ############################################################################

image_lens = lensing.lens(image, rc, eps, dom)
plt.figure()
plt.imshow(image_lens/255)


# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')

# %%
