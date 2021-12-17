'''

define some fucntions that will plot spheres and galaxies in pixels

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
import Project_completed.modules.lensing_function as lensing
import Project_completed.modules.mark_and_search_rgb as MSrgb
import timeit

# %%


# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0
eps = 0
size = 300
dom = 2  # abs() of domain of r values (eg. -1, 1 --> 1)

# set up a figure and subplot axis
fig = plt.figure(figsize=(20, 9))
fig.tight_layout()
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=None, hspace=None)

# set up visuals for each axis set
ax1.tick_params(labelsize=20)
ax1.set_xlabel(r'$x \ pixel \ index$', fontsize=20)
ax1.set_ylabel(r'$y \ pixel \ index$', fontsize=20)
ax1.set_title(r'$ image \ of \ pixels \ marked \ in \ RGB $', fontsize=20)
ax1.set_xticks(np.arange(0, size+1, int(size/5)))
ax1.set_yticks(np.arange(0, size+1, int(size/5)))
ax1.set_aspect('equal')

ax2.tick_params(labelsize=20)
ax2.set_xlabel(r'$x \ pixel \ index$', fontsize=20)
ax2.set_ylabel(r'$y \ pixel \ index$', fontsize=20)
ax2.set_title(r'$ lensed \ image \ of \ marked \ pixels $', fontsize=20)
ax2.set_xticks(np.arange(0, size+1, int(size/5)))
ax2.set_yticks(np.arange(0, size+1, int(size/5)))
ax2.set_aspect('equal')

ax3.tick_params(labelsize=20)
ax3.set_xlabel(r'$x \ pixel \ index$', fontsize=20)
ax3.set_ylabel(r'$y \ pixel \ index$', fontsize=20)
ax3.set_title(r'$ magnification \ map \ on \ log\ scale $', fontsize=20)
ax3.set_xticks(np.arange(0, size+1, int(size/5)))
ax3.set_yticks(np.arange(0, size+1, int(size/5)))
ax3.set_aspect('equal')


# set up an empty array for image, initialise rbg margers and mark each pixel uniquely
image_s = np.zeros([size, size, 3])

image_s = MSrgb.rgb_track_mark(image_s)

# plot that image and lens it, using the written function, plot the result
ax1.imshow(image_s/255)
image_lensed = lensing.lens(image_s, rc, eps, dom)
ax2.imshow(image_lensed/255)


# now need to count how many of each RBG combinations appear:
results =  np.zeros([size, size])  # array to store occurances of each marker
results = MSrgb.count_rbgs(results, image_lensed)

# for pcolormesh plot, set up x and y grids and plot it as log sclae color map
x = np.arange(0, size, 1)
y = np.arange(0, size, 1)
xg, yg = np.meshgrid(x, y)
results += 1  # avoid log(0) errors
plot = ax3.pcolormesh(xg, yg, results, cmap=cm.jet, norm=LogNorm(1, results.max()))

# set a colourbar
cbar = plt.colorbar(plot, fraction=0.05)
cbar.ax.tick_params(labelsize=20)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')