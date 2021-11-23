# attempt 1 at a movie with jpg image

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

# read in the image of the source
# NB set correct Working directory
# This is an image I have taken myself of M83, therefore no copyright
image = Image.open('attempts\\images\\my image M65.jpg')

# change it to a numpy array
image = np.array(image)

# from it, extract size, making sure to find the minimum (to ensure a square)
# and make certain it is a square
sizex = len(image[:, 0, 0])
sizey = len(image[0, :, 0])

if sizex < sizey:
    size = sizex
elif sizex > sizey:
    size = sizey
else:
    # equal
    size = sizex

image = image[:size, :size, :]

# start a figure window
fig = plt.figure()
ax = fig.gca()

# loop over updating the offset (in pixels)
for motion in range(int(size/(50*5)) + 6, int(size/(50)) + 1):
    # restart (or set for the first time) the first frame
    # initially, the image is all the way to the left and the whole frame is
    # black
    image_s = np.zeros([size, size, 3])
    
    # create the image by moving in the loaded image by 1 pixel to the right:
    image_s[:, :50*motion, :] = image[:, size - 50*motion:, :]
    
    # give this image to the lensing fucntion with chosen parameters
    img_lensed = lensing.lens(image_s, rc, eps, dom)
    
    # rescale its rgb for imshow (in range 0 to 1 not 0 to 255)
    img_lensed *= 1/255
    
    # plot it:
    # plt.imshow(img_lensed)
    plt.imshow(img_lensed)
    
    # pause to update
    plt.pause(0.001)

