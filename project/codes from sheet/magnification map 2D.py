# Magnification map

# import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
import project.lensing_function as lensing
from numba import jit
import timeit


@jit(nopython=True)
def rgb_track_mark(image_s):
    
    assert len(image_s[:, 0, 0]) == len(image_s[0, :, 0]), 'image must be square'
    assert len(image_s[:, 0, 0]) < np.sqrt(256**3), 'Assert, image too big for uniquq marking'
    
    # get size of image
    size = len(image_s[:, 0, 0])
    
    # initialise markers
    mark_R, mark_G, mark_B = 0, 0, 0
    
    # loop over marking each pixel uniquely
    for i in range(size):
        for j in range(size):
            # set the current pixel to current free, rgb marker
            image_s[i, j, :] = mark_R, mark_G, mark_B
            
            # update markers in base 256
            if mark_B < 255:
                mark_B += 1
            else:
                mark_B = 0
                if mark_G < 255:
                    mark_G += 1
                else:
                    mark_G = 0
                    mark_R += 1
    
    # return image
    return image_s


@jit(nopython=True)
def count_rbgs(results):
    
    cR, cG, cB = 0, 0, 0  # intial checkerss
    countx = 0  # source pixel counter
    county = 0


    stop = False  # stopping variable
    
    # loop over checking each RGB combination:
    while stop is False:
        # find how many values appear for current RGB checker
        number = len(np.where((image_lensed[:, :, 0] == cR) & (image_lensed[:, :, 1] == cG) & (image_lensed[:, :, 2] == cB))[0])
        
        # store it in the corresponding pixel
        results[countx, county] = number
        
        # update the checkers as before, in base 256
        if cB < 255:
            cB += 1
        else:
            cB = 0
            if cG < 255:
                cG += 1
            else:
                cG = 0
                cR += 1
        
        # update the source pixel indicies:
        if countx < size-1:
            countx += 1
        else:
            countx = 0
            county += 1
        
        # once all pixel combinations were checked, stop the loop
        if countx == size-1 and county == size-1:
            stop = True
    
    return results


# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0
eps = 0
size = 100
dom = 3  # abs() of domain of r values (normally -1, 1 --> 1)

# set up a figure and subplot axis
fig = plt.figure(figsize=(9, 9))
fig.tight_layout()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

# set up visuals for each axis set
ax1.set_xlabel(r'$x \ pixel \ index$')
ax1.set_ylabel(r'$y \ pixel \ index$')
ax1.set_title(r'$ image \ of \ pixels \ marked \ in \ RGB $')
ax1.set_xticks(np.arange(0, size+1, 20))
ax1.set_yticks(np.arange(0, size+1, 20))
ax1.set_aspect('equal')

ax2.set_xlabel(r'$x \ pixel \ index$')
ax2.set_ylabel(r'$y \ pixel \ index$')
ax2.set_title(r'$ lensed \ image \ of \ marked \ pixels $')
ax2.set_xticks(np.arange(0, size+1, 20))
ax2.set_yticks(np.arange(0, size+1, 20))
ax2.set_aspect('equal')

ax3.set_xlabel(r'$x \ pixel \ index$')
ax3.set_ylabel(r'$y \ pixel \ index$')
ax3.set_title(r'$ magnification \ map \ on \ linear \ scale $')
ax3.set_xticks(np.arange(0, size+1, 20))
ax3.set_yticks(np.arange(0, size+1, 20))
ax3.set_aspect('equal')

ax4.set_xlabel(r'$x \ pixel \ index$')
ax4.set_ylabel(r'$y \ pixel \ index$')
ax4.set_title(r'$ magnification \ map \ on \ log\ scale $')
ax4.set_xticks(np.arange(0, size+1, 20))
ax4.set_yticks(np.arange(0, size+1, 20))
ax4.set_aspect('equal')


# set up an empty array for image, initialise rbg margers and mark each pixel uniquely
image_s = np.zeros([size, size, 3])

image_s = rgb_track_mark(image_s)

# plot that image and lens it, using the written function, plot the result
ax1.imshow(image_s/255)
image_lensed = lensing.lens(image_s, rc, eps, dom)
ax2.imshow(image_lensed/255)


# now need to count how many of each RBG combinations appear:
results =  np.zeros([size, size])  # array to store occurances of each marker
results = count_rbgs(results)

# for pcolormesh plot, set up x and y grids and plot it as log sclae color map
x = np.arange(0, size, 1)
y = np.arange(0, size, 1)
xg, yg = np.meshgrid(x, y)
results += 1  # avoid log(0) errors
plot = ax4.pcolormesh(xg, yg, results, cmap=cm.jet, norm=LogNorm(1, results.max()))

# set a colourbar
plt.colorbar(plot)

# do the plot with imshow
ax3.imshow(results)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
