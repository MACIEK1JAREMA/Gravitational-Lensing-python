# Optimised version of creating the distortions graph

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
size = 401  # odd for test

# number of displaed pixels
disp_max = 30

# set up a list to store ratio of perimeter to area
ratio_list = []


# loop over different number of displacements
for disp in range(-disp_max, disp_max+1, 1):

    # set up an image of the source. For simplest test, a single pixel at centre
    # As for the initial test, use 21 pixels, empty apart from centre pixel
    image_s = np.zeros([size, size, 3])  # allow for RGB to start with
    image_s[int((size-1)/2) + disp, int((size-1)/2) + disp, 0] = 1
    # image_s[int((size-1)/2) + disp, int((size-1)/2) + disp, 0] = 1  # diagonal
    
    # find the width of each pixel given the domain and size
    p_width = 2*dom/(size)
    
    # set up an empty array to store lensed image
    image_l = np.zeros([size, size, 3])
    
    # set up an array of index numbers in the lens image array
    i_arr = np.arange(0, size, 1)
    j_arr = np.arange(0, size, 1)
    
    # based on pixel position get reduced coords. r_1 and r_2 as arrays
    r1 = 2*dom*i_arr/(size-1) - dom
    r2 = 2*dom*j_arr/(size-1) - dom
    
    # grid them
    r1g, r2g = np.meshgrid(r1, r2)
    
    # use lens equation to get array of positions on image_s for each pixel in lens image
    s1 = r1g - ((1 - eps)*r1g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)
    s2 = r2g - ((1 + eps)*r2g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)
    
    # s coordinates dont have to be pixel positions in reduced
    # need to find which pixel they lie in in the original image for all pixels
    # therefore for all array values
    index_1 = np.floor((s1 + dom)/p_width)
    index_2 = np.floor((s2 + dom)/p_width)
    
    # change them to integers
    index_1 = index_1.astype(int).transpose()
    index_2 = index_2.astype(int).transpose()
    
    # copy the data from source image at these indexes over to lens image array
    image_l[:, :, :] = image_s[index_1, index_2, :]
    
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
disps = [i for i in range(-disp_max, disp_max+1, 1)]

# plot the graph
fig = plt.figure()
ax = fig.gca()
ax.plot(disps, ratio_list)

# set up its axis
ax.set_ylabel(r'$displacement \ from \ centre \ [pixels]$')
ax.set_xlabel(r'$\frac{image \ object \ perimeter \ [pixels]}{image \ object \ area \ [pixels]}$')


# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
