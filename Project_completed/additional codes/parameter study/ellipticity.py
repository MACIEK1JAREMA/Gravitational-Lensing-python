'''

parameter study, changing elipticity and observing results
also, plotting average magnification as ratio of initial and final luminosities

@author: Maciej Tomasz Jarema ppymj11

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import Project_completed.modules.lensing_function as lensing
import Project_completed.modules.draw_pixels as pix_draw
import timeit

# %%

# start the timer
start = timeit.default_timer()

# set up some parameters
rc = 0.2
dom = 4  # abs() of domain of r values (normally -1, 1 --> 1)
size = 400
size_obj = 30
eps = 0  # initial
eps_N = 200

# set up array of set eps:
eps_arr = np.linspace(0, 1, eps_N)

# set up a total luminosity list to store it for each ellipticity
lum_arr = []

# set up the source image, with centred, circular source, use written function
image_s = np.zeros([size, size, 3])
image_s = pix_draw.draw_sphere(size_obj, image_s, int(size/2), (255, 255, 255))

# loop over changing ellipticity, for each, lens and get total intensity:
for epsilon in eps_arr:
    # lens
    image_lens = lensing.lens(image_s, rc, epsilon, dom)
    
    # if its first or last, save for later inset plots:
    if epsilon == 0:
        img_l_start = image_lens/255
    elif epsilon == eps_arr[-1]:
        img_l_end = image_lens/255
    
    # update the total luminosty array with sum of all pizels with colours
    lum_arr.append(np.sum(image_lens/255))


# set up fiugre and axis:
fig = plt.figure()
ax = fig.gca()
ax.set_xlabel(r'$\epsilon$', fontsize=14)
ax.set_ylabel(r'$ Magnification \ L_{bol, lens} \ / \ L_{bol, init}$', fontsize=14)

# plot total bol lum after / intial , against used epsilon
ax.plot(eps_arr, lum_arr, 'b-')

# plot insets with saved images
d_eps = 0.7  # param to det size of inset in eps length-scales
d_lum = np.sum(image_s)/255  # in lum length-scales

inset_start = ax.inset_axes([eps_arr[0] - d_eps/2 + d_eps/10, lum_arr[0] - d_lum/2 - d_lum, d_eps, d_lum], transform=ax.transData)
inset_start.set_yticks([])
inset_start.set_xticks([])
inset_start.imshow(img_l_start)

inset_end = ax.inset_axes([eps_arr[-1] - d_eps/2 - d_eps/10, lum_arr[-1] - d_lum/2 + d_lum, d_eps, d_lum], transform=ax.transData)
inset_end.set_yticks([])
inset_end.set_xticks([])
inset_end.imshow(img_l_end)

# redo lensed images at interest points (at decline)
# and plot as inset plots
# NB start and end alreayd saved from orig loop

img_l_dec1 = lensing.lens(image_s, rc, 0.35, dom)/255
mid_ind1 = int(np.argmin(np.abs(eps_arr - 0.25)))  # get its index
inset_dec1 = ax.inset_axes([eps_arr[mid_ind1] - d_eps/2 +  d_eps/3, lum_arr[mid_ind1] - d_lum/2, d_eps, d_lum], transform=ax.transData)
inset_dec1.set_yticks([])
inset_dec1.set_xticks([])
inset_dec1.imshow(img_l_dec1)

img_l_dec2 = lensing.lens(image_s, rc, 0.65, dom)/255
mid_ind2 = int(np.argmin(np.abs(eps_arr - 0.75)))  # get its index
inset_dec2 = ax.inset_axes([eps_arr[mid_ind2] - d_eps/2, lum_arr[mid_ind2] - d_lum/2 + 1.2*d_lum, d_eps, d_lum], transform=ax.transData)
inset_dec2.set_yticks([])
inset_dec2.set_xticks([])
inset_dec2.imshow(img_l_dec2)

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
