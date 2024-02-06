"""
Código para avaliar o tempo de processamento de sinais
Será utilizado o sinal gerado com harmônicas
"""
import numpy as np
import matplotlib.pyplot as plt
import emd

from GeraSinais import GeraSinais  # Import the class from the module

# ADICIONAR AQUI OS PACOTES E FUNCOES DAS OUTRAS TRANSFORMADAS


''' Parte 1 - Gera os sinais a serem analisados'''

# Teste 1 - Sinal de tensão com afundamento de tensão

sag_magnitude = 0.5  # Change this to set the sag magnitude
start_time = 0.1  # Change this to set the start time of the sag
end_time = 0.6  # Change this to set the end time of the sag
duration = 1.0  # Change this to set the duration of the signal
frequency = 60.0  # frequencia em Hz

involved_phases = 'A'  # Change this to set the involved phase or combination

# Gerando os sinais com afundamento - com 2048 amostras por ciclo
samples_per_cycle = 2048
sampling_frequency = samples_per_cycle * frequency  # Change this to set the sampling frequency
resulting_voltages_withnoise_highsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time,
                                                                               duration, sampling_frequency,
                                                                               involved_phases, 'True', 40)
resulting_voltages_nonoise_highsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time,
                                                                             duration, sampling_frequency,
                                                                             involved_phases, 'False', 1000)

# Gerando os sinais com afundamento - com 128 amostras por ciclo
samples_per_cycle = 128
sampling_frequency = samples_per_cycle * frequency  # Change this to set the sampling frequency
resulting_voltages_withnoise_lowsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time,
                                                                              duration, sampling_frequency,
                                                                              involved_phases, 'True', 40)
resulting_voltages_nonoise_lowsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time,
                                                                            duration, sampling_frequency,
                                                                            involved_phases, 'False', 1000)

# Test 2 - Short Circuit Current

amplitude = 1.00  # Peak amplitude of the current waveform
frequency = 60.0  # Frequency of the sinusoidal component (60 Hz)
short_circuit_time = 0.1  # Time at which the short circuit occurs (in seconds)
increase_factor = 7.0  # Factor determining the increase in current during short circuit
decay_factor = 5.0  # Exponential decay factor after the increase
duration = 0.5  # Total duration of the waveform (in seconds)

# gera o sinal de corrente durante curto circuito
# high frequency
samples_per_cycle = 2048  # samples per cycle of the generated signal
sampling_frequency = samples_per_cycle * frequency
time1, short_circuit_current_withnoise_highsample = GeraSinais.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'True', 40
)
time2, short_circuit_current_nonoise_highsample = GeraSinais.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'False', 1000
)

# low frequency
samples_per_cycle = 128  # samples per cycle of the generated signal
sampling_frequency = samples_per_cycle * frequency
time1, short_circuit_current_withnoise_lowsample = GeraSinais.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'True', 40
)
time2, short_circuit_current_nonoise_lowsample = GeraSinais.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'False', 1000
)

''' Parte 2 - Analisa a Técnica de Processamento de Sinais'''
# A partir daqui apague e coloque a avaliação da sua técnica


# Criar uma instância da classe Stockwell
# emd_instance = emd()

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

# Estrutura para armazenar os resultados
resultados = {}

print("Gerou todos os sinais")

#imf1 = emd.sift.sift(resulting_voltages_withnoise_highsample['A'])
#emd.plotting.plot_imfs(imf1)

#imf2 = emd.sift.sift(resulting_voltages_withnoise_lowsample['A'])
#emd.plotting.plot_imfs(imf2)

#imf1 = emd.sift.sift(resulting_voltages_nonoise_highsample['A'])
#emd.plotting.plot_imfs(imf1)

#imf2 = emd.sift.sift(resulting_voltages_nonoise_lowsample['A'])
#emd.plotting.plot_imfs(imf2)

#imf1 = emd.sift.sift(short_circuit_current_withnoise_highsample)
#emd.plotting.plot_imfs(imf1)

#imf2 = emd.sift.sift(short_circuit_current_withnoise_lowsample)
#emd.plotting.plot_imfs(imf2)

imf1 = emd.sift.sift(short_circuit_current_nonoise_highsample)
emd.plotting.plot_imfs(imf1)

imf2 = emd.sift.sift(short_circuit_current_nonoise_lowsample)
emd.plotting.plot_imfs(imf2)


# Show the plots
plt.show()
