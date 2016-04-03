"""
Orbiting Planets: 
Calculates and plots orbits of planets in 
the solar system using the DOPRI5 method
!!!Complete Rewrite!!!
Author: Michael Horstkoetter 
        Morgan Allison
        Jacob See
Date Created: 3/16
Date edited: 4/16
Windows 8 64-bit/Mac OSX v ???
Python 2.7.11 64-bit (Miniconda 4.0.5)
NumPy 1.10.4, MatPlotLib 1.4.3
To get Anaconda/Miniconda: http://continuum.io/downloads
Miniconda includes NumPy and MatPlotLib
"""
#units of velocity are in m/s
#units of distance are in m

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode

# The gravitational constant G
G = 6.67428e-11

#No need to worry about scale
AU = 149.6e6*1000   # 149.6 million km, in meters.

class HeavenlyBody:
    #in case you want to add other initial conditions
    def __init__(self, name='planet', mass=0, px=0, py=0, vx=0, vy=0, color='k'):
        self.name = name
        self.mass = mass
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.pxvector = [self.px]
        self.pyvector = [self.py]
        self.color = color

    def generate_x_params(self, other):
        positionParams = [self.px, other.px, self.mass, other.mass, ]

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

        return np.array([fx, fy])

def x_function(t, px, fx, mass):
    px += (fx/mass*t)*t
    return px

def y_function(t, py, fy, mass):
    py += (fy/mass*t)*t
    return py

def main():
    sun = HeavenlyBody(name='Sun', mass=1.98892e30)
    mercury = HeavenlyBody(name='Mercury', mass=0.3301e24, px=-.387*AU, vy=47.36e3, color='black')
    venus = HeavenlyBody(name='Venus', mass=4.8685e24, px=-.723*AU, vy=-35.02e3, color='orange')
    earth = HeavenlyBody(name='Earth', mass=5.9742e24, px=-1*AU, vy=29.783e3, color='blue')
    moon = HeavenlyBody(name='Moon', mass=7.3478e22, px=-1.00257*AU, vy=(1.0224e3+29.783e3), color='gray')
    mars = HeavenlyBody(name='Mars', mass=.64171e24, px=-1.524*AU, vy=24.07e3, color='red')
    jupiter = HeavenlyBody(name='Jupiter', mass=1898.19e24, px=-5.204*AU, vy=13.06e3, color='magenta')
    saturn = HeavenlyBody(name='Saturn', mass=568.34e24, px=-9.582*AU, vy=9.6e3, color='green')
    uranus = HeavenlyBody(name='Uranus', mass=86.813e24, px=-19.201*AU, vy=6.8e3, color='brown') #haha
    neptune = HeavenlyBody(name='Neptune', mass=102.413e24, px=-30.047*AU, vy=5.43e3, color='aquamarine')
    pluto = HeavenlyBody(name='Pluto', mass=0.01303e24, px=-39.482*AU, vy=4.74e3, color='purple')

    bodies = [sun, mercury, venus, earth, moon]#, mars, jupiter, saturn, uranus, neptune, pluto]
    t = 0
    dt = 3600  # One hour in seconds
    numSteps = int(1.1e3)
    print('Calculating orbital paths over a period of {} tellurian hours...'.format(numSteps))
    
    for i in xrange(numSteps):
        if (i>0) and (i%1000 == 0):
            for body in bodies:
                plt.plot(body.pxvector,body.pyvector, body.color)
                body.pxvector = [body.px]
                body.pyvector = [body.py]
        for body in bodies:   #rows
            # Add up all of the forces exerted on 'body'.
            fx = fy = 0.0
            dopri_x = ode(x_function).set_integrator('dopri5', method='adams')
            dopri_x.set_f_params(body.px, fx, body.mass)
            dopri_x.set_initial_value(body.px)

            dopri_y = ode(y_function).set_integrator('dopri5', method='adams')
            dopri_y.set_f_params(body.py, fy, body.mass)
            dopri_y.set_initial_value(body.py)
            for other in bodies:
                # Don't calculate the body's attraction to itself
                if body is other:
                    continue
                f = body.attraction(other)
                fx += f[0]
                fy += f[1]
            px = dopri_x.integrate(dopri_x.t+dt, dt)
            py = dopri_y.integrate(dopri_y.t+dt, dt)
            print(dopri_x.successful())
            print(dopri_y.successful())

            body.pxvector.append(px)
            body.pyvector.append(py)
    plt.show()

if __name__ == '__main__':
    main()