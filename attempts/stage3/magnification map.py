# Magnification map

# import modules
import numpy as np
import matplotlib.pyplot as plt
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
size = 201  # don;t set higher than 4096, cant mark uniquely in RGB

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
                mark_B += 1

# plot that image
plt.imshow(image_s/255)

# now lens this image, use the imported function
image_lensed = lensing.lens(image_s, rc, eps, dom)

# normalise it to [0, 1] form [0, 255] for imshow
image_lensed *= 1/255

# start a new figure and plot it
plt.figure()
plt.imshow(image_lensed)

# now need to count how many of each RBG combinations appear

# !!!

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')