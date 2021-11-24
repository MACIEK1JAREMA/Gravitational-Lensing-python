# Magnification map

# import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
from PIL import Image
import timeit
import attempts.stage3.function_lens as lensing

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.7
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)
size = 200  # don;t set higher than 4096, cant mark uniquely in RGB

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

# plot that image
plt.imshow(image_s/255)

# now lens this image, use the imported function
image_lensed = lensing.lens(image_s, rc, eps, dom)

# start a new figure and plot it
plt.figure()
plt.imshow(image_lensed/255)


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


# for pcolormesh plot, set up x and y arrays:
x = np.arange(0, size, 1)
y = np.arange(0, size, 1)
xg, yg = np.meshgrid(x, y)

# now plot it as a colour map
plt.figure()
indexes = np.where(results==0)
results[indexes] = 0.01  # set 0s to 0.001 to allow for log scaling to work
plot = plt.pcolormesh(xg, yg, results, cmap=cm.jet, norm=LogNorm(0.01, results.max()))

# set a colourbar
plt.colorbar(plot)

# do the plot with imshow

plt.figure()
plt.imshow(results)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
