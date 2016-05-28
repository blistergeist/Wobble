"""
DOPRI5 Test:Simple proof of concept for the DOPRI5 
			integration method using the flight of a ball
Author: Morgan Allison
Date Created: 5/16
Date edited: 5/16
Windows 8 64-bit
Python 2.7.11 64-bit (Miniconda 4.0.5)
NumPy 1.10.4, MatPlotLib 1.4.3
To get Anaconda/Miniconda: http://continuum.io/downloads
Miniconda includes NumPy and MatPlotLib
"""

import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
import time

def eulerMethod():
	"""################ EULER METHOD ################"""
	gravity = -9.81 #m/s2
	xInitialPos = 0.0 #m
	yInitialPos = 0.0 #m
	xInitialVel = 10.0 #m/s
	yInitialVel = 10.0 #m/s
	xInitialAcc = 0.0 #m/s
	yInitialAcc = gravity

	timeRes = 100
	timeArray = np.linspace(0,5,timeRes)

	yPosE = np.zeros(timeRes)
	xPosE = np.zeros(timeRes)

	#calculate x and y positions from original velocities
	start = time.clock()
	for i in range(timeRes):
		xPosE[i] = xInitialPos + xInitialVel*timeArray[i] + 0.5*xInitialAcc*timeArray[i]**2
		if (i > 1) and (yPosE[i-1] <= 0):
			yPosE[i] = 0
		else:
			yPosE[i] = yInitialPos + yInitialVel*timeArray[i] + 0.5*yInitialAcc*timeArray[i]**2
	end = time.clock()
	elapsed = end-start
	print('Elapsed time for Euler: {} seconds'.format(elapsed))

	return xPosE, yPosE

def calcPos(t, currentPos):
	gravity = -9.81 #m/s^2
	xLastPos = currentPos[0] #m
	yLastPos = currentPos[1] #m
	xInitialVel = 1.0 #m/s
	yInitialVel = 10.0 #m/s
	xInitialAcc = 0.0 #m/s
	yInitialAcc = gravity
	
	xPos = 0 + xInitialVel*t + 0.5*xInitialAcc*t**2
	if t > .001 and yLastPos <= 0:
		yPos = 0
	else:
		yPos = 0 + yInitialVel*t + 0.5*yInitialAcc*t**2

	return np.array([xPos, yPos])

def dopriMethod():
	"""################ DOPRI5 METHOD ################"""
	#define function to integrate
	#t is current time, y is current variable values
	t0 = 0.0
	t1 = 5.0
	dt = 0.1
	y0 = [0.0,0.0]
	xPosD = []
	yPosD = []
	posD = []

	dopriPos = ode(calcPos).set_integrator('dopri5', method='adams')
	dopriPos.set_initial_value(y0, t0)
	while dopriPos.t < t1:
		posD = dopriPos.integrate(dopriPos.t+dt, dt)
		#print('DOPRI5 Time: {}'.format(dopriPos.t))
		#print('DOPRI5 Positions: x => {} y => {}'.format(posD[0], posD[1]))
		xPosD.append(posD[0])
		yPosD.append(posD[1])

	return xPosD, yPosD

def main():
	xPosE, yPosE = eulerMethod()
	xPosD, yPosD = dopriMethod()

	"""################ PLOT ################"""
	plt.figure(1)
	plt.subplot(121, axisbg='k')
	eulerAxes, = plt.plot(xPosE,yPosE, 'y')
	plt.subplot(122)
	dopriAxes, = plt.plot(xPosD, yPosD)
	plt.show()

if __name__ == '__main__':
	main()