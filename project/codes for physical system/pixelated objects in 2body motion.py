# changing the animation of 2 body motion to be in pixels, with objects
# that have physical extent

# import modules
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy
from scipy import integrate
import project.lensing_function as lensing
from matplotlib.lines import Line2D
import matplotlib.animation as animation

# %%

# start up an empty source image
size = 200
image_s = np.zeros((size, size, 3))

# #############################################################################
# simulation of 2 bodies orbiting in plane, for centre positions
# #############################################################################

# set up 2 body system parameters in SI
M = 2e30
m = 2e30
G = 6.67e-11
maxR = 1e11  # max planet disp from star, in SI
dom = 1

# from size of max orbit get pixel size to scale down
p_width = maxR/size

# set initial parameters of the 2 bodies in SI
xs = -maxR/2
ys = 0
xp = maxR/2
yp = 0
vxs = 0
vys = 1000
vxp = 0
vyp = -1000

init_cond = [xs, ys, xp, yp, vxs, vys, vxp, vyp]  # put into a list

# get time array and needed values
year = 3.156e7
t_max = 1 * year
t_number = 1000
t_arr = np.linspace(0, t_max, t_number)
dt = t_arr[-1] - t_arr[-2]


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


# #############################################################################
# Animation with pixel placement
# #############################################################################

# set up a figure and axis on which to plot the resulting simulation
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-maxR, maxR), ylim=(-maxR, maxR))
plt.sca(ax)
plt.xticks([])  # take off the axis ticks for both, no need for images
plt.yticks([])
ax.set_aspect('equal')

# set up a timer and draw it on with nothing in it initially
timer = 'time = %.1f yr'
time_text = ax.text(0.05, 0.01, '', transform=ax.transAxes)


# set up a function that defines the initial plot for the animation (empty)
def init():
    plot = ax.imshow(image_s)
    time_text.set_text('')
    return plot, time_text


# set up a function to animate uisng FuctAnimate
def animate(i):
    # get the current x values for planet and star
    x = [xs_anim[i], xp_anim[i]]
    
    # scale down to domain and find which pixels these lie in
    # NB y index is always half way up
    index_s = np.floor((x[0] + dom)/p_width)
    index_p = np.floor((x[1] + dom)/p_width)
    index_s = index_s.astype(int) # change them to integers
    index_p = index_p.astype(int)
    
    # add the central dot to the image:
    image_s[index_s, int(size/2), :] = 1
    image_s[index_p, int(size/2), :] = 1

    # replot the image and time text
    plot = ax.imshow(image_s)
    time_text.set_text(timer % (i*dt/year), color='white')
    
    return plot, time_text


# Animate the result
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(solution)),
                              interval=25, blit=True, init_func=init)


# for all time find the CoM position in x and plot to check
# should not change from 0
x_cm = (M*xs_anim + m*xp_anim)/(M + m)
plt.figure()
plt.plot(x_cm)
