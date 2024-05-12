
"""
Código para avaliar o tempo de processamento de sinais
Será utilizado o sinal gerado com harmônicas
"""

from matplotlib.ticker import ScalarFormatter

from functions.SignalGenerator.SignalGenerator import Generate_Signals  # Import the class from the module
from functions.TW.DTW import DWT  # Import the class from the module
import numpy as np
import matplotlib.pyplot as plt

''' Parte 1 - Gera os sinais a serem analisados'''

# Teste 1 - Sinal de tensão com afundamento de tensão

sag_magnitude = 0.5  # Change this to set the sag magnitude
start_time = 0.1     # Change this to set the start time of the sag
end_time = 0.6       # Change this to set the end time of the sag
duration = 1.0       # Change this to set the duration of the signal
frequency = 60.0  # frequencia em Hz

involved_phases = 'A'    # Change this to set the involved phase or combination

# Gerando os sinais com afundamento - com 2048 amostras por ciclo
samples_per_cycle = 2048
sampling_frequency = samples_per_cycle*frequency  # Change this to set the sampling frequency
resulting_voltages_withnoise_highsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'True', 40)
resulting_voltages_nonoise_highsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'False', 1000)

# Gerando os sinais com afundamento - com 128 amostras por ciclo
samples_per_cycle = 128
sampling_frequency = samples_per_cycle*frequency  # Change this to set the sampling frequency
resulting_voltages_withnoise_lowsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'True', 40)
resulting_voltages_nonoise_lowsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'False', 1000)


# Test 2 - Short Circuit Current

amplitude = 1.00     # Peak amplitude of the current waveform
frequency = 60.0        # Frequency of the sinusoidal component (60 Hz)
short_circuit_time = 0.1  # Time at which the short circuit occurs (in seconds)
increase_factor = 7.0   # Factor determining the increase in current during short circuit
decay_factor = 5.0      # Exponential decay factor after the increase
duration = 0.5         # Total duration of the waveform (in seconds)

# gera o sinal de corrente durante curto circuito
# high frequency
samples_per_cycle = 2048 # samples per cycle of the generated signal
sampling_frequency = samples_per_cycle*frequency
time1, short_circuit_current_withnoise_highsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'True', 40
)
time2, short_circuit_current_nonoise_highsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'False', 1000
)

# low frequency
samples_per_cycle = 128 # samples per cycle of the generated signal
sampling_frequency = samples_per_cycle*frequency
time1, short_circuit_current_withnoise_lowsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'True', 40
)
time2, short_circuit_current_nonoise_lowsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'False', 1000
)




''' Parte 2 - Analisa a Técnica de Processamento de Sinais'''
# A partir daqui apague e coloque a avaliação da sua técnica


# Criar uma instância da classe Wavelet
wavelet_instance = DWT()

# Tipos de sinais já carregados no ambiente Python
resulting_voltages_withnoise_highsample_A = resulting_voltages_withnoise_highsample['A']
resulting_voltages_nonoise_highsample_A = resulting_voltages_nonoise_highsample['A']
resulting_voltages_withnoise_lowsample_A = resulting_voltages_withnoise_lowsample['A']
resulting_voltages_nonoise_lowsample_A = resulting_voltages_nonoise_lowsample['A']

vetor_sinais = [
    resulting_voltages_withnoise_highsample_A,
    resulting_voltages_nonoise_highsample_A,
    resulting_voltages_withnoise_lowsample_A,
    resulting_voltages_nonoise_lowsample_A,
    short_circuit_current_withnoise_highsample,
    short_circuit_current_nonoise_highsample,
    short_circuit_current_withnoise_lowsample,
    short_circuit_current_nonoise_lowsample
]

nome_sinais = [
    'resulting_voltages_withnoise_highsample',
    'resulting_voltages_nonoise_highsample',
    'resulting_voltages_withnoise_lowsample',
    'resulting_voltages_nonoise_lowsample',
    'short_circuit_current_withnoise_highsample',
    'short_circuit_current_nonoise_highsample',
    'short_circuit_current_withnoise_lowsample',
    'short_circuit_current_nonoise_lowsample'
]

nome_sinais_title = [
    'Voltage with noise - High sample',
    'Voltage without noise - High sample',
    'Voltage with noise - Low sample',
    'Voltage without noise - Low sample',
    'Current with noise - High sample',
    'Current without noise - High sample',
    'Current with noise - Low sample',
    'Current without noise - Low sample'
]

# Estrutura para armazenar os resultados
resultados = {}

print("Gerou todos os sinais")

i = 0

# Loop over signal types
for signal_name, signal_values in zip(nome_sinais, vetor_sinais):
    # Determine if it's highsample or lowsample based on signal name
    if 'highsample' in signal_name:
        samples_per_cycle = 2048
    elif 'lowsample' in signal_name:
        samples_per_cycle = 128
    else:
        raise ValueError(f"Unrecognized signal type in name: {signal_name}")

    '''Start substitution with another function here'''
    # Calculate desired function using 'calculate_TS_of_signal' function

    # Determine the duration based on signal type
    if 'voltages' in signal_name:
        duration = 1.0
    else:
        duration = 0.5

    # Apply Discrete Wavelet Transform (DWT) to the signal
    ca, cd = wavelet_instance.transform(signal_values, 'db4')

    # Generate time arrays for the signal and its DWT
    signal_time = np.linspace(0, duration, len(signal_values))
    cd_time = np.linspace(0, duration, len(cd))

    # Square the DWT coefficients and ignore certain elements
    cd = list(map(lambda x: x**2, cd))
    cd_ignored = cd[100:-100]

    # Find the index of the maximum value in the ignored portion of the DWT
    max_index = None
    value = max(cd_ignored) * 0.9
    size = len(cd)
    for i, element in enumerate(cd):
        if i < 100 or i > size - 100:
            continue
        if element >= value:
            max_index = i
            break

    # Calculate the time corresponding to the maximum value
    time = cd_time[max_index]

    # Generate a binary signal indicating trip occurrence based on this time
    y = [1 if t >= time else 0 for t in cd_time]
    y_signal = [1 if t >= start_time else 0 for t in signal_time]

    # Create subplots for each aspect of the analysis
    fig, axs = plt.subplots(3)
    #fig.suptitle(nome_sinais_title[0])

    # Adjust subplot layout
    plt.subplots_adjust(left=0.22)
    plt.subplots_adjust(hspace=1.0)

    # Plot the original signal
    axs[0].plot(signal_time, signal_values)
    axs[0].set_title('Signal')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Amplitude [pu]')

    # Plot the DWT
    axs[1].plot(cd_time, cd)
    axs[1].set_title('DWT')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Amplitude [pu]')

    # Plot the trip occurrence
    axs[2].plot(cd_time, y, label='Real trip')
    axs[2].plot(signal_time, y_signal, linestyle='--', label='Ideal trip')
    axs[2].legend()
    axs[2].set_xlabel('Time [s]')
    axs[2].set_ylabel('Amplitude [pu]')
    axs[2].set_title('Trip')
    print(signal_name)

    # Set custom formatter for y-axis to display in scientific notation
    def scientific_formatter(value, pos):
        return "{:.1e}".format(value)

    for ax in axs.flat:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(scientific_formatter))

    # Show the plots
    plt.show()
    i = i+1
