# -*- coding: utf-8 -*-
"""
Código para testar os sinais gerados criado por Gabriela Nunes.
dúvidas: gabrielanuneslopes@usp.br
"""
from functions.SignalGenerator.SignalGenerator import Generate_Signals  # Import the class from the module
import matplotlib.pyplot as plt
import numpy as np


"""
Test 1 - Evaluating voltage sag caused by a short circuit
"""

# Example usage
sag_magnitude = 0.5  # Change this to set the sag magnitude
start_time = 0.1     # Change this to set the start time of the sag
end_time = 0.5       # Change this to set the end time of the sag
duration = 1.0       # Change this to set the duration of the sag
samples_per_cycle = 128
frequency = 60.0  # frequencia em Hz
sampling_frequency = samples_per_cycle*frequency  # Change this to set the sampling frequency
involved_phases = 'AB'    # Change this to set the involved phase or combination

# Example usage with noise
add_noise_sag = True  # Change this to True if you want to add noise
SNR_sag = 20  # Change this to set the SNR for the sag signal

resulting_voltages = Generate_Signals.voltage_sag_short_circuit(
    sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, add_noise_sag, SNR_sag
)

# Plotting
for phase, voltage in resulting_voltages.items():
    plt.plot(np.arange(0, duration, 1/sampling_frequency), voltage, label=f'Phase {phase}')

plt.title('Three-Phase Voltage Sag caused by Short Circuit')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (pu)')
plt.legend()
plt.grid(True)
plt.show()





"""
Test 2 - Evaluating Generating Signals With Harmonics
"""
# Exemplo de uso da função com harmonics_start_time = 0.1 segundos
amplitude_fundamental = 10  # amplitude da fundamental
samples_per_cycle = 128
frequency = 60.0  # frequencia em Hz
harmonics = [2, 3, 5]
amplitudes = [5, 3, 1]  # Adicione amplitudes correspondentes às harmônicas
duration = 0.2
harmonics_start_time = 0.1  # tempo em segundos para começar a adicionar as harmônicas

# Example usage with noise
add_noise_harmonics = True  # Change this to True if you want to add noise
SNR_harmonics = 15  # Change this to set the SNR for the harmonics signal

time, generated_signal = Generate_Signals.GenerateSignalWithHarmonics(
    amplitude_fundamental, samples_per_cycle, frequency, harmonics, amplitudes, duration, harmonics_start_time, add_noise_harmonics, SNR_harmonics
)

# Plota a forma de onda
plt.plot(time, generated_signal)
plt.title('Signal with Harmonics')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()





"""
Test 3 - Short Circuit Current
"""
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
time, short_circuit_current = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, add_noise_current, SNR_current
)

# Plotting
plt.plot(time, short_circuit_current)
plt.title('Short Circuit Current')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.grid(True)
plt.show()