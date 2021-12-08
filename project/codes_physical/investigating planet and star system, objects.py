# planet + star lensing, investigation
# and use of classes

# import modules
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import integrate
import project.lensing_function as lensing
import project.codes_physical.functions.class_2body as bodies
import project.codes_physical.functions.draw_sphere as pix_draw
from numba import jit
import timeit

# %%

# start the timer
start = timeit.default_timer()

# start up lensing parametrers and constants
size = 400
eps = 0
rc = 0.1
dom = 4
year = 3.156e7
G = 6.67e-11
maxR = 1.496e11  # AU in SI
size_source = 4e11  # size of the source plane
p_width = size_source/size  # get pixel size to scale down

# set up simualtion time parameters
t_max = 1 * year
t_number = 300
t_arr = np.linspace(0, t_max, t_number)
dt = t_arr[-1] - t_arr[-2]

# set up 2 body system parameters in SI, using imported classes:
Star = bodies.body_def(Mass=2e30, size=40, x=0, y=0, vx=0, vy=0)  # Star
Planet = bodies.body_def(Mass=6e24, size=12, x=maxR, y=0, vx=0, vy=-29800)  # Planet

# Merge them into a system:
system = bodies.system_def(Star, Planet)
system.initials()  # produce initial conditions in system instance

# #############################################################################
# simulation of 2 bodies orbiting in plane, for centre positions
# #############################################################################

# initialise the lists that will store integrated, bolometric 'luminosity'
# for both transit data and lensed transit
lumin_bol = []
lumin_bol_lensed = []

# call odeint to solve it:
solution = scipy.integrate.odeint(system.jacobian_get, system.init, t_arr)

# from it extract wanted positions
xs_anim = solution[:, 0]
xp_anim = solution[:, 2]

ys_anim = solution[:, 1]
yp_anim = solution[:, 3]


# #############################################################################
# from animated solution, get the pixelated images of the bodies
# and light curves with and without gravitationally lensing
# #############################################################################

# set a stopping variable
switchoff = False

# loop over the simulation result values and get data from transit and lensed transit
for t_index in range(len(t_arr)):
    
    # reset the image:
    image_s = np.zeros((size, size, 3))
    
    # get the current x values for planet and star
    x = [xs_anim[t_index], xp_anim[t_index]]
    
    # scale down to domain and find which x pixels these lie in
    # NB y index is always half way up
    index_s = np.floor((x[0] + size_source/2)/p_width) - 1
    index_p = np.floor((x[1] + size_source/2)/p_width) - 1  # zero-indexing
    index_s = index_s.astype(int).transpose() # change them to integers
    index_p = index_p.astype(int).transpose()
    
    # set initial checker for if planet is in front:
    pfront = True
    
    # check which body is in front when in line, using the y data:
    if abs(index_s + Star.size) > abs(index_p - Planet.size) and abs(index_s - Star.size) < abs(index_p + Planet.size):
        if yp_anim[t_index] < ys_anim[t_index]:
            pfront = False
    
    # draw on the star as a big, yellow circle, using above defined
    # function, sped up bu numba jit
    image_s = pix_draw.draw_sphere(Star.size, image_s, index_s, (255, 255, 255))
    
    # draw on the planet as a smaller, dark circle, if not behind star
    if pfront:
        image_s = pix_draw.draw_sphere(Planet.size, image_s, index_p, (30, 30, 30))

    # save the luminosities into the list
    lumin_bol.append(np.sum(image_s/255))
    
    # lens the created image:
    image_lens = lensing.lens(image_s, rc, eps, dom)
    
    # update the total luminosty array
    lumin_bol_lensed.append(np.sum(image_lens/255))


# #############################################################################
# plot the light curves
# #############################################################################


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
#plt.plot(xs_anim, ys_anim, 'b*')
#plt.plot(xp_anim, yp_anim)

# set up a figure, axis and visuals for the light curves
fig_lc = plt.figure()
ax_lc = fig_lc.gca()
ax_lc.set_xlabel('time [years]')
ax_lc.set_ylabel(r'$L_{bol} [RGB \ sum]$')

# turn resulting lists into arrays:
lumin_bol = np.array(lumin_bol)
lumin_bol_lensed = np.array(lumin_bol_lensed)

# plot the obtained light curves:
ax_lc.plot(t_arr[:len(lumin_bol)]/year, lumin_bol, label='original')
ax_lc.plot(t_arr[:len(lumin_bol_lensed)]/year, lumin_bol_lensed, label='lensed')
ax_lc.legend()

# print the dip size ratio:
print('dip size ratio = {:.4f}'.format(np.max(abs(lumin_bol_lensed))/np.max(abs(lumin_bol))))

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')

