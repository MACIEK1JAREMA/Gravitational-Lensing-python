# First attetmps at gravitational lensing

# Import modules
import numpy as np
import matplotlib.pyplot as plt

# %%

# set up some initial parameters
rc = 0.7
eps = 0

# set up an image of the source. For simplest test, a single pixel at centre
# As for the initial test, use 21 pixels, empty apart from centre pixel
size = 21  # odd
image_s = np.zeros([size, size])
image_s[int((size-1)/2), int((size-1)/2)] = 1

# set up an empty array to store lensed image
image_l = np.zeros([size, size])


# loop over tracking back pixels from image_l to image_s via lens eqn
# Inefficiently for now (initial attempts)
for i in range(size):
    for j in range(size):
        # based on pixel position get reduced coords. r_1 and r_2
        r1 = (1/size)*(2*i - size)
        r2 = (1/size)*(2*j - size)
        # use lens equation to get position on image_s of this pixel
        s1 = r1 - ((1 - eps)*r1)/np.sqrt(rc**2 + (1 - eps)*r1**2 + (1 + eps)*r2**2)
        s2 = r2 - ((1 + eps)*r2)/np.sqrt(rc**2 + (1 - eps)*r1**2 + (1 + eps)*r2**2)
        # translate s coordinates into pixel coordinates
        rs1 = size(1+s1)/2
        rs2 = 
