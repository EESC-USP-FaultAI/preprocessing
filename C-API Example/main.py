import numpy as np
from libs import fft, fft_faster
from time import perf_counter
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from functions.TF import FFT_function

fs = 10e3
fs = (2 ** int(np.ceil(np.log2(fs))))  # Next power of 2
t = np.arange(0, 2, 1/fs)
signal = np.sin(2*np.pi*60*t) + np.sin(2*np.pi*120*t) + np.sin(2*np.pi*180*t)

t0 = perf_counter()
fft_signal = fft(signal)
t1 = perf_counter()
print(f'Time elapsed at C-API FFT Recursive: {(t1-t0)*1e3:.4f} ms')

t0 = perf_counter()
fft_signal = fft_faster(signal)
t1 = perf_counter()
print(f'Time elapsed at C-API FFT Non-Recursive: {(t1-t0)*1e3:.4f} ms')


t0 = perf_counter()
fft_signal2 = FFT_function.FFT(signal)
t1 = perf_counter()
print(f'Time elapsed at Python FFT Recursive: {(t1-t0)*1e3:.4f} ms')

t0 = perf_counter()
fft_signal2 = np.fft.fft(signal)
t1 = perf_counter()
print(f'Time elapsed at Numpy FFT: {(t1-t0)*1e3:.4f} ms')


# plots
import matplotlib.pyplot as plt

freqArray = np.fft.fftfreq(len(signal), 1/fs)

fft_signal = fft_signal[np.logical_and(freqArray >= 0, freqArray <= 240)]/len(signal)*2
fft_signal2 = fft_signal2[np.logical_and(freqArray >= 0, freqArray <= 240)]/len(signal)*2
freqArray = freqArray[np.logical_and(freqArray >= 0, freqArray <= 240)]

plt.figure(figsize=(15,5))

plt.subplot(1,2,1)
plt.stem(freqArray, np.abs(fft_signal))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('FFT C-API')
plt.xticks(np.arange(0, 241, 60))
plt.grid(True)

plt.subplot(1,2,2)
plt.stem(freqArray, np.abs(fft_signal2))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('FFT Python')
plt.xticks(np.arange(0, 241, 60))
plt.grid(True)

plt.tight_layout()
plt.show()

