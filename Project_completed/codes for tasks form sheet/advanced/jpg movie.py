'''

Movie of a lening object moving into a jpg image

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import project.lensing_function as lensing

# %%

# set up some initial parameters
rc = 0.3
eps = 0
dom = 4  # abs() of domain of r values (normally -1, 1 --> 1)

# read in the image of the source, get it as numpy array and get its size
image = Image.open('Project_completed\\my image M65.jpg')
image = np.array(image)
sizex = len(image[:, 0, 0])
sizey = len(image[0, :, 0])

# and make certain it is a square, if not cut to size
if sizex < sizey:
    size = sizex
elif sizex > sizey:
    size = sizey
else:
    # equal, set size to whichever
    size = sizex

image = image[:size, :size, :]


# start a figure, axis and visuals
fig = plt.figure()
ax = fig.gca()
plt.sca(ax)
plt.xticks([])  # take off the axis ticks for both, no need for images
plt.yticks([])

N_step = 40

# loop over updating the offset (in pixels) and finding the lensed image
for motion in np.linspace(int(size/2), int(size), N_step):
    plt.cla()
    # restart (or set for the first time) the first frame to empty and move image in from the right
    image_s = np.zeros([size, size, 3])
    image_s[:, :int(motion), :] = image[:, size - int(motion):, :]
    
    # lens it using the lensing function
    img_lensed = lensing.lens(image_s, rc, eps, dom)
    
    # rescale rgb for imshow (0 to 255 --> 0 to 1) and plot
    img_lensed *= 1/255
    plt.imshow(img_lensed)
    
    # pause to update image
    plt.pause(0.001)
