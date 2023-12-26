import PyWaveletScripts
from SignalGenerator.GeraSinais import GeraSinais
import matplotlib.pyplot as plt
import numpy as np


"""Generating Signal"""
amplitude = 100.00     # Peak amplitude of the current waveform
frequency = 60.0        # Frequency of the sinusoidal component (60 Hz)
short_circuit_time = 0.1  # Time at which the short circuit occurs (in seconds)
increase_factor = 7.0   # Factor determining the increase in current during short circuit
decay_factor = 5.0      # Exponential decay factor after the increase
duration = 0.5         # Total duration of the waveform (in seconds)
samples_per_cycle = 128 # samples per cycle of the generated signal
sampling_frequency = samples_per_cycle*frequency

# Example usage with noise
add_noise_current = True  # Change this to True if you want to add noise
SNR_current = 60  # Change this to set the SNR for the short circuit current signal

# Generate short circuit current waveform
time, short_circuit_current = GeraSinais.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, add_noise_current, SNR_current
)

# Plotting generated signal
plt.plot(time, short_circuit_current)
plt.title('Short Circuit Current')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.grid(True)
plt.show()


"""Wavelet Testing"""

PyWaveletScripts.list_wavelets()  # Showing wavelets available.
wave_name = input("Write the name of the wavelet you wanna choose: ")  # User chooses the wavelet they want.
print(f"You choose {wave_name} wavelet:")
PyWaveletScripts.wavelet_viewer(wave_name)  # Showing chosen wavelet properties.
cA, cD = PyWaveletScripts.evaluate_dwt_single_phase(short_circuit_current, wave_name)  # Evaluating DWT

# Plotting Approximation Coefficients
plt.plot(cA)
plt.title("Approximation Coefficients")
plt.xlabel("Sample")
plt.ylabel("cA")
plt.grid(True)
plt.show()


# Plotting Detail Coefficients
plt.plot(cD)
plt.title("Detail Coefficients")
plt.xlabel("Sample")
plt.ylabel("cD")
plt.grid(True)
plt.show()
