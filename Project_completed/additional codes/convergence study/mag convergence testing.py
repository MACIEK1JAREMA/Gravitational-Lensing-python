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
rc = 0.7
eps = 0
dom = 1  # abs() of domain of r values (normally -1, 1 --> 1)

# set the initial size and maximum. To conserve pixel size, will split each
# at each step upto 'splits'
initial_img = 19
init_N = 19  # multpile of initial img
N_max = 1200
splits = N_max//init_N

# set up array to store number of pixels for eahc of these:
N_ends = []

# set up lists to store wnated data
sizes = []  # used image sizes
odds = []  # magnification for odd size images
odds_n = []  # tried odd image sizes
evens = []
evens_n = []


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
    N_ends.append(N_end/initial_img)
    sizes.append(N)
    
    # appedn to odds and evens depending on orig image:
    if initial_img % 2 == 1:
        if msplit % 2 == 1:
            odds.append(N_end/initial_img)
            odds_n.append(N)
        else:
            evens.append(N_end/initial_img)
            evens_n.append(N)
    else:
        evens.append(N_end/initial_img)
        evens_n.append(N)
    
    # save some figures for iset plots
    if msplit == 1:
        plt.figure()
        plt.imshow(image_l*255)
        image_save1 = image_l
    elif msplit == 20:
        plt.figure()
        plt.imshow(image_l*255)
        image_save2 = image_l
    elif msplit == 21:
        plt.figure()
        plt.imshow(image_l*255)
        image_save3 = image_l
    elif msplit == 40:
        plt.figure()
        plt.imshow(image_l*255)
        image_save4 = image_l


# set up figure, axia and visuals
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.tick_params(labelsize=20)
ax2.tick_params(labelsize=20)
ax1.set_xlabel(r'$N \ [pixels]$', fontsize=20)
ax1.set_ylabel(r'$M \ = \ L_{f} \ / \ L_{i}$', fontsize=20)
ax2.set_xlabel(r'$N$', fontsize=20)
ax2.set_ylabel(r'$100 \ \delta M \ [ \% \ error]$', fontsize=20)

# plot
#ax1.plot(sizes, N_ends, 'k')
ax1.plot(odds_n, odds, 'r')
ax1.plot(evens_n, evens, 'b')
ax1.plot(evens_n[20], evens[20], 'g*')

# magnification convergence value and its confidence interval

# get fractional changes in magnification between each iteration
change = abs((np.diff(N_ends) / N_ends[:-1])*100)
change_odd = abs((np.diff(odds) / odds[:-1])*100)
change_even = abs((np.diff(evens) / evens[:-1])*100)

#ax2.plot(sizes[1:], change)
ax2.plot(odds_n[1:], change_odd)
ax2.plot(evens_n[1:], change_even)

# horizontals at 2% and 1% for reference:
ax2.plot(sizes[1:], np.ones(np.shape(sizes[1:])) * 1, 'g-.')
ax2.plot(sizes[1:], np.ones(np.shape(sizes[1:])) * 2, 'r-.')

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')

# %%

plt.imshow(image_save1)
plt.imshow(image_save2)
plt.imshow(image_save3)

# %%

# print last results
print('last value of magnification for odd images was: {:5f}'.format(odds[-1]))
print('with error {:.2f} %'.format(abs(change_odd[-1])))
print('\n')
print('last value of magnification for even images was: {:5f}'.format(evens[-1]))
print('with error {:.2f} %'.format(abs(change_even[-1])))
print('\n')

print('value of magnification at 1% error for odd images was: {:5f}'.format(odds[np.where(np.array(change_odd) <= 1)[0][0]]))
print('occuring at N = ' + str(odds_n[np.where(np.array(change_odd) <= 1)[0][0]]))
print('value of magnification at 1% error for even images was: {:5f}'.format(evens[np.where(np.array(change_even) <= 1)[0][0]]))
print('occuring at N = ' + str(evens_n[np.where(np.array(change_even) <= 1)[0][0]]))
print('\n')

print('difference between odds and evens was {:.5f}'.format(abs(odds[-1] - evens[-1])))
print('with error {:.5f} %'.format(np.sqrt(change_odd[-1]**2 + change_even[-1]**2)))

# return time to run
stop = timeit.default_timer()
print('Time to run was: {:.4f}'.format(stop - start) + ' s')
