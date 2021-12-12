'''

Measures distortion to shape caused by lensing by ratio of peirm/area in pixels
Does so in 1D

@author: Maciej Tomasz Jarema ppymj11

'''

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops
import Project_completed.modules.lensing_function as lensing
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.2
eps = 0
size = 401
dom = 5  # abs() of domain of r values (normally -1, 1 --> 1)
p_width = 2*dom/(size)  # width of each pixel

# max number of pixels displacement from centre
disp_max = 100

# set up a list to store ratio of perimeter to area
ratio_list = []


# loop over different number of displacements, lensing and finding the ratio
for disp in range(-disp_max, disp_max+1, 1):
    
    # set up an image of the source, with 1 pixel, at displaced position
    image_s = np.zeros([size, size, 3])
    #image_s[int((size-1)/2) + disp, int((size-1)/2) + disp, 0] = 1  # keep one commented
    #image_s[int((size-1)/2), int((size-1)/2) + disp, 0] = 1
    image_s[int((size-1)/2) + disp, int((size-1)/2), 0] = 1
    
    # set up an empty array to store lensed image and lens
    image_l = np.zeros([size, size, 3])
    image_l = lensing.lens(image_s, rc, eps, dom)
    
    # finding the area, perim and perim/area in lensed image:
    # NB The area of source is one pixel = 1
    
    # find the area of the ending lensed image in terms of pixels:
    nonzero_number = len(np.nonzero(image_l[:, :, 0]))  # source is only red
    
    # find the perimeter of the new shape:
    image_shape = image_l[:, :, 0] != 0
    region = regionprops(image_shape.astype(int))
    perim = region[0].perimeter
    
    # find the ratio of area to perimeter of it and append to list
    ratio = perim/nonzero_number
    ratio_list.append(ratio)


# set up a list of all used displacement as in loop:
disps = [i for i in range(-disp_max, disp_max+1, 1)]

# set up a figre, axis and visuals
fig = plt.figure()
ax = fig.gca()
ax.set_xlabel(r'$displacement \ from \ centre \ [pixels]$')
ax.set_ylabel(r'$\frac{image \ object \ perimeter \ [pixels]}{image \ object \ area \ [pixels]}$')

# plot the resulting graph
ax.plot(disps, ratio_list)


# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')


# %%

'''

Manual tests of specific displacement

'''

# start the timer
start = timeit.default_timer()

# set up some initial parameters, as instrucetd on the sheet
disp = 19

# set up image arrays. Source is single pixel at centre. Lensed is empty now
image_s = np.zeros([size, size, 3])
image_s[int((size-1)/2) + disp, int((size-1)/2), 0] = 1
image_l = np.zeros([size, size, 3])

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
