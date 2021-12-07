# Parameter study - ellipticity impact on intensity

# keep the source in the middle of the image, lens it with
# different ellipticity lesnses and compare total 'luminosoty'
# as sum of all pixel RGB

# import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from skimage.measure import label, regionprops
import project.lensing_function as lensing
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some parameters
rc = 0.1
dom = 5  # abs() of domain of r values (normally -1, 1 --> 1)
size = 300
size_obj = 20
eps = 0  # initial
eps_N = 100

# set up array of set eps:
eps_arr = np.linspace(0, 0.99, eps_N)

# set up a total luminosity list to store it for each ellipticity
lum_arr = []

# set up the source image, with centred, circular source:
image_s = np.zeros([size, size, 3])
for i in range(2*size_obj+1):
    for j in range(2*size_obj+1):
        # get x and y from these relative to star centre
        x = -size_obj + i
        y = -size_obj + j
        # check if current point is outside the circle:
        if (x/size_obj)**2 + (y/size_obj)**2 > 1:
            pass
        else:
            # its in ellipse, add its pixel data accordinly
            try:  # careful about image edges
                image_s[int(size/2) - size_obj + i, int(size/2) - size_obj + j, :] += tuple((1, 0, 0))
            except IndexError:
                pass

# show image:
plt.imshow(image_s)  # no /255 to easily see R=1, easier to track with this


# loop over changing ellipticity, for each, lens and get total intensity:
for epsilon in eps_arr:
    # lens
    image_lens = lensing.lens(image_s, rc, epsilon, dom)
    
    # update the total luminosty array with sum of all pizels with colours
    lum_arr.append(np.sum(image_lens/255))


# plot graph:
plt.figure()
plt.plot(eps_arr, lum_arr, 'b-')



# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')

# %%

# lens
image_lens = lensing.lens(image_s, rc, 0.99, 5)

# plot
plt.imshow(image_lens)