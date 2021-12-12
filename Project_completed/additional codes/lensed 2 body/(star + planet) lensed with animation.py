'''

pixelated sun and earth in 2D orbit, projected to 1D and lensed with animation

extracts found radius of planet to star (changed from true by lensing)

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import scipy
import project.lensing_function as lensing
import Project_completed.modules.class_2body as bodies
import Project_completed.modules.draw_pixels as pix_draw
import matplotlib.widgets as widgets
from scipy.signal import find_peaks

# %%


# define function to quit animation when button is pressed
def quit_resp(event):
    '''
    Stops the looping animation
    '''
    global switchoff
    # set the exiting loop variable to break
    switchoff = True
    # close the window
    plt.close()


# start up an empty source image and lensing parametrers
size = 200
eps = 0
rc = 0.15
dom = 6
year = 3.156e7
maxR = 1.49e11  # AU in SI
size_source = 2.5e11  # size of the source plane, in SI distacnes

# get pixel size to scale down from full animation to reduced coords
p_width = size_source/size

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

# set up a figure and axis on which to plot the resulting simulation
fig = plt.figure()
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
ax.set_xlim(-size_source, size_source)
ax.set_ylim(-size_source, size_source)
plt.sca(ax)
plt.xticks([])  # take off the axis ticks for both, no need for images
plt.yticks([])
ax.set_aspect('equal')

# set up axis for timer
ax_time = plt.axes([0.01, 0.05, 0.18, 0.05])
ax_time.axes.xaxis.set_visible(False)  # turn off axis visuals for the timer
ax_time.axes.yaxis.set_visible(False)

# set up a button to stop the aniation
ax_quit = plt.axes([0.85, 0.85, 0.1, 0.1])
offHandle = widgets.Button(ax_quit, 'QUIT')
offHandle.on_clicked(quit_resp)

# set up a timer and draw it on with nothing in it initially
timer = 'time = %.1f yr'
ax_time.text(0.05, 0.01, '', transform=ax.transAxes)

# set a stopping variable
switchoff = False

# loop over the simulation result values and plot as animation, wiht pixels
for t_index in range(len(t_arr)):
    
    # clear axis, reset the image and get current x values for planet and star
    ax.cla()
    ax_time.cla()
    image_s = np.zeros((size, size, 3))
    x = [xs_anim[t_index], xp_anim[t_index]]
    
    # scale down to domain and find which pixels these lie in
    # NB y index is always half way up
    index_s = np.floor((x[0] + size_source/2)/p_width)
    index_p = np.floor((x[1] + size_source/2)/p_width)
    index_s = index_s.astype(int).transpose() # change them to integers
    index_p = index_p.astype(int).transpose()
    
    # initial checker: (if planet is in front when in line of star), using the y data
    pfront = True
    if abs(index_s + Star.size) > abs(index_p - Planet.size) and abs(index_s - Star.size) < abs(index_p + Planet.size):
        if yp_anim[t_index] > ys_anim[t_index]:
            pfront = False
    
    # draw on the star as a big, white circle, use prepared function.
    image_s = pix_draw.draw_sphere(Star.size, image_s, index_s, (255, 255, 255))
    
    # draw on the planet as a smaller, dark circle, if not behind star
    if pfront:
        image_s = pix_draw.draw_sphere(Planet.size, image_s, index_p, (0, 0, 0))
    
    # lens the created image and update total luminosity for this iteration
    image_lens = lensing.lens(image_s, rc, eps, dom)
    lumin_bol.append(np.sum(image_lens/255))
    
    # plot the lensed image and the new time
    ax.imshow(image_lens/255)
    ax_time.text(0.01, 0.2, 'time = {:.2f} yrs'.format(t_arr[t_index]/year))
    
    # check the quit command:
    if switchoff:
        break
    
    # pause to update plot:
    plt.pause(0.001)


# set up a figure, axis and visuals for the light curve
fig_lc = plt.figure()
ax_lc = fig_lc.gca()
ax_lc.set_xlabel('time [years]')
ax_lc.set_ylabel(r'$L_{bol} [RGB \ sum]$')

# plot the obtained light curve:
ax_lc.plot(t_arr[:len(lumin_bol)]/year, lumin_bol)

# turn resulting lists into arrays to slice
lumin_bol = np.array(lumin_bol)

# from dip sizes get Radii for each and print
ratio = (lumin_bol[0] - np.min(lumin_bol))/lumin_bol[0]
print('\n')
print('The True (Ratio of radii)^2 true is: {:.4f}'.format((Planet.size/Star.size)**2))
print('Found (Ratio of radii)^2 when lensed = {:.4f}'.format(ratio))
print('\n')


# %%

# Extra plots for functionality tests

# for all time find the CoM position in x and plot to check
# should not change from 0
x_cm = (Star.Mass*xs_anim + Planet.Mass*xp_anim)/(Star.Mass + Planet.Mass)
fig_cm = plt.figure()
ax_cm = fig_cm.gca()
ax_cm.set_xlabel('time step index')
ax_cm.set_ylabel(r'$x_{cm}$')
ax_cm.plot(x_cm)

# plot the motion of the two objects in the x-y plane
plt.figure()
plt.plot(xs_anim, ys_anim)
plt.plot(xp_anim, yp_anim)




