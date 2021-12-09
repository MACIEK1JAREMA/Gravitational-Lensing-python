# trying to optimise lensing a galaxy cluster

import numpy as np
import matplotlib.pyplot as plt
import project.lensing_function as lensing
import project.codes_physical.functions.draw_sphere as pix_draw
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
# Generate a random galaxy cluser, lens and plot
# ############################################################################

# start the timer for function
start_f = timeit.default_timer()

image = pix_draw.gal_image(gal_N, size, max_a, minor_max, minor_major_multiplier=4, seeded=143)

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
