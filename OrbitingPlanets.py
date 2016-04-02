#!/usr/bin/env python3
#units of velocity are in m/s
#units of distance are in m

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

def calculate_positions(bodies):
    """([Body])

    Never returns; loops through the simulation, updating the
    positions of all the provided bodies.
    """
    timestep = 3600  # One hour in seconds
    num_steps = int(1.1e3)
    print('Calculating orbital paths over a period of {} tellurian hours...'.format(num_steps))

    for step in xrange(num_steps): #columns
        #update graph every 1000 days
        if (step>0) and (step%1000 == 0):
            for body in bodies:
                plt.plot(body.pxvector,body.pyvector, body.color)
                body.pxvector = [body.px]
                body.pyvector = [body.py]
        #update_info(step, bodies)
        force = {}
        for body in bodies:   #rows
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in bodies:
                # Don't calculate the body's attraction to itself
                if body is other:
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy

            body.vx += total_fx/body.mass*timestep
            body.vy += total_fy/body.mass*timestep
            body.px += body.vx*timestep
            body.py += body.vy*timestep
            body.pxvector.append(body.px)
            body.pyvector.append(body.py)
    plt.show()

def main():
    sun = heavenly_body(name='Sun', mass=1.98892e30)
    mercury = heavenly_body(name='Mercury', mass=0.3301e24, pos=(-.387*AU,0), vel=(0,47.36e3), color='black')
    venus = heavenly_body(name='Venus', mass=4.8685e24, pos=(-.723*AU,0), vel=(0,-35.02e3), color='orange')
    earth = heavenly_body(name='Earth', mass=5.9742e24, pos=(-1*AU,0), vel=(0,29.783e3), color='blue')
    moon = heavenly_body(name='Moon', mass=7.3478e22, pos=(-1.00257*AU,0), vel=(0,(1.0224e3+29.783e3)), color='gray')
    mars = heavenly_body(name='Mars', mass=.64171e24, pos=(-1.524*AU,0), vel=(0,24.07e3), color='red')
    jupiter = heavenly_body(name='Jupiter', mass=1898.19e24, pos=(-5.204*AU,0), vel=(0,13.06e3), color='magenta')
    saturn = heavenly_body(name='Saturn', mass=568.34e24, pos=(-9.582*AU,0), vel=(0,9.6e3), color='green')
    uranus = heavenly_body(name='Uranus', mass=86.813e24, pos=(-19.201*AU,0), vel=(0,6.8e3), color='brown') #haha
    neptune = heavenly_body(name='Neptune', mass=102.413e24, pos=(-30.047*AU,0), vel=(0,5.43e3), color='aquamarine')
    pluto = heavenly_body(name='Pluto', mass=0.01303e24, pos=(-39.482*AU,0), vel=(0,4.74e3), color='purple')

    bodies = [sun, mercury, venus, earth, moon]#, mars, jupiter, saturn, uranus, neptune, pluto]
    calculate_positions(bodies)

if __name__ == '__main__':
    main()