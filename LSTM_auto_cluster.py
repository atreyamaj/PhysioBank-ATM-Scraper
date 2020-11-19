#Writing Code for a single file, you can extrapolate this to your files in a loop using os.listdir(dir)

m_name = '3000063_final.mat' #Taking a single file to work with for now
i_name = '3000063m.info'

import keras #Importing necessary libraries
import sklearn
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

#Loading the .mat file and storing values in lists so that we can use them again later
mat = loadmat(m_name)
abp_ar = mat['ABP']
pleth_ar = mat['PLETH']
time_ar = np.arange(len(abp_ar[0])) #A temporal numpy array
abp_ar = abp_ar.T #Taking transpose of the array in order to keep the array dimensions consistent

plt.plot(time_ar ,abp_ar) #Plotting the graph

#____________________________________________________________________________

'''
We must now add a low pass filter so filter out noise from the ECG data.
For this, I am currently using a Kaiser-window baed 15 Hertz low-pass filter with a sampling rate of 125 Hertz (fs). 
'''

fc = 0.12  # Cutoff frequency as a fraction of the sampling rate , 15/125
b = 0.1    # Transition band, as a fraction of the sampling rate (in (0, 0.5)).
A = 40     # Attenuation in the stopband [dB].
 
N = int(np.ceil((A - 8) / (2.285 * 2 * np.pi * b))) + 1
if not N % 2: N += 1  # Make sure that N is odd.
if A > 50:
    beta = 0.1102 * (A - 8.7)
elif A <= 50 and A >= 21:
    beta = 0.5842 * (A - 21) ** 0.4 + 0.07886 * (A - 21)
else:
    beta = 0
n = np.arange(N)
 
# Compute sinc filter.
h = np.sinc(2 * fc * (n - (N - 1) / 2))
 
# Compute Kaiser window.
w = np.i0(beta * np.sqrt(1 - (2 * n / (N - 1) - 1) ** 2)) / np.i0(beta)
 
# Multiply sinc filter by window.
h = h * w
 
# Normalize to get unity gain.
h = h / np.sum(h) #This is the final Window

#__________________________________________________________________________

'''
Now that we have our Kaiser window LP filter set up, we will convolve this with the  time-series data.
Another alternative is to use FFT to convert the data to frequency domain, multiply the window instead of convolving and back-converting using IFFT.
'''

abp_ar = abp_ar[:,0]
filtered = np.convolve(abp_ar, h) #Filtered array

plt.plot(np.arange(len(filtered)),filtered) #Plotting the filtered data
#_____________________________________________
'''
We must now segment the data into smaller arrays. In order to optimize computation time,
I am segmenting the data into multiple smaller Numpy arrays and storing all those array
within a single Numpy Binary file (.npy) as a multi-dimensional array, with each array having 725 elements.
'''

import os
#file_no = 0
#file = open('Vals_file', 'a+b')
x=[]
new = []
for i in range(1,len(filtered)):
  if i % 725 == 0:
    x.append(new)
    new = []
  else:
    new.append(filtered[i])

np.array(x).tofile('value_file.npy') #This creates the Numpy Binary file
#__________________________________________________________

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, TimeDistributed, RepeatVector # Importing Functions to create the Autoencoder

# define model
encoded = Sequential()
encoded.add(LSTM(100, activation = 'relu', input_shape=(t,1)))
encoded.add(LSTM(100, activation = 'relu'))
decoded = LSTM(100, activation='relu', return_sequences=True)(encoded)
decoded.add(LSTM(t, return_sequences=True))
decoded.compile(optimizer='adam', loss='mse')

decoded.fit(filtered, filtered, epochs = 5, verbose = 0)

decoded.save('LSTM_AutoEncoder_CDL')