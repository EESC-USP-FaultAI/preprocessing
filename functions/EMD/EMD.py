import numpy as np
import matplotlib.pyplot as plt
import emd

from functions.SignalGenerator.SignalGenerator import GeraSinais # Import the class from the module


# Example usage
sag_magnitude = 0.5  # Change this to set the sag magnitude
start_time = 0.1  # Change this to set the start time of the sag
end_time = 0.5  # Change this to set the end time of the sag
duration = 1.0  # Change this to set the duration of the sag
samples_per_cycle = 128
frequency = 60.0  # frequencia em Hz
sampling_frequency = samples_per_cycle * frequency  # Change this to set the sampling frequency
involved_phases = 'AB'  # Change this to set the involved phase or combination

# Example usage with noise
add_noise_sag = False  # Change this to True if you want to add noise
SNR_sag = 20  # Change this to set the SNR for the sag signal

resulting_voltages = GeraSinais.voltage_sag_short_circuit(
    sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, add_noise_sag, SNR_sag
)

# Plotting
for phase, voltage in resulting_voltages.items():
    plt.plot(np.arange(0, duration, 1 / sampling_frequency), voltage, label=f'Phase {phase}')

'''plt.title('Three-Phase Voltage Sag caused by Short Circuit')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (pu)')
plt.legend()
plt.grid(True)
plt.show()'''

signal = np.array(resulting_voltages['A'])
time = np.arange(0, duration, 1 / sampling_frequency)
imf = emd.sift.sift(signal)

IP, IF, IA = emd.spectra.frequency_transform(imf, sampling_frequency, 'hilbert')

freq_range = (0, 10, 100)  # 0 to 10Hz in 50 steps
f, hht = emd.spectra.hilberthuang(IF, IA, freq_range, sum_time=False)

plt.figure(figsize=(10, 8))
plt.subplot(211, frameon=False)
plt.plot(time, signal, 'k')
plt.plot(time, imf[:, 0]-4, 'r')
plt.plot(time, imf[:, 1]-8, 'g')
plt.plot(time, imf[:, 2]-12, 'b')
plt.xlim(time[0], time[-1])
plt.grid(True)
plt.subplot(212)
plt.pcolormesh(time, f, hht, cmap='ocean_r')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (secs)')
plt.grid(True)
plt.show()
