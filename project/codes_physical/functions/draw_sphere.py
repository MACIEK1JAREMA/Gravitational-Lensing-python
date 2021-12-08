# drawing a sphere function
from numba import jit

@jit(nopython=True)
# define a function that will draw spherical regions around point in pixels
def draw_sphere(body_size, image_s, index, color):
    '''
    Draws a spherical body on the provided image in pixels
    Parameters:
    --------------
    body - size of body (radius) in pizels, int.
    image_s - size x size x 3 array, image will be plotted on it.
    color - tuple of size 3, gives flat RGB color of shpere.
    
    Returns:
    --------------
    image as size x size x 3 array
    
    '''
    
    # make sure given image is square:
    assert len(image_s[0, :, 0]) == len(image_s[:, 0, 0]), 'Need a square Image'
    
    # from given array get size
    size = len(image_s[0, :, 0])
    
    # loop over i and j, for a square around the object
    for i in range(2*body_size+1):
        # get x rel. to star centre and current x index
        x = -body_size + i
        ind_1 = int(size/2) - body_size + i
        for j in range(2*body_size+1):
            # get y rel. to star centre and current y index
            y = -body_size + j
            ind_2 = index - body_size + j
            # check if current point is outside the ellipse:
            if ((x/body_size)**2 + (y/body_size)**2) <= 1 and (ind_1 >= 0 and ind_1 < size) and (ind_2 >= 0 and ind_2 < size):
                image_s[ind_1, ind_2, :] = color
    
    # return the image with source drawn, to user
    return image_s

