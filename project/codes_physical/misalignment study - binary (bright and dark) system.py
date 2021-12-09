# binary (bright + dark) system investigation into misalignment

# import modules
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import integrate
import project.lensing_function as lensing
import project.codes_physical.functions.class_2body as bodies
import project.codes_physical.functions.draw_sphere as pix_draw
import matplotlib.widgets as widgets
from scipy.signal import find_peaks
from numba import jit
import timeit


# loop over lensing the system, with different x displacements in each repeat
# to get representative plots for the system at different displacements:
# do so in a fucntion to speed it up with numba
#@jit(nopython=True)
def binary_len(displacements, axis, size, t_arr, p_width, maxR, sizes, sizep, eps=0, rc=0.15, dom=6):
    '''
    Lenses a binary system of two objects, of equal mass, one big and bright,
    one smaller and dark. Calculates the Light curve and returns it to user
    Repeats doing so for different displacements from aligned binary CoM.
    
    Parameters:
    -------------
    displacements - list or array of displacements of CoM of binary to lensing
                    planar object at screen centre. Do not use many (slow)
    
    axis - list of matplotlib axis instances - list of axis on which to plot
                                               for each dispalcement
    
    size - int - size of image to use in pixels, deifnes precision
    
    t - array of times (floats or ints) for odeint to use in solving
    
    p_width - float - gives width of each pixel in simualtion taht runs in SI
    
    maxR - float - initial distance from CoM of each body, in SI
                    with p_width and size, make sure that this fits in plot
                    
    sizes and sizep - int - sizes of star and planet in pixels (respectively)
    
    
    eps, rc and dom - standard lensing parameters, as in lensing fucntion.
    
    Returns:
    -------------
    axis - list of matplotlib axis instances, with plots of light curves
            for each displacement, in order of given array.
    
    light_curves - list of arrays taht store light curve for each time
    
    maxima - list of arrays of positions and heights of peaks
    
    '''
    
    # from p_width and size, get size of whole plane in SI
    size_source = p_width * size
    
    # axis index counter
    axc = 0
    
    # set up an array to store Light curves
    light_curves = []
    
    # set up an array to store peaks for each disp
    maxima = []
    
    for com_disp in displacements:
        # set up 2 body system parameters in SI, using imported classes:
        Star = bodies.body_def(Mass=2e30, size=sizes, x=-maxR/2 + com_disp, y=0, vx=0, vy=20000)  # Star
        Planet = bodies.body_def(Mass=2e30, size=sizep, x=maxR/2 + com_disp, y=0, vx=0, vy=-20000)  # Planet
        
        # Merge them into a system:
        system = bodies.system_def(Star, Planet)
        system.initials()  # produce initial conditions in system instance
        
        # #############################################################################
        # simulation of 2 bodies orbiting in plane, for centre positions
        # #############################################################################
        
        # initialise the list that will store integrated, bolometric 'luminosity'
        lumin_bol = []
        
        # call odeint to solve it:
        solution = scipy.integrate.odeint(system.jacobian_get, system.init, t_arr)
        
        # from it extract wanted positions
        xs_anim = solution[:, 0]
        xp_anim = solution[:, 2]
        
        ys_anim = solution[:, 1]
        yp_anim = solution[:, 3]
        
        
        # #############################################################################
        # Animation with pixel placement
        # #############################################################################
        
        # loop over the simulation result values and plot as animation, wiht pixels
        for t_index in range(len(t_arr)):
            
            # reset the image and get current x values for planet and star
            image_s = np.zeros((size, size, 3))
            x = [xs_anim[t_index], xp_anim[t_index]]
            
            # scale down to domain and find which pixels these lie in
            # NB y index is always half way up
            index_s = np.floor((x[0] + size_source/2)/p_width) - 1
            index_p = np.floor((x[1] + size_source/2)/p_width) - 1  # zero-indexing
            index_s = index_s.astype(int).transpose() # change them to integers
            index_p = index_p.astype(int).transpose()
            
            # initial checker: (if planet is in front when in line of star), using the y data
            pfront = True
            if abs(index_s + Star.size) > abs(index_p - Planet.size) and abs(index_s - Star.size) < abs(index_p + Planet.size):
                if yp_anim[t_index] > ys_anim[t_index]:
                    pfront = False
            
            # draw on the star as a big, white circle, use prepared function.
            image_s = pix_draw.draw_sphere(Star.size, image_s, index_s, (230, 230, 230))
            
            # draw on the planet as a smaller, dark circle, if not behind star
            if pfront:
                image_s = pix_draw.draw_sphere(Planet.size, image_s, index_p, (0, 0, 0))
            
            # lens the created image and update total luminosity for this iteration
            image_lens = lensing.lens(image_s, rc, eps, dom)
            lumin_bol.append(np.sum(image_lens/255))
        
        # plot the obtained light curve:
        axis[axc].plot(t_arr[:len(lumin_bol)]/year, lumin_bol)
        
        # from the found L_{bol} extract the positions of peaks and plot these on:
        lumin_bol = np.array(lumin_bol)
        peak_indexes = find_peaks(lumin_bol, height=1)[0]
        lum_maxima = lumin_bol[peak_indexes]
        axis[axc].plot(t_arr[peak_indexes]/year, lum_maxima, 'r*')
        
        # append data to lists to return to user
        light_curves.append(lumin_bol)
        maxima.append(np.vstack((lum_maxima, peak_indexes)))
        
        # update axis index counter
        axc += 1
        
        # find the ratio of their heights and print to user
        #for i in range(int(np.floor(len(lum_maxima)/2))):
        #    if i % 2 == 0:
        #        print(lum_maxima[2*i]/lum_maxima[2*i + 1])
        #    else:
        #        print(lum_maxima[2*i+1]/lum_maxima[2*i])

    return axis, light_curves, maxima


# %%


# start the timer
start = timeit.default_timer()

# #############################################################################
# Set up parameters:
# #############################################################################

# start up an empty source image and lensing parametrers
size = 200
eps = 0
rc = 0.15
dom = 6
year = 3.156e7
maxR = 1.49e11  # AU in SI
size_source = 2.5e11  # size of the source plane
size_star = 18
size_pl = 6

# get pixel size to scale down from full animation to reduced coords
p_width = size_source/size

# set up simualtion time parameters
t_max = 0.55 * year
t_number = 500
t_arr = np.linspace(0, t_max, t_number)
dt = t_arr[-1] - t_arr[-2]

# run the fucnction for a few test deisplacements
disps = [0, maxR/50, maxR/30, maxR/20]

# #############################################################################
# set up visuals, run fucntion and plot results
# #############################################################################

fig = plt.figure(figsize=(15, 4))
axis = []
y_lim = [2000, 11000]

# automatic axis set up:
for a in range(1, len(disps)+1):
    # set up axis and append to list:
    exec('ax' + str(a) + ' = fig.add_subplot(1' + str(len(disps)) + str(a) + ')')
    exec('axis.append(ax' + str(a) + ')')
    
    # set up labels and lmits:
    if a == 1:
        ax1.set_ylabel(r'$L_{bol} [RGB \ sum]$')
    exec('ax' + str(a) + '.set_xlabel(\'time [years]\')')
    exec('ax' + str(a) + '.set_ylim(y_lim[0], y_lim[1])')


# run the function to get all light curves
axis_ret, lc, L_maxima = binary_len(disps, axis, size, t_arr, p_width, maxR, size_star, size_pl, eps, rc, dom)

plt.tight_layout()  # fit subplots to fig

# #############################################################################
# result analysis
# #############################################################################

# extract the two later peaks (affected by planet) and get their height ratios
for run in range(len(disps)):
    exec('ratio' + str(run) + ' = (L_maxima[' + str(run) + '][0, 0] - lc[' + str(run) + '][0]) / (L_maxima[' + str(run) + '][0, 1] - lc[' + str(run) + '][0])' )
    exec('print(\'ratio of second peak to third peak for run \' + str(run) + \' was {:.5f}\'.format(ratio' + str(run) + '))')

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')

# %%


ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
axis = [ax1, ax2, ax3]

# set up visuals for all:
ax1.set_ylabel(r'$L_{bol} [RGB \ sum]$')
ax1.set_xlabel('time [years]')
ax2.set_xlabel('time [years]')
ax3.set_xlabel('time [years]')
ax1.set_ylim(800, 4600)  # adjust manually for nicer figures
ax2.set_ylim(800, 4600)
ax3.set_ylim(800, 4600)



# Extra plots for tests.

# for all time find the CoM position in x and plot to check
# should not change from 0
#x_cm = (M*xs_anim + m*xp_anim)/(M + m)
#fig_cm = plt.figure()
#ax_cm = fig_cm.gca()
#ax_cm.set_xlabel('time step index')
#ax_cm.set_ylabel(r'$x_{cm}$')
#ax_cm.plot(x_cm)

# plot the motion of the two objects in the x-y plane
#plt.figure()
#plt.plot(xs_anim, ys_anim)
#plt.plot(xp_anim, yp_anim)
