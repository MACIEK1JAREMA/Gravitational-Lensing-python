# chessboard pattern for magnification

# Attempts at vectorising the lensing process

# import modules
import numpy as np
import matplotlib.pyplot as plt
import timeit
from PIL import Image

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.7
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)
size = 201  # odd for test

# read in the image of the source
# NB set correct Working directory
image_s = Image.open('attempts\\images\\M83 my own image.jpg')
# change it to a numpy array
image_s = np.array(image_s)

# from it, extract size:
size = len(image_s[:, 0 , 0])

# plot that image
plt.imshow(image_s)

# set up an empty array to store lensed image
image_l = np.zeros([size, size, 3])

# find the width of each pixel given the domain and size
p_width = 2*dom/(size)

# Vectorising the mapping of pixels to source plane and copying data:

# set up an array of index numbers in the lens image array
i_arr = np.arange(0, size, 1)
j_arr = np.arange(0, size, 1)

# based on pixel position get reduced coords. r_1 and r_2 as arrays
r1 = 2*dom*i_arr/(size-1) - dom
r2 = 2*dom*j_arr/(size-1) - dom

# grid them
r1g, r2g = np.meshgrid(r1, r2)

# use lens equation to get array of positions on image_s for each pixel in lens image
s1 = r1g - ((1 - eps)*r1g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)
s2 = r2g - ((1 + eps)*r2g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)

# s coordinates dont have to be pixel positions in reduced
# need to find which pixel they lie in in the original image for all pixels
# therefore for all array values
index_1 = np.floor((s1 + dom)/p_width)
index_2 = np.floor((s2 + dom)/p_width)

# change them to integers
index_1 = index_1.astype(int)
index_2 = index_2.astype(int)

# copy the data from source image at these indexes over to lens image array
image_l[:, :, :] = image_s[index_1, index_2, :]

# correct for RGB going range 0, 1 for imshow
image_l *= 1/256


plt.figure()
# plot the resulting image
plt.imshow(image_l)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')