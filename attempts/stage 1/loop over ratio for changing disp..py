# ATtempts at looping over the area and perimeter ratios for different displacements
# Testing lensing and finding areas + permieters

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.7
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)
size = 201  # odd for test

# number of displaed pixels
disp_max = 8

# set up a list to store ratio of perimeter to area
ratio_list = []


# loop over different number of displacements
for disp in range(-disp_max, disp_max+1, 1):

    # set up an image of the source. For simplest test, a single pixel at centre
    # As for the initial test, use 21 pixels, empty apart from centre pixel
    image_s = np.zeros([size, size, 3])  # allow for RGB to start with
    image_s[int((size-1)/2), int((size-1)/2) + disp, 0] = 1
    
    # set up an empty array to store lensed image
    image_l = np.zeros([size, size, 3])
    
    # set up an array of pixel centre coordinates, in reduced
    pixels_l = np.zeros([size, size, 2])
    for i in range(size):
        for j in range(size):
            pixels_l[i, j, 0] = 2*dom*i/(size-1) - dom
            pixels_l[i, j, 1] = 2*dom*j/(size-1) - dom
    
    # loop over tracking back pixels from image_l to image_s via lens eqn
    # Inefficiently for now (initial attempts)
    for i in range(size):
        for j in range(size):
            # based on pixel position get reduced coords. r_1 and r_2
            r1 = 2*dom*i/(size-1) - dom
            r2 = 2*dom*j/(size-1) - dom
            # use lens equation to get position on image_s of this pixel
            s1 = r1 - ((1 - eps)*r1)/np.sqrt(rc**2 + (1 - eps)*r1**2 + (1 + eps)*r2**2)
            s2 = r2 - ((1 + eps)*r2)/np.sqrt(rc**2 + (1 - eps)*r1**2 + (1 + eps)*r2**2)
            # s coordinates dont have to be pixel positions in reduced
            # need to find which pixel they lie in in the original image
            # to do so, find the nearest value it maps to in pixel centres corrds.
            index_1 = (np.abs(pixels_l - s1))[:, 0, 0].argmin()  # abs in order for argmin to funciton correctly
            index_2 = (np.abs(pixels_l - s2))[0, :, 1].argmin()
            # check input of these indexes in the original image
            values = image_s[index_1, index_2, :]
            # put whatever these are into the lensed image
            image_l[i, j, :] += values
    
    # find the area of the ending lensed image in terms of pixels:
    nonzero_number = len(np.nonzero(image_l[:, :, 0]))  # only reds for now as source is only red
    
    # The area of source is one pixel.
    
    try:
        # find the perimeter of the new shape:
        image_shape = image_l[:, :, 0] != 0
        region = regionprops(image_shape.astype(int))
        perim = region[0].perimeter   # Not sure if I will use this yet, as it extrapolates by itself
        
        # find the ratio of area to perimeter of it:
        ratio = perim/nonzero_number
        
        # return that to user:
        print('Ratio of perim to area of lensed shape is {:.4f}'.format(ratio))
        
        ratio_list.append(ratio)
    except IndexError:
        # shape has been lensed completely outside of the initial image
        pass

# set up a list of all used displacement as in loop:
disps = [i for i in range(-disp_max, disp_max, 1)]

# plot the graph
fig = plt.figure()
ax = fig.gca()
ax.plot(disps, ratio_list)


# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
