import matplotlib.pyplot as plt
import numpy as np
from GeraSinais import GeraSinais

def STFT(x, fs, frame_size, hop):
  """
  Perform STFT (Short-Time Fourier Transform).

  x: Input data.
  fs: Sampling rate.
  frame_size: Frame size.
  hop: Hop size
  """

  frame_samp = int(frame_size*fs)
  hop_samp = int(hop*fs)
  w = np.hanning(frame_samp) # Hanning window
  X = np.array([np.fft.fft(w*x[i:i+frame_samp])
               for i in range(0, len(x)-frame_samp, hop_samp)])
  return X

"""
Test 2 - Evaluating Generating Signals With Harmonics
"""
# Exemplo de uso da função com harmonics_start_time = 0.1 segundos
amplitude_fundamental = 10  # amplitude da fundamental
samples_per_cycle = 128
frequency = 60.0  # frequência em Hz
harmonics = [2, 3, 5]
amplitudes = [5, 3, 1]  # Adicione amplitudes correspondentes às harmônicas
duration = 2
harmonics_start_time = 0.5  # tempo em segundos para começar a adicionar as harmônicas

# Example usage with noise
add_noise_harmonics = True  # Change this to True if you want to add noise
SNR_harmonics = 15  # Change this to set the SNR for the harmonics signal

time, generated_signal = GeraSinais.GenerateSignalWithHarmonics(
    amplitude_fundamental, samples_per_cycle, frequency, harmonics, amplitudes, duration, harmonics_start_time, add_noise_harmonics, SNR_harmonics
)

# Plota a forma de onda
plt.plot(time, generated_signal)
plt.title('Signal with Harmonics')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

fs = samples_per_cycle/(1/frequency)
frame_size = 0.05
hop = 0.025


X = STFT(generated_signal, fs, frame_size, hop)

# Plot time-frequency relation

plt.figure(figsize=(20, 15))

ax = plt.subplot(2, 1, 2)
Fz = int(frame_size * fs * 0.3)
ax.imshow(np.absolute(X[:,:Fz].T), origin='lower',
          aspect='auto', interpolation='nearest',extent=[0, 2, 0, 500])
plt.title('Measured signal')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency (Hz)')
plt.show()