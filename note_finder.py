#Morgan Note Finder

import numpy as np
import matplotlib.pyplot as plt
import math
import pyaudio
import wave

def note_finder(f):
	a = 2.0**(1.0/12.0)
	A4 = 440.0
	arg = abs(f)/A4
	step = round(math.log(arg,a))
	octave = round(step/12)
	relativeStep = np.mod(step, 12)
	note = notes[int(relativeStep)]
	return step, note, octave

def example_notes(t):
	freq1 = 23.12
	freq2 = 2217.46
	freq3 = 622.25
	#y = 2*np.sin(freq1*2*np.pi*t) + np.sin(freq2*2*np.pi*t) + np.sin(freq3*2*np.pi*t)
	y = np.sin(freq2*2*np.pi*t)
	return y


notes = ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab']

samplerate = 44100.0
recordLength = 1e4
t = np.linspace(0, recordLength/samplerate, recordLength)
y = example_notes(t)

yf = abs(np.fft.fft(y))/recordLength
f = np.fft.fftfreq(yf.size, d=1/samplerate)
np.fft.fftshift(f)

max_freq = np.argmax(yf)
max_amp = np.amax(yf)
step, note, octave = note_finder(f[max_freq])
print('Strongest signal level: {}'.format(max_amp))
print('Frequency of strongest signal: {}'.format(f[max_freq]))
print('Half steps from A4: {}'.format(step))
print('Note name: {}\nOctaves from A4: {}'.format(note, octave))

"""
!!!ignore this!!!

filename = 'E:\\testsignal_1.wav'
write_file = open(filename, 'w')
#write_file.setparams((1,1,samplerate,0,'NONE','not compressed'))
write_file.write(y.tostring())
write_file.close()
"""

plt.plot(f,yf)
plt.xlim([0,10e3])
plt.show()
