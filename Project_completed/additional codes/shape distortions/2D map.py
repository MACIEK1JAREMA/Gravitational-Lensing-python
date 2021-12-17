'''

Measures distortion to shape caused by lensing by ratio of peirm/area in pixels
Does so in 2D and creates a map

@author: Maciej Tomasz Jarema ppymj11

'''

# Import modules
import numpy as np
import matplotlib.pyplot as plt
import Project_completed.modules.lensing_function as lensing
from skimage.measure import regionprops
from matplotlib.colors import LogNorm
from matplotlib import cm
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)
size = 201

# max number of pixels displacement
disp_max = 90

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
ax1 = fig.gca()

# set up visuals for axis
ax1.tick_params(labelsize=20)
ax1.set_xlabel(r'$x \ displacement \ in \ pixels$', fontsize=20)
ax1.set_ylabel(r'$y \ displacement \ in \ pixels$', fontsize=20)
ax1.set_xticks(np.arange(0, size+1, 20))
ax1.set_yticks(np.arange(0, size+1, 20))
ax1.set_aspect('equal')

# plot it on log sclae using pcolormesh, this also needs grids
disps = np.arange(-disp_max, disp_max+1)
disps_xg, disps_yg = np.meshgrid(disps, disps)
plot = ax1.pcolormesh(disps_xg, disps_yg, 1+ratio_arr, cmap=cm.jet, norm=LogNorm(1, ratio_arr.max()))
cbar = plt.colorbar(plot, fraction=0.05)
cbar.ax.tick_params(labelsize=20)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')