#Código comentado linha a linha em inglês

import numpy as np  # Import the NumPy library for numerical operations
import matplotlib.pyplot as plt  # Import the Matplotlib library for plotting graphs
import emd  # Import the emd package for Empirical Mode Decomposition analysis

from GeraSinais import GeraSinais  # Import the GeraSinais class from the GeraSinais module

# Example usage
sag_magnitude = 0.5  # Magnitude of the voltage sag
start_time = 0.1  # Start time of the voltage sag
end_time = 0.5  # End time of the voltage sag
duration = 1.0  # Total duration of the signal
samples_per_cycle = 128  # Number of samples per cycle
frequency = 60.0  # Frequency of the electrical network in Hz
sampling_frequency = samples_per_cycle * frequency  # Sampling frequency
involved_phases = 'AB'  # Involved phases

# Example usage with noise
add_noise_sag = True  # Add noise to the voltage sag signal
SNR_sag = 20  # Signal-to-noise ratio for the voltage sag signal

# Generate the three-phase voltage sag signal caused by short circuit
resulting_voltages = GeraSinais.voltage_sag_short_circuit(
    sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, add_noise_sag, SNR_sag
)

# Plotting
'''
for phase, voltage in resulting_voltages.items():
    plt.plot(np.arange(0, duration, 1 / sampling_frequency), voltage, label=f'Phase {phase}')
'''

'''
plt.title('Three-Phase Voltage Sag caused by Short Circuit')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (pu)')
plt.legend()
plt.grid(True)
plt.show()
'''

# Convert the resulting voltage signal into a NumPy array
signal = np.array(resulting_voltages['A'])

# Create a time vector
time = np.arange(0, duration, 1 / sampling_frequency)

# Perform Empirical Mode Decomposition (EMD) of the signal
imf = emd.sift.sift(signal)

# Calculate the Hilbert Transform
IP, IF, IA = emd.spectra.frequency_transform(imf, sampling_frequency, 'hilbert')

# Plot the IMF (Intrinsic Mode Functions) modes
emd.plotting.plot_imfs(imf)

# Adjust the layout of the plot
plt.tight_layout()

# Display the plot
plt.show()