'''

Convergence study of maximum mangification for central value with size

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import Project_completed.modules.lensing_function as lensing
import timeit

# %%

# start the timer
start = timeit.default_timer()


# set up lensing parameters
rc = 0
eps = 0
dom = 2  # abs() of domain of r values (normally -1, 1 --> 1)

# set the values of size to check the central magnification for
# all must be odd to ensure centre
init_N = 3  # odd
N_max = 600
splits = N_max//init_N

# set up array to store number of pixels for eahc of these:
N_ends = []

# set up an array of used image sizes
sizes = []

# loop over them finding max magnification:
for msplit in range(1, splits):
    
    # get size of image from original and number of splits in each cell
    N = init_N*msplit
    
    # reset the initial image
    image_s = np.zeros((N, N, 3))
    
    if msplit % 2 == 1:
        half = int((N-1)/2)  # middle integer
        spread = int((msplit-1)/2)  # range around to to inc in xoliured pixel
        image_s[half-spread : half+spread, half-spread : half+spread, 0] = 1/msplit**2
        
        # lens it
        image_l = lensing.lens(image_s, rc, eps, dom)
        
        # find number of pixels this central value projected to
        # using 1 in R (from RGB) only, this is same as sum:
        # note, includes the pixel itself, as for transparent source, it will
        # also be visible
        N_end = np.sum(image_l)
        N_ends.append(N_end)
        sizes.append(N)

    else:
        pass
#        half = int(N/2)  # not middle index, but represntative
#        spread = int(msplit/2)  # spread around rep. middle
#        image_s[half-spread : half+spread, half-spread : half+spread, 0] = 1/msplit**2

# from the found sums, get magnifications, removing the bias of more points
# size**2
mag = N_ends

# set up figure, axia and visuals
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.set_xlabel(r'$N \ [pixels]$', fontsize=16)
ax1.set_ylabel(r'$M \ L_{bol, f} \ / \ L_{bol, i}$', fontsize=16)
ax2.set_xlabel(r'$N$', fontsize=16)
ax2.set_ylabel(r'$100 \ \delta M$', fontsize=16)

# plot
ax1.plot(sizes, mag)

# magnification convergence value and its confidence interval

# get fractional changes in magnification between each iteration
change = (np.diff(mag) / mag[:-1])*100

ax2.plot(sizes[1:], change)

# horizontals at 2% and 1% for reference:
ax2.plot(sizes[1:], np.ones(np.shape(sizes[1:])) * 1, 'g-.')
ax2.plot(sizes[1:], np.ones(np.shape(sizes[1:])) * 2, 'r-.')

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')