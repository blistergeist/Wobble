#!/usr/bin/env python3
from scipy.inegrate import ode
import numpy as np
import matplotlib.pyplot as plt

# The gravitational constant G
G = 6.67428e-11

#No need to worry about scale
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.

class heavenly_body:
    #pos and vel should both be tuples, e.g. (0, 3)
    #in case you want to add other initial conditions
    def __init__(self, name='yar', mass=0, pos=(0,0), vel=(0,0), color='k'):
        self.name = name
        self.mass = mass
        self.px, self.py = pos
        self.vx, self.vy = vel
        self.pxvector = [self.px]
        self.pyvector = [self.py]
        self.color = color

    def attraction(self, other):
        # Report an error if the other object is the same as this one.
        if self is other:
            raise ValueError("Attraction of object %r to itself requested" % self.name)
        dx = other.px-self.px
        dy = other.py-self.py
        d = np.sqrt(dx**2 + dy**2)
        if d == 0:
            raise ValueError("Collision between objects %r and %r" % (self.name, other.name))
        
        # Compute the force of attraction
        f = G*self.mass*other.mass/(d**2)

        # Compute the direction of the force.
        theta = np.arctan2(dy, dx)
        fx = np.cos(theta) * f
        fy = np.sin(theta) * f
        return fx, fy

def update_info(step, bodies):
    """(int, [Body])
    
    Displays information about the status of the simulation.
    """
    print('Step #{0}'.format(step))
    for body in bodies:
         print('{0:<8}  Pos.={1:>6.2f} {2:>6.2f} Vel.={3:>10.3f} {4:>10.3f}'.format(
            body.name, body.px/AU, body.py/AU, body.vx, body.vy))
    print('\n')

def draw_orbits():
    plt.plot(sun.pxvector, sun.pyvector, 'black')
    plt.plot(mercury.pxvector, mercury.pyvector, 'orange')
    plt.plot(earth.pxvector, earth.pyvector, 'blue')
    plt.plot(venus.pxvector, venus.pyvector, 'yellow')
    plt.plot(mars.pxvector, mars.pyvector, 'red')
    plt.plot(jupiter.pxvector, jupiter.pyvector, 'magenta')
    plt.plot(saturn.pxvector, saturn.pyvector, 'green')
    plt.plot(uranus.pxvector, uranus.pyvector, 'brown')#haha
    plt.plot(neptune.pxvector, neptune.pyvector, 'aquamarine')
    plt.plot(pluto.pxvector, pluto.pyvector, 'purple')
    plt.show()

def calculate_positions(bodies):
    """([Body])

    Never returns; loops through the simulation, updating the
    positions of all the provided bodies.
    """
    timestep = 60  # One day in seconds
    num_steps = int(1e5)
    print('Calculating orbital paths over a period of {} tellurian days...'.format(num_steps))

   

def dopri_function(timestep, bodyInfo):
            vx += total_fx/mass*timestep
            vy += total_fy/mass*timestep
            px += vx*timestep
            py += vy*timestep
            
            return px, py

"""body.pxvector.append(body.px)
body.pyvector.append(body.py)
plt.show()"""


def main():
    sun = heavenly_body(name='Sun', mass=1.98892e30)
    mercury = heavenly_body(name='Mercury', mass=0.3301e24, pos=(-.387*AU,0), vel=(0,47.36e3), color='black')
    venus = heavenly_body(name='Venus', mass=4.8685e24, pos=(-.723*AU,0), vel=(0,35.02e3), color='orange')
    earth = heavenly_body(name='Earth', mass=5.9742e24, pos=(-1*AU,0), vel=(0,29.783e3), color='blue')
    themoon = heavenly_body(name='The Moon', mass=7.34767309e22, pos=(-1*AU-0.00257*AU,0), vel=(0,29.783e3+1.022e3), color='grey')
    mars = heavenly_body(name='Mars', mass=.64171e24, pos=(-1.524*AU,0), vel=(0,24.07e3), color='red')
    jupiter = heavenly_body(name='Jupiter', mass=1898.19e24, pos=(-5.204*AU,0), vel=(0,13.06e3), color='magenta')
    saturn = heavenly_body(name='Saturn', mass=568.34e24, pos=(-9.582*AU,0), vel=(0,9.6e3), color='green')
    uranus = heavenly_body(name='Uranus', mass=86.813e24, pos=(-19.201*AU,0), vel=(0,6.8e3), color='brown') #haha
    neptune = heavenly_body(name='Neptune', mass=102.413e24, pos=(-30.047*AU,0), vel=(0,5.43e3), color='aquamarine')
    pluto = heavenly_body(name='Pluto', mass=0.01303e24, pos=(-39.482*AU,0), vel=(0,4.74e3), color='purple')

    bodies = [sun, mercury, venus, earth, themoon] #, mars, jupiter, saturn, uranus, neptune, pluto]
    bodyInfo = [body.vx, body.vy, body.px, body.py, body.mass]
    integrate_dat_bitch = ode(dopri_function).set_integrator('dopri5', method='adams')
    integrate_dat_bitch.set_f_params(bodyInfo)
    integrate_dat_bitch.set_initial_value()
    #calculate_positions(bodies)
    for step in xrange(num_steps): #columns
        #update graph every 1000 days
        for body in bodies:
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in bodies:
                # Don't calculate the body's attraction to itself
                if body is other:
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy


    """
    plt.plot(sun.pxvector, sun.pyvector, 'black')
    plt.plot(mercury.pxvector, mercury.pyvector, 'orange')
    plt.plot(earth.pxvector, earth.pyvector, 'blue')
    plt.plot(venus.pxvector, venus.pyvector, 'yellow')
    plt.plot(mars.pxvector, mars.pyvector, 'red')
    plt.plot(jupiter.pxvector, jupiter.pyvector, 'magenta')
    plt.plot(saturn.pxvector, saturn.pyvector, 'green')
    plt.plot(uranus.pxvector, uranus.pyvector, 'brown')#haha
    plt.plot(neptune.pxvector, neptune.pyvector, 'aquamarine')
    plt.plot(pluto.pxvector, pluto.pyvector, 'purple')
    plt.show()
    """

if __name__ == '__main__':
    main()