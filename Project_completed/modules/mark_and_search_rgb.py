'''

Write functions to mark an image in unique RGB codes and to search for them
in altered image (by lensing)

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
from numba import jit


@jit(nopython=True)
def rgb_track_mark(image_s):
    
    assert len(image_s[:, 0, 0]) == len(image_s[0, :, 0]), 'image must be square'
    assert len(image_s[:, 0, 0]) < np.sqrt(256**3), 'Assert, image too big for uniquq marking'
    
    # get size of image
    size = len(image_s[:, 0, 0])
    
    # initialise markers
    mark_R, mark_G, mark_B = 0, 0, 0
    
    # loop over marking each pixel uniquely
    for i in range(size):
        for j in range(size):
            # set the current pixel to current free, rgb marker
            image_s[i, j, :] = mark_R, mark_G, mark_B
            
            # update markers in base 256
            if mark_B < 255:
                mark_B += 1
            else:
                mark_B = 0
                if mark_G < 255:
                    mark_G += 1
                else:
                    mark_G = 0
                    mark_R += 1
    
    # return image
    return image_s


@jit(nopython=True)
def count_rbgs(results, image_lensed):
    
    # from the input lensed image, get size of array to search
    assert len(image_lensed[0, :, 0]) == len(image_lensed[:, 0, 0]), 'Need a square Image'
    size = len(image_lensed[0, :, 0])
    
    # make sure that results in of correct size to store it:
    assert np.shape(results) == np.shape(image_lensed[:, :, 0])
    
    cR, cG, cB = 0, 0, 0  # intial checkerss
    countx = 0  # source pixel counter
    county = 0


    stop = False  # stopping variable
    
    # loop over checking each RGB combination:
    while stop is False:
        # find how many values appear for current RGB checker
        number = len(np.where((image_lensed[:, :, 0] == cR) & (image_lensed[:, :, 1] == cG) & (image_lensed[:, :, 2] == cB))[0])
        
        # store it in the corresponding pixel
        results[county, countx] = number
        
        # update the checkers as before, in base 256
        if cB < 255:
            cB += 1
        else:
            cB = 0
            if cG < 255:
                cG += 1
            else:
                cG = 0
                cR += 1
        
        # update the source pixel indicies:
        if countx < size-1:
            countx += 1
        else:
            countx = 0
            county += 1
        
        # once all pixel combinations were checked, stop the loop
        if countx == 0 and county == size:
            stop = True
    
    return results

# %%