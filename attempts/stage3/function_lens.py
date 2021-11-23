# create a function that completes the lensing process:

# import modules
import numpy as np
import matplotlib.pyplot as plt

# %%


def lens(image_s, rc, eps, dom=1):
    '''
    Lenses the given image for a planar, transparent, symmetric lensing object
    inputs:
    square image as numpy array of values from 0 to 255 in RGB
    central core radius rc
    ellipticity eps
    domain of the image, as absolute value (default=1, giving range [-1, 1])
    return array of the lensed image
    '''
    
    # check if the user gave a square image and get number of pixels per side
    if len(image_s[:, 0, 0]) == len(image_s[0, :, 0]):
        size = len(image_s)
    else:
        raise IndexError(' Image must be square, can\'t broadcast with different shapes')

    # set up an empty array to store lensed image
    image_l = np.zeros([size, size, 3])
    
    # find the width of each pixel given the domain and size
    p_width = 2*dom/(size)
    
    # Vectorised the mapping of pixels to source plane and copying data:
    
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
    index_1 = index_1.astype(int).transpose()
    index_2 = index_2.astype(int).transpose()
    
    # copy the data from source image at these indexes over to lens image array
    image_l[:, :, :] = image_s[index_1, index_2, :]
    
    # return the image to the suer
    return image_l
