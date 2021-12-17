'''

Convergence study of maximum mangification for central value with resolution

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
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)

# set the initial size and maximum. To conserve pixel size, will split each
# at each step upto 'splits'

lasts = []

for init_N in np.arange(3, 15, 2):
    if init_N < 10:
        N_max = init_N * 200
    else:
        N_max = 1500
    splits = N_max//init_N
    
    # set up array to store number of pixels for eahc of these:
    N_ends = []
    
    # set up an array of used image sizes
    sizes = []
    
    odds = []
    odds_n = []
    evens = []
    evens_n = []
    
    # loop over them finding max magnification:
    for msplit in range(1, splits):
        
        # get size of image from original and number of splits in each cell
        N = init_N*msplit
        
        # reset the initial image
        image_s = np.zeros((N, N, 3))
        
        if msplit == 1:
            half = int((N-1)/2)
            image_s[half, half, 0] = 1
        
        elif msplit % 2 == 1:
            half = int((N-1)/2)  # middle integer
            spread = int((msplit-1)/2)  # range around to to inc in xoliured pixel
            image_s[half-spread : half+spread, half-spread : half+spread, 0] = 1/msplit**2
    
        else:
            half = int(N/2)  # not middle index, but represntative
            spread = int(msplit/2)  # spread around rep. middle
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
        
        if msplit % 2 == 1:
            odds.append(N_end)
            odds_n.append(N)
        else:
            evens.append(N_end)
            evens_n.append(N)
    
    lasts.append(evens[-1])

# %%
# set up figure, axia and visuals
fig = plt.figure()
ax1 = fig.add_subplot(111)

# plot
inits = np.arange(3, 15, 2)
ax1.plot(inits, lasts/inits)


# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')