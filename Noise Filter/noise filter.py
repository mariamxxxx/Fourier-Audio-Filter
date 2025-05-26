import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft


t = np.linspace(0,4,4*44100)

# octaves frequency
octave_3 = {'C': 130.81, 'D': 146.83, 'E': 164.81, 'F': 174.61, 'G': 196.00, 'A': 220.00, 'B': 246.94}
octave_4 = {'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23, 'G': 392.00, 'A': 440.00, 'B': 493.88}

# Notes of Twinkle Twinkle Little Star
melody_notes = ['C', 'C', 'G', 'G', 'A', 'A', 'G']
duration = 0.25  

# generate ti
start_times = []
current_time = 0
for _ in melody_notes:
    start_times.append(current_time)
    current_time += 0.5 

# initialize signal
x = np.zeros(len(t))

# Unit step function
def unit_step(t):
    return np.where(t >= 0, 1, 0)

# generate signal
for i in range(len(melody_notes)):
    ti = start_times[i]
    Ti = duration
    fi = octave_4[melody_notes[i]]  
    Fi = octave_3[melody_notes[i]]  

    unit = unit_step(t - ti) - unit_step(t - ti - Ti)
    x += ((np.sin(2 * np.pi * fi * t) + np.sin(2 * np.pi * Fi * t)) * unit) 

#-------------------------------------------------------------------------------------------------------------
N = 4*44100
f= np.linspace(0,44100/2,int(N/2))

#frequency domain
x_f = fft(x)
x_f = 2/N * np.abs(x_f [0:int(N/2)])

#noise
fn1 , fn2 = np. random. randint(0, 44100/2, 2)
n = np.sin(2*np.pi*fn1*t)+np.sin(2*np.pi*fn2*t)

#noise frequency
xn = x+n
xn_f = fft(xn)
xn_f = 2/N * np.abs(xn_f [0:int(N/2)])

#--------------------------------------------------------------------------------------------------------------
#filtering
threshold = np.max(x_f) + 0.1 

z = np.where(xn_f > threshold)[0]
for i in range (len(z)):
    z[i]=f[z[i]]

#extracting main values from z
z = list(set(z))  
z = sorted(z, reverse=True) 


#filtered frequency
xFiltered = xn - (np.sin(2*np.pi* z[0]*t)+np.sin(2*np.pi*z[1]*t))
xFiltered_f = fft(xFiltered)
xFiltered_f = 2/N * np.abs(xFiltered_f [0:int(N/2)])


sd.play(xFiltered, 44100)

#--------------------------------------------------------------------------------------------------------------
# graph time domain
plt.figure()
plt.subplot(3,1,1)
plt.plot(t,x)
plt.title("Initial Signal in Time Domain")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(t,xn)
plt.title("Signal with Noise in Time Domain")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(t,xFiltered)
plt.title("Filtered Signal in Time Domain")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()


#graph frequency domain
plt.figure()
plt.subplot(3,1,1)
plt.plot(f,x_f)
plt.title("Frequency Domain of Signal")
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(f,xn_f)
plt.title("Frequency Domain of Signal with Noise")
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(f, xFiltered_f)
plt.title("Frequency Domain of Filtered Signal")
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.show()

