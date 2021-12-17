'''

test the case RGB marking and searching through a simple operation

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import Project_completed.modules.mark_and_search_rgb as MSrgb
import timeit

# %%

# start the timer
start = timeit.default_timer()


# define a small RGB image:
size = 5
img_test = np.zeros((size, size, 3))


# mark it with RGB
img_test = MSrgb.rgb_track_mark(img_test)

# perform a simple operation:
# copy column 2 to column 4 and keep a copy of it still at 2:
img_test[:, 3, :] = img_test[:, 1, :]

# Perform RGB search
results =  np.zeros([size, size])  # array to store occurances of each marker
results = MSrgb.count_rbgs(results, img_test)

# set up the figure and plot test and result images:

# plot it using imshow:
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.tick_params(labelsize=20)
ax1.set_xticks(np.arange(0, size+1, int(size/5)))
ax1.set_yticks(np.arange(0, size+1, int(size/5)))
ax1.set_xlabel(r'$x \ pixel \ index$', fontsize=20)
ax1.set_ylabel(r'$y \ pixel \ index$', fontsize=20)

ax2.tick_params(labelsize=20)
ax2.set_xticks(np.arange(0, size+1, int(size/5)))
ax2.set_yticks(np.arange(0, size+1, int(size/5)))
ax2.set_xlabel(r'$x \ pixel \ index$', fontsize=20)
ax2.set_ylabel(r'$y \ pixel \ index$', fontsize=20)

# plot test image
ax1.imshow(img_test/size**2)

# plot result with labels for size
x = np.arange(0, size+1, 1)
y = np.arange(0, size+1, 1)
xg, yg = np.meshgrid(x, y)
plot = ax2.pcolormesh(xg, yg, results, cmap=cm.jet)

# set a colourbar
cbar = plt.colorbar(plot, fraction=0.05)
cbar.ax.tick_params(labelsize=20)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')