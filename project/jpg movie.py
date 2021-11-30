# jpg lensing movie
# NB set working directory to repository

# import modules
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import attempts.stage3.function_lens as lensing

# %%

# set up some initial parameters
rc = 0.3
eps = 0
dom = 4  # abs() of domain of r values (normally -1, 1 --> 1)

# read in the image of the source, get it as numpy array and get its size
image = Image.open('attempts\\images\\my image M65.jpg')
image = np.array(image)
sizex = len(image[:, 0, 0])
sizey = len(image[0, :, 0])

# and make certain it is a square
if sizex < sizey:
    size = sizex
elif sizex > sizey:
    size = sizey
else:
    # equal, set size to whichever
    size = sizex

image = image[:size, :size, :]  # cut to size

# start a figure, axis and visuals
fig = plt.figure()
ax = fig.gca()
plt.sca(ax)
plt.xticks([])  # take off the axis ticks for both, no need for images
plt.yticks([])

# loop over updating the offset (in pixels) and findgin the lensed image
for motion in range(int(size/(50*5)) + 6, int(size/(50)) + 1):
    # restart (or set for the first time) the first frame to empty and move image in from the right
    image_s = np.zeros([size, size, 3])
    image_s[:, :50*motion, :] = image[:, size - 50*motion:, :]
    
    # lens it using the lensing function
    img_lensed = lensing.lens(image_s, rc, eps, dom)
    
    # rescale rgb for imshow ( 0 to 255) and plot
    img_lensed *= 1/255
    plt.imshow(img_lensed)
    
    # pause to update image
    plt.pause(0.001)

