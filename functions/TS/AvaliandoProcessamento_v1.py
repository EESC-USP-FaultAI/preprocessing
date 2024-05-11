
"""
Code to evaluate the ST of signals with harmonics 
"""

from functions.SignalGenerator.SignalGenerator import Generate_Signals  # Import the class from the module
from functions.TS.ST import Stockwell
import time
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Generate the signals 
amplitude_fundamental = 10  # Fundamental amplitude 
samples_per_cycle = 128
frequency = 60.0  # frequency
harmonics = [2, 3, 5]
amplitudes = [5, 3, 1]  # Add the amplitude of the harmonics
duration = 0.2
harmonics_start_time = 0.1  # Time to start to add the harmonics 
add_noise_harmonics = False  # Change this to True if you want to add noise
SNR_harmonics = 15  # Change this to set the SNR for the harmonics signal

tempo_sinal, signal = Generate_Signals.GenerateSignalWithHarmonics(
    amplitude_fundamental, samples_per_cycle, frequency, harmonics, amplitudes, duration, harmonics_start_time, add_noise_harmonics, SNR_harmonics
)

# Step 2: Evaluate the signal processing
# Criar uma instância da classe Stockwell
stockwell_instance = Stockwell()
# Call the method calculate_ST_of_the_signal da instância stockwell_instance
start_time = time.time()
amp, ang = stockwell_instance.calculate_ST_of_the_signal(signal, samples_per_cycle, 3)
end_time = time.time()
tempo_total = end_time - start_time

# plot line 1 (fundamental) and the lines that contain the harmonics
# Number of harmonics
num_harm = len(harmonics) + 1

# Create subplots for 'amp'
plt.figure(figsize=(12, 8))
j=0
for i in [1] + harmonics:
    plt.subplot(num_harm, 1, j+1)
    plt.plot(amp[i, :], label=f'{i}ª Harmônica' if i > 1 else 'Fundamental')
    plt.title(f'{i}ª Harmônica' if i > 1 else 'Fundamental')
    plt.ylim(0, 11)
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    plt.legend()
    j+=1

plt.suptitle(f'Processing Time: {tempo_total:.4f} segundos', y=1.02)
plt.tight_layout()
plt.show()

# Criar subplots para 'ang'
plt.figure(figsize=(12, 8))
j=0
for i in [1] + harmonics:
    plt.subplot(num_harm, 1, j + 1)
    plt.plot(ang[i, :], label=f'{i}ª Harmônica' if i > 1 else 'Fundamental')
    plt.title(f'{i}ª Harmônica' if i > 1 else 'Fundamental')
    plt.xlabel('Tempo')
    # plt.xlim(0, 6)
    plt.ylabel('Ângulo')
    plt.legend()
    j+=1

plt.suptitle(f'Tempo de Processamento: {tempo_total:.4f} segundos', y=1.02)
plt.tight_layout()
plt.show()
a=1+2
