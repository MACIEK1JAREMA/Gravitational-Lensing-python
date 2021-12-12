'''

Lensing a generated galaxy cluster

@author: Maciej Tomasz Jarema ppymj11

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fonts
import Project_completed.modules.lensing_function as lensing
import Project_completed.modules.draw_pixels as pix_draw
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up parameters for lenisng and image
rc = 0.2
eps = 0
size = 2048
dom = 3  # abs() of domain of r values (normally -1, 1 --> 1)

# set up galaxy parameters (in pixel units)
max_a = 0.32  # maximum scale-length
minor_max = 80  # max minor axis
gal_N = 70  # number to generate

# ############################################################################
# Generate galaxy cluster
# ############################################################################

# start the timer for galaxy drawing function, run it and return time
start_f = timeit.default_timer()

image = pix_draw.gal_image(gal_N, size, max_a, minor_max, minor_major_multiplier=4, seeded=143)

stop_f = timeit.default_timer()
print('Time to generate source image was: {:.4f}'.format(stop_f - start_f) + ' s')
print('\n')

# ############################################################################
# Lens and present end result
# ############################################################################

# set up a figure, axis
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# set up visuals for each axis
ax1.set_aspect('equal')
ax2.set_aspect('equal')
plt.xticks([])  # take off the axis ticks for both, no need for images
plt.yticks([])
plt.sca(ax1)
plt.xticks([])
plt.yticks([])

# plot the soure image
ax1.imshow(image/255)

# plot the lensed image
image_lens = lensing.lens(image, rc, eps, dom)
ax2.imshow(image_lens/255)

# add a scale bar:
ring_size = np.sqrt(1-rc**2) - dom
ring_reduced = (ring_size + dom) * (size-1) / (2*dom)
font = fonts.FontProperties(size=16)
scalebar = AnchoredSizeBar(ax2.transData, ring_reduced, r'$r_{ring} ~ ' + '{:.2f}$'.format(np.sqrt(1-rc**2)), 'lower left', pad=0.1, color='white', fontproperties=font, frameon=False)
ax2.add_artist(scalebar)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
