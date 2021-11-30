# residuals between magnification map and shape distrotion map

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from skimage.measure import label, regionprops
import project.lensing_function as lensing
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up common parameters:
rc = 0.2
eps = 0
size = 101
dom = 2  # abs() of domain of r values (normally -1, 1 --> 1)

# max number of pixels to displace from centre by
disp_max = 30


# #############################################################################
# Produce map of distrotions
# #############################################################################


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

# #############################################################################
# Produce map of magnifications
# #############################################################################

# set up an image of the source, empty, then mark each pixel uniquely in RGB
image_s = np.zeros([size, size, 3])

mark_R, mark_G, mark_B = 0, 0, 0

for i in range(size):
    for j in range(size):
        image_s[i, j, :] = mark_R, mark_G, mark_B
        
        # update markers in base 256, making sure to change over
        if mark_B < 255:
            mark_B += 1
        else:
            mark_B = 0
            if mark_G < 255:
                mark_G += 1
            else:
                mark_G = 0
                mark_R += 1

# now lens this image, use the imported function
image_lensed = lensing.lens(image_s, rc, eps, dom)


# now need to count how many of each RBG combinations appear


# set up an array to store numbers of occurances of each marker
results =  np.zeros([size, size])

# set the intial checkers
cR, cG, cB = 0, 0, 0

# set up a source pixel counter, not to have to deal with base 255 too much
countx = 0
county = 0

# set up a stopping variable
stop = False

# loop over checking each RGB combination:
while stop is False:
    # find how many values appear for current RGB checks
    number = len(np.where((image_lensed[:, :, 0] == cR) & (image_lensed[:, :, 1] == cG) & (image_lensed[:, :, 2] == cB))[0])
    
    # store it in the corresponding pixel
    results[countx, county] = number
    
    # update the checkers:
    if cB < 255:
        cB += 1
    else:
        cB = 0
        if cG < 255:
            cG += 1
        else:
            cG = 0
            cR += 1
    
    # update the source pixel indexes:
    if countx < size-1:
        countx += 1
    else:
        countx = 0
        county += 1
    
    # once all pixel combinations were checked, stop the loop
    if countx == size-1 and county == size-1:
        stop=True

# cut the results array to size of ratios
results_cut = results[int((size-1)/2) - disp_max:int((size-1)/2) + disp_max, int((size-1)/2) - disp_max:int((size-1)/2) + disp_max]


# #############################################################################
# Find residuals and plot as a colour map
# #############################################################################


# normalise both results to their maximum value
ratio_arr *= 1/(np.max(ratio_arr))
results_cut *= 1/(np.max(results_cut))

# get risiduals
residuals = ratio_arr - results_cut

# plot the colour map
fig = plt.figure()
ax = fig.gca()
plt.imshow(residuals)

# plot it with pcolormesh too
fig = plt.figure()
disps = np.arange(0, disp_max*2)
disps_xg, disps_yg = np.meshgrid(disps, disps)
plot = plt.pcolormesh(disps_xg, disps_yg, residuals, cmap=cm.jet)
plt.colorbar(plot)  # set a colourbar


# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')