# 1D distoritions measured as perim / area from circular source

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some initial parameters
rc = 0.2
eps = 0
size = 401
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)

# max number of pixels displacement
disp_max = 30

# set up a list to store ratio of perimeter to area
ratio_list = []


# loop over different number of displacements, lensing and finding the ratio
for disp in range(-disp_max, disp_max+1, 1):
    
    # Lensing the image with displaced source:
    
    # set up an image of the source, with 1 pixel, at displaced position
    image_s = np.zeros([size, size, 3])
    #image_s[int((size-1)/2), int((size-1)/2) + disp, 0] = 1  # keep one commented
    image_s[int((size-1)/2) + disp, int((size-1)/2), 0] = 1
    p_width = 2*dom/(size)  # width of each pixel
    
    # set up an empty array to store lensed image
    image_l = np.zeros([size, size, 3])
    
    # set up an array of index numbers in the lens image array
    i_arr = np.arange(0, size, 1)
    j_arr = np.arange(0, size, 1)
    
    # get reduced coords. r_1 and r_2 as arrays and mesh
    r1 = 2*dom*i_arr/(size-1) - dom
    r2 = 2*dom*j_arr/(size-1) - dom
    r1g, r2g = np.meshgrid(r1, r2)
    
    # use lens equation to get array of positions on image_s
    s1 = r1g - ((1 - eps)*r1g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)
    s2 = r2g - ((1 + eps)*r2g)/np.sqrt(rc**2 + (1 - eps)*r1g**2 + (1 + eps)*r2g**2)
    
    # find which pixel they lie in in the original image for all pixels
    index_1 = np.floor((s1 + dom)/p_width)
    index_2 = np.floor((s2 + dom)/p_width)
    
    # change them to integers
    index_1 = index_1.astype(int).transpose()
    index_2 = index_2.astype(int).transpose()
    
    # copy the data from source image at these indexes over to lens image array
    image_l[:, :, :] = image_s[index_1, index_2, :]
    
    # finding the area, perim and perim/area in lensed image:
    # NB The area of source is one pixel
    
    # find the area of the ending lensed image in terms of pixels:
    nonzero_number = len(np.nonzero(image_l[:, :, 0]))  # source is only red
    
    try:
        # find the perimeter of the new shape:
        image_shape = image_l[:, :, 0] != 0
        region = regionprops(image_shape.astype(int))
        perim = region[0].perimeter
        
        # find the ratio of area to perimeter of it and append to list
        ratio = perim/nonzero_number
        ratio_list.append(ratio)
        
    except IndexError:
        # shape has been lensed completely outside of the initial image
        pass

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
