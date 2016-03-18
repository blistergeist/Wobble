#!/usr/bin/env python3

import math
from turtle import *

# The gravitational constant G
G = 6.67428e-11

# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 50 / AU

class Body(Turtle):
    """Subclass of Turtle representing a gravitationally-acting body.

    Extra attributes:
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m
    """
    
    name = 'Body'
    mass = None
    vx = vy = 0.0
    px = py = 0.0
    
    def attraction(self, other):
        """(Body): (fx, fy)

        Returns the force exerted upon this body by the other body.
        """
        # Report an error if the other object is the same as this one.
        if self is other:
            raise ValueError("Attraction of object %r to itself requested"
                             % self.name)

        # Compute the distance of the other body.
        sx, sy = self.px, self.py
        ox, oy = other.px, other.py
        dx = (ox-sx)
        dy = (oy-sy)
        d = math.sqrt(dx**2 + dy**2)

        # Report an error if the distance is zero; otherwise we'll
        # get a ZeroDivisionError exception further down.
        if d == 0:
            raise ValueError("Collision between objects %r and %r"
                             % (self.name, other.name))

        # Compute the force of attraction
        f = G * self.mass * other.mass / (d**2)

        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        return fx, fy

def update_info(step, bodies):
    """(int, [Body])
    
    Displays information about the status of the simulation.
    """
    print('Step #{0}'.format(step))
    for body in bodies:
        s = '{0:<8}  Pos.={1:>6.2f} {2:>6.2f} Vel.={3:>10.3f} {4:>10.3f}'.format(
            body.name, body.px/AU, body.py/AU, body.vx, body.vy)
        print(s)
    print()

def loop(bodies):
    """([Body])

    Never returns; loops through the simulation, updating the
    positions of all the provided bodies.
    """
    timestep = 24*3600  # One day
    
    for body in bodies:
        body.penup()
        body.hideturtle()

    step = 1
    while True:
        update_info(step, bodies)
        step += 1

        force = {}
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

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

        # Update velocities based upon on the force.
        for body in bodies:
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            # Update positions
            body.px += body.vx * timestep
            body.py += body.vy * timestep
            body.goto(body.px*SCALE, body.py*SCALE)
            body.dot(3)


def main():
    sun = Body()
    sun.name = 'Sun'
    sun.mass = 1.98892 * 10**30
    sun.pencolor('black')

    mercury = Body()
    mercury.name = 'Mercury'
    mercury.mass = 0.33011 * 10**24 #Planet Mass
    mercury.px = -0.387 * AU        #Ratio Semimajor axis
    mercury.vy = 47.36 * 1000       #Planet Mean orbital velocity (km/s)
    mercury.pencolor('purple')

    # Venus parameters taken from
    # http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
    venus = Body()
    venus.name = 'Venus'
    venus.mass = 4.8685 * 10**24
    venus.px = -0.723 * AU
    venus.vy = 35.02 * 1000
    venus.pencolor('grey')

    earth = Body()
    earth.name = 'Earth'
    earth.mass = 5.9742 * 10**24
    earth.px = -1 * AU
    earth.vy = 29.783 * 1000            # 29.783 km/sec
    earth.pencolor('blue')

    mars = Body()
    mars.name = 'Mars'
    mars.mass = 0.64171 * 10**24 #Planet Mass
    mars.px = -1.524 * AU        #Ratio Semimajor axis
    mars.vy = 24.07 * 1000       #Planet Mean orbital velocity (km/s)
    mars.pencolor('red')

    jupiter = Body()
    jupiter.name = 'Jupiter'
    jupiter.mass = 1898.19 * 10**24 #Planet Mass
    jupiter.px = -5.204 * AU        #Ratio Semimajor axis
    jupiter.vy = 13.06 * 1000       #Planet Mean orbital velocity (km/s)
    jupiter.pencolor('brown')

    saturn = Body()
    saturn.name = 'Saturn'
    saturn.mass = 568.34 * 10**24 #Planet Mass
    saturn.px = -9.582 * AU        #Ratio Semimajor axis
    saturn.vy = 9.68 * 1000       #Planet Mean orbital velocity (km/s)
    saturn.pencolor('tan')

    uranus = Body()
    uranus.name = 'Uranus'
    uranus.mass = 86.813 * 10**24 #Planet Mass
    uranus.px = -19.201 * AU        #Ratio Semimajor axis
    uranus.vy = 6.80 * 1000       #Planet Mean orbital velocity (km/s)
    uranus.pencolor('blue')

    neptune = Body()
    neptune.name = 'Neptune'
    neptune.mass = 102.413 * 10**24 #Planet Mass
    neptune.px = -30.047 * AU        #Ratio Semimajor axis
    neptune.vy = 5.43 * 1000       #Planet Mean orbital velocity (km/s)
    neptune.pencolor('blue')

    pluto = Body()
    pluto.name = 'Pluto'
    pluto.mass = 0.01303 * 10**24 #Planet Mass
    pluto.px = -39.482 * AU        #Ratio Semimajor axis
    pluto.vy = 4.67 * 1000       #Planet Mean orbital velocity (km/s)
    pluto.pencolor('orange')

    loop([sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto])

if __name__ == '__main__':
    main()