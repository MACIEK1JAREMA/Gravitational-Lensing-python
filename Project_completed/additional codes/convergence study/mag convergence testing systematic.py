'''

Convergence study of maximum mangification for central value with resolution
For graph of the found systematic error on convergence from initial image

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
rc = 0.7
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)

# set the initial size and maximum. To conserve pixel size, will split each
# at each step upto 'splits'
initial_img_start = 21  # initial
initial_img_end = 121

# lists to store results:
Mag_odds = []
Mag_evens = []
N_inis = []

# loop over different start size images
for initial_img in np.arange(initial_img_start, initial_img_end, 10):
    
    init_N = initial_img  # multpile of initial img
    N_max = 30*init_N
    splits = N_max//init_N
    
    # set up lists to store wnated data
    odds = []  # magnification for odd size images
    evens = []
    
    # loop over them finding max magnification:
    for msplit in range(int(init_N/initial_img), splits):
        # get size of image
        N = initial_img*msplit
        
        # reset the initial image
        image_s = np.zeros((N, N, 3))
        
        # get 'half way' indicies for odd / even 
        ho = int((N-1)/2)
        he_o = int(((N/msplit) - 1)/2)  # for odd starting grids
        he= int(N/(2*msplit))
        
        # fill its middle in same range
        if initial_img % 2 == 1:  # odd starting grids
            if msplit == 1:
                image_s[ho, ho, 0] = 1
            elif msplit % 2 == 1:
                spread = int((msplit-1)/2)  # range around to to inc in coloured pixel
                image_s[ho-spread : ho+spread+1, ho-spread : ho+spread+1, 0] = 1/(msplit**2)
            else:
                # even grids from even splits of odd grid
                spread = int(msplit)
                image_s[he_o*msplit : he_o*msplit + msplit, he_o*msplit : he_o*msplit + msplit, 0] = 1/(msplit**2)
        else:  # even starting grids
            image_s[(he-1)*msplit:(he+1)*msplit, (he-1)*msplit:(he+1)*msplit, 0] = 1/(msplit**2)
        
        # lens it
        image_l = lensing.lens(image_s, rc, eps, dom)
        
        # find number of pixels this central value projected to
        N_end = np.sum(image_l)
        
        # appedn to odds and evens depending on orig image:
        if initial_img % 2 == 1:
            if msplit % 2 == 1:
                odds.append(N_end/initial_img)
            else:
                evens.append(N_end/initial_img)
        else:
            evens.append(N_end/initial_img)
    
    # get out end, converged results:
    Mag_odds.append(odds[-1])
    Mag_evens.append(evens[-1])
    N_inis.append(init_N)

# set up figure, axis and visuals
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.tick_params(labelsize=20)
ax2.tick_params(labelsize=20)
ax1.plot(N_inis, Mag_odds, label='odd sizes')
ax1.plot(N_inis, Mag_evens, label='even sizes')
ax1.set_xlabel(r'$N_{i}$', fontsize=20)
ax1.set_ylabel('M', fontsize=20)
ax1.legend(fontsize=20)

ax2.plot(np.log10(N_inis), np.log10(Mag_odds), label='odd sizes')
ax2.plot(np.log10(N_inis), np.log10(Mag_evens), label='even sizes')
ax2.set_xlabel(r'$log_{10}(N_i)$', fontsize=20)
ax2.set_ylabel(r'$log_{10}(M)$', fontsize=20)
ax2.legend(fontsize=20)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')

