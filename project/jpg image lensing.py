# magnification map produced by uniquely marking each pixel in RGB

# Set working directory to respitory

# import modules
import numpy as np
import matplotlib.pyplot as plt
import project.lensing_function as lensing
from PIL import Image
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.7
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)

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
image_s = Image.open('attempts\\images\\my image M65.jpg')
image_s = np.array(image_s)
size = len(image_s[:, 0 , 0])

# plot that image on left axis
ax1.imshow(image_s)

# set up an empty array to store lensed image
image_l = np.zeros([size, size, 3])
p_width = 2*dom/(size)  # width of each pixel

# lens the image using the written in fucntion
image_l = lensing.lens(image_s, rc, eps, dom)

# correct for RGB going range 0, 1 for imshow
image_l *= 1/256

# plot the elnsed
ax2.imshow(image_l)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')