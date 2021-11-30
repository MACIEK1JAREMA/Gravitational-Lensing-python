# # distortions from perim/area, 2D map

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
rc = 0.2
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)
size = 201

# max number of pixels displacement
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
        
        # set up an image of the source,  a single pixel
        image_s = np.zeros([size, size, 3])
        image_s[int((size-1)/2) + disp1, int((size-1)/2) + disp2, 0] = 1
        
        # lens it using the written funciton
        image_l = lensing.lens(image_s, rc, eps, dom)
        
        # find the area of the ending lensed image in terms of pixels:
        nonzero_number = len(np.nonzero(image_l[:, :, 0]))  # only reds
        # NB The area of source is one pixel.
        
        # find the perimeteter of shape using inbuilt funciton and get ratio
        try:
            image_shape = image_l[:, :, 0] != 0
            region = regionprops(image_shape.astype(int))  # Matplab translated function
            perim = region[0].perimeter
            
            # find the ratio of area to perimeter of it and set to pixel data 
            ratio = perim/nonzero_number
            ratio_arr[i, j] = ratio
            
        except IndexError:
            # shape has been lensed completely outside of the initial image
            pass
        
        # update i:
        i += 1
    # update j
    j += 1

# set up a figure, axis
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# set up visuals for each axis
ax1.set_xlabel(r'$x \ displacement \ in \ pixels$')
ax1.set_ylabel(r'$y \ displacement \ in \ pixels$')
ax1.set_title(r'$ shape \ distortions \ map $')
ax1.set_xticks(np.arange(0, size+1, 20))
ax1.set_yticks(np.arange(0, size+1, 20))
ax1.set_aspect('equal')

ax2.set_xlabel(r'$x \ displacement \ in \ pixels$')
ax2.set_ylabel(r'$y \ displacement \ in \ pixels$')
ax2.set_title(r'$  shape \ distortions \ logarithmic \ map $')
ax2.set_xticks(np.arange(0, size+1, 20))
ax2.set_yticks(np.arange(0, size+1, 20))
ax2.set_aspect('equal')


# plot with imshow
ax1.imshow(ratio_arr)

# plot it on log sclae using pcolormesh, this also needs grids
disps = np.arange(-disp_max, disp_max+1)
disps_xg, disps_yg = np.meshgrid(disps, disps)
plot = ax2.pcolormesh(disps_xg, disps_yg, ratio_arr, cmap=cm.jet)
plt.colorbar(plot)  # set a colourbar


# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')