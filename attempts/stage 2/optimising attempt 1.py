# Attempts at vectorising the lensing process

# import modules
import numpy as np
import matplotlib.pyplot as plt
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.7
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)
size = 101  # odd for test

# set up an image of the source. For simplest test, a single pixel at centre
# As for the initial test
image_s = np.zeros([size, size, 3])  # allow for RGB from the start
image_s[int((size-1)/2), int((size-1)/2), 0] = 1

# plot that image
plt.imshow(image_s)

# set up an empty array to store lensed image
image_l = np.zeros([size, size, 3])

# find the width of each pixel given the domain and size
p_width = 2*dom/(size)

# loop over tracking back pixels from image_l to image_s via lens eqn
# Inefficiently for now (initial attempts)
for i in range(size):
    for j in range(size):
        # based on pixel position get reduced coords. r_1 and r_2
        r1 = 2*dom*i/(size-1) - dom
        r2 = 2*dom*j/(size-1) - dom
        # use lens equation to get position on image_s of this pixel
        s1 = r1 - ((1 - eps)*r1)/np.sqrt(rc**2 + (1 - eps)*r1**2 + (1 + eps)*r2**2)
        s2 = r2 - ((1 + eps)*r2)/np.sqrt(rc**2 + (1 - eps)*r1**2 + (1 + eps)*r2**2)
        # s coordinates dont have to be pixel positions in reduced
        # need to find which pixel they lie in in the original image
        index_1 = int(np.floor((s1 + dom)/p_width))
        index_2 = int(np.floor((s2 + dom)/p_width))
        # check input of these indexes in the original image
        values = image_s[index_1, index_2, :]
        # put whatever these are into the lensed image
        image_l[i, j, :] += values


plt.figure()
# plot the resulting image
plt.imshow(image_l)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')