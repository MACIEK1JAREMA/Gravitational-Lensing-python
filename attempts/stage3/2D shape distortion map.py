# distortions from perim/area, 2D map

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from skimage.measure import label, regionprops
import attempts.stage3.function_lens as lensing
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
disp_max = 30

# set up an array to store ratio of perimeter to area in 2D
ratio_arr = np.zeros((2*disp_max, 2*disp_max))

# set up counters for array values to access
i, j = 0, 0

# loop over different number of displacements in both directions:
for disp1 in range(-disp_max, disp_max+1, 1):
    # reset i
    i = 0
    
    # inform user of pregress
    print('wokred out column ' + str(j) + ' out of ' + str(2*disp_max))
    for disp2 in range(-disp_max, disp_max+1, 1):
        
        # set up an image of the source. For simplest test, a single pixel
        image_s = np.zeros([size, size, 3])  # allow for RGB to start with
        image_s[int((size-1)/2) + disp1, int((size-1)/2) + disp2, 0] = 1
        # image_s[int((size-1)/2) + disp, int((size-1)/2) + disp, 0] = 1  # diagonal
        
        # lens it using the written funciton
        image_l = lensing.lens(image_s, rc, eps, dom)
        
        # find the area of the ending lensed image in terms of pixels:
        nonzero_number = len(np.nonzero(image_l[:, :, 0]))  # only reds for now as source is only red
        # NB The area of source is one pixel.
        
        try:
            # find the perimeter of the new shape:
            image_shape = image_l[:, :, 0] != 0
            region = regionprops(image_shape.astype(int))
            perim = region[0].perimeter   # Not sure if I will use this yet, as it extrapolates by itself
            
            # find the ratio of area to perimeter of it:
            ratio = perim/nonzero_number
            
            ratio_arr[i, j] = ratio
        except IndexError:
            # shape has been lensed completely outside of the initial image
            pass
        
        # update i:
        i += 1
    # update j
    j += 1

# plot the colour map
fig = plt.figure()
ax = fig.gca()
plt.imshow(ratio_arr)

# plot it with pcolormesh too
fig = plt.figure()
disps = np.arange(-disp_max, disp_max+1)
disps_xg, disps_yg = np.meshgrid(disps, disps)
plot = plt.pcolormesh(disps_xg, disps_yg, ratio_arr, cmap=cm.jet)
plt.colorbar(plot)  # set a colourbar


# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')