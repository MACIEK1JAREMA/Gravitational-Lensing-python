'''

define some fucntions that will plot spheres and galaxies in pixels

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import Project_completed.modules.lensing_function as lensing
from PIL import Image
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up lensing parameters
rc = 0.3
eps = 0
dom = 2  # abs() of domain of r values (normally -1, 1 --> 1)

# set up a figure with subplot axis to display the result
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.set_aspect('equal')
ax2.set_aspect('equal')
plt.xticks([])  # take off the axis ticks for both, no need for images
plt.yticks([])
plt.sca(ax1)
plt.xticks([])
plt.yticks([])

# read in the image of the source as a numpy array and get its size
image_s = Image.open('Project_completed\\my image M65.jpg')
image_s = np.array(image_s)
size = len(image_s[:, 0 , 0])

# plot that image on left axis
ax1.imshow(image_s)

# set up an empty array to store lensed image and lens using function
image_l = np.zeros([size, size, 3])
image_l = lensing.lens(image_s, rc, eps, dom)

# correct for RGB going range 0, 1 for imshow and plot
image_l *= 1/256
ax2.imshow(image_l)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
