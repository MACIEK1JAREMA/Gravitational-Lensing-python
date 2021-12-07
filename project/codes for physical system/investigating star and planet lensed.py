# planet + star lensing, investigation for possible correlation

# import modules
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy
from scipy import integrate
import project.lensing_function as lensing
import matplotlib.widgets as widgets
from scipy.signal import find_peaks
import timeit

# %%

# start the timer
start = timeit.default_timer()

# start up an empty source image and lensing parametrers
size = 200
eps = 0
rc = 0.1
dom = 5

# set up simualtion time parameters
year = 3.156e7  # numerical factor
t_max = 1 * year
t_number = 400

# set up 2 body system parameters in SI
M = 2e30
m = 6e24
G = 6.67e-11
maxR = 1.496e11  # max planet disp from star, in SI

# define star and planet sizes in pixels:
size_s = 20
size_p = 6
size_source = 4e11  # size of the source plane

# from size of max orbit get pixel size to scale down
p_width = size_source/size

# set initial parameters of the 2 bodies in SI
xs = 0
ys = 0
xp = maxR
yp = 0
vxs = 0
vys = 0
vxp = 0
vyp = -29800

init_cond = [xs, ys, xp, yp, vxs, vys, vxp, vyp]  # put into a list


# #############################################################################
# simulation of 2 bodies orbiting in plane, for centre positions
# #############################################################################

# get time array and needed values
t_arr = np.linspace(0, t_max, t_number)
dt = t_arr[-1] - t_arr[-2]

# initialise the lists that will store integrated, bolometric 'luminosity'
# for both transit data and lensed transit
lumin_bol = []
lumin_bol_lensed = []

# set up a fucntion for odeint to use to get needed derivatives
def jacob(y, x):
    # set up an empty list to store derivaitves:
    derivs = np.zeros_like(y)
    
    # deal with substitution derivatives:
    derivs[0] = y[4]
    derivs[1] = y[5]
    derivs[2] = y[6]
    derivs[3] = y[7]
    
    # get the distance between the bodies
    dist = np.sqrt((y[0] - y[2])**2 + (y[1] - y[3])**2)
    
    # deal with equation dependant derivatives, from N2L and N grav. law. in 1D
    derivs[4] = -(G*m/dist**3) * (y[0] - y[2])
    derivs[5] = -(G*m/dist**3) * (y[1] - y[3])
    derivs[6] = -(G*M/dist**3) * (y[2] - y[0])
    derivs[7] = -(G*M/dist**3) * (y[3] - y[1])
    
    # return to odeint:
    return derivs


# call odeint to solve it:
solution = scipy.integrate.odeint(jacob, init_cond, t_arr)

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
    
    # scale down to domain and find which pixels these lie in
    # NB y index is always half way up
    index_s = np.floor((x[0] + size_source/2)/p_width)
    index_p = np.floor((x[1] + size_source/2)/p_width) - 1  # zero-indexing
    index_s = index_s.astype(int).transpose() # change them to integers
    index_p = index_p.astype(int).transpose()
    
    # set initial checker for if planet is in front:
    pfront = True
    
    # check which body is in front when in line, using the y data:
    if abs(index_s + size_s) > abs(index_p - size_p) and abs(index_s - size_s) < abs(index_p + size_p):
        if yp_anim[t_index] < ys_anim[t_index]:
            pfront = False
        elif yp_anim[t_index] > ys_anim[t_index]:
            pfront = True
        else:
            pass
    else:
        pass
    
    # draw on the star as a big, yellow circle:
    for i in range(2*size_s+1):
        for j in range(2*size_s+1):
            # get x and y from these relative to star centre
            x = -size_s + i
            y = -size_s + j
            # check if current point is outside the ellipse:
            if (x/size_s)**2 + (y/size_s)**2 > 1:
                pass
            else:
                # its in ellipse, add its pixel data accordinly
                try:  # careful about image edges
                    image_s[int(size/2) - size_s + i, index_s  - size_s + j, :] += tuple((255, 255, 255))
                except IndexError:
                    pass
    
    # draw on the planet as a smaller, dark circle:
    for i in range(2*size_p+1):
        for j in range(2*size_p+1):
            # get x and y from these relative to planet centre
            x = -size_p + i
            y = -size_p + j
            # check if current point is outside the ellipse:
            if (x/size_p)**2 + (y/size_p)**2 > 1:
                pass
            else:
                # its in ellipse, add its pixel data accordinly
                try:  # careful about image edges
                    # check if overcasting the sun:
                    if pfront:
                        image_s[int(size/2) - size_p + i, index_p - size_p + j, :] = tuple((0, 0, 0))
                    else:
                        pass
                except IndexError:
                    pass
    
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

