# Test image reproduction in reduced coordinates to check
# circle radius is correct

# import modules
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters, as instrucetd on the sheet
rc = 0.7
eps = 0
size = 21
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)

# set up images, source - single pixel at centre, lensed image - empty
image_s = np.zeros([size, size, 3])
image_s[int((size-1)/2), int((size-1)/2), 0] = 1
image_l = np.zeros([size, size, 3])
p_width = 2*dom/(size)  # width of each pixel

# Vectorised mapping of pixels to source plane and copying data:

# set up an array of index numbers corr. to lensed image array
i_arr = np.arange(0, size, 1)
j_arr = np.arange(0, size, 1)

# get reduced coords. r_1 and r_2 as arrays and use their grids to get s
# uses given equtions for s1 and s2
r1 = 2*dom*i_arr/(size-1) - dom
r2 = 2*dom*j_arr/(size-1) - dom
r1g, r2g = np.meshgrid(r1, r2)
s1 = r1g - ((1 - eps)*r1g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)
s2 = r2g - ((1 + eps)*r2g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)

# find which pixel they lie in in the original image for all pixels
index_1 = np.floor((s1 + dom)/p_width)
index_2 = np.floor((s2 + dom)/p_width) 
index_1 = index_1.astype(int) # change them to integers
index_2 = index_2.astype(int)

# copy the data from source image at these indexes over to lens image array
image_l[:, :, :] = image_s[index_1, index_2, :]


# start a figure and customise visuals
fig = plt.figure()
ax = fig.gca()
ax.set_xlabel(r'$x \ pixel \ index$')
ax.set_ylabel(r'$y \ pixel \ index$')
ax.set_xticks(np.arange(0, size+1, 5))
ax.set_yticks(np.arange(0, size+1, 5))
# add a scale bar:
scalebar = AnchoredSizeBar(ax.transData, 5, r'$5r_{c}$', 'lower left', pad=0.1, color='white', frameon=False)
ax.add_artist(scalebar)

# plot the resulting image onto that plot
plt.imshow(image_l)

# on top of it plot the circle of ecpected radius, changed to pixel coords.
theta = np.linspace(0, 2*np.pi, 1000)
r = np.sqrt(1-rc**2)

x = r*np.cos(theta)
y = r*np.sin(theta)

xr = (x + dom) * (size-1) / (2*dom)
yr = (y + dom) * (size-1) / (2*dom)

plt.plot(xr, yr)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
