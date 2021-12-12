'''

TESTING

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters, as instrucetd on the sheet
rc = 0.2
eps = 0
size = 401  # odd
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)


disp = 20

# set up image arrays. Source is single pixel at centre. Lensed is empty now
image_s = np.zeros([size, size, 3])
image_s[int((size-1)/2) + disp, int((size-1)/2), 0] = 1

image_l = np.zeros([size, size, 3])
p_width = 2*dom/(size)  # get width of each pixel

# #############################################################################
# Vectorised mapping of pixels to source plane and copying data:
# #############################################################################

# set up an array of index numbers corr. to lensed image array
i_arr = np.arange(0, size, 1)
j_arr = np.arange(0, size, 1)

# get reduced coordinates r_1 and r_2 as arrays and use their grids to get s
# by given equtions for s1 and s2
r1 = 2*dom*i_arr/(size) - dom + p_width/2
r2 = 2*dom*j_arr/(size) - dom + p_width/2
r1g, r2g = np.meshgrid(r1, r2)
s1 = r1g - ((1 - eps)*r1g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)
s2 = r2g - ((1 + eps)*r2g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)

# find which pixel the s1's and s2's all lie in, in the original image
index_1 = np.floor((s1 + dom)/p_width)
index_2 = np.floor((s2 + dom)/p_width) 
index_1 = index_1.astype(int) # change them to integers
index_2 = index_2.astype(int)

# copy the data from source image at these indexes over to lens image array
image_l[:, :, :] = image_s[index_1, index_2, :]

# #############################################################################
# display result
# #############################################################################

# start a figure and customise visuals
fig = plt.figure()
ax = fig.gca()
ax.set_xlabel(r'$x \ pixel \ index$')
ax.set_ylabel(r'$y \ pixel \ index$')
ax.set_xticks(np.arange(0, size+1, int(size/5)))
ax.set_yticks(np.arange(0, size+1, int(size/5)))

# plot the resulting image onto that plot
ax.imshow(image_l)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')