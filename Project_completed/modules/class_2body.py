'''

define classes to be used in setting up and solving 2 body problems

@author: Maciej Tomasz Jarema ppymj11

'''

import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import integrate

# %%


# deifne a function that will set up a class instance of a single body
def body_def(Mass, size, x, y, vx, vy):
    class body():
        def __init__(self, Mass, size, x, y, vx, vy):
            assert Mass >= 0, 'Mass must be positive'
            assert size >= 0, 'size must be positive'
            self.Mass = Mass
            self.size = size
            self.pos = [x, y]
            self.vel = [vx, vy]
        
        
        def size_up(self):
            '''
            Increases body size by 1
            '''
            self.size += 1
    
    # run the class and return the instance of it to user
    instance = body(Mass, size, x, y, vx, vy)
    return instance


# define a function that will set up a class instance for a system of bodies
# for any number of input bodies
def system_def(*bodies):
    class system():
        def __init__(self, *bodies):
            # define system for however many bodies were input
            i = 0
            for body in [*bodies]:
                exec('self.body' + str(i) + ' = body')
                i += 1
            
            self.init = []  # list of initial parameters, to be generated
            self.length = i  # number of bodies
        
        # define a method to set up initials from all bodies:
        def initials(self):
            '''
            Takes no inputs, returns no outputs
            Sets up the intiial ocnditions of the system of bodies
            Stores these in the system isnatance that it acts on
            '''
            # append positions of each body
            for n in range(self.length):
                exec('self.init.extend(self.body' + str(n) + '.pos)')
            
            # append velocoties of each body
            for n in range(self.length):
                exec('self.init.extend(self.body' + str(n) + '.vel)')
        
        # define a function for the jacobian of this system:
        # this will be used by odeint, only for 2D, 2 body
        def jacobian_get(self, y, x):
            '''
            Acts as function for odeint to get derivatives for motion.
            takes in odeint array of variables and returns its derivastives
            the order is set by set up initial condition in system instance
            
            Only works for 2 bodies in 2D
            could generalise but no need for this investigation
            '''
            # grav constant
            G = 6.67e-11
            
            # extract masses for easier reading
            M = self.body0.Mass
            m = self.body1.Mass
            
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
    
    # run the class and return the instance of it to user
    instance = system(*bodies)
    return instance


# #############################################################################
# example for how to use these
# #############################################################################


# Example of use:
if __name__ == '__main__':
    # define parameters for body 1:
    M1 = 2e30
    size1 = 20
    x1 = 0
    y1 = 0
    vx1 = 0
    vy1 = 0
    
    # set up a class instance for body 1:
    body_1 = body_def(M1, size1, x1, y1, vx1, vy1)
    
    # same for body 2:
    M2 = 6e24
    size2 = 6
    x2 = 1.496e11
    y2 = 0
    vx2 = 0
    vy2 = -29800
    body_2 = body_def(M2, size2, x2, y2, vx2, vy2)
    
    # run it with the above two bodies
    system_1 = system_def(body_1, body_2)
    system_1.initials()
    
    # set up simualtion time parameters
    year = 3.156e7  # numerical factor
    t_max = 1 * year
    t_number = 400
    t_arr = np.linspace(0, t_max, t_number)
    dt = t_arr[-1] - t_arr[-2]
    
    # call odeint to solve it:
    solution = scipy.integrate.odeint(system_1.jacobian_get, system_1.init, t_arr)
    
    # from it extract wanted positions
    xs_anim = solution[:, 0]
    xp_anim = solution[:, 2]
    
    ys_anim = solution[:, 1]
    yp_anim = solution[:, 3]
    
    # plot the motion of the two objects in the x-y plane
    fig = plt.figure()
    ax = fig.gca()
    ax.set_aspect('equal')
    ax.set_xlabel(r'$x \ [m]$')
    ax.set_ylabel(r'$y \ [m]$')
    ax.set_title('Simulation of Earth\'s orbit')
    plt.plot(xs_anim, ys_anim, 'ro')
    plt.plot(xp_anim, yp_anim, 'k-')
