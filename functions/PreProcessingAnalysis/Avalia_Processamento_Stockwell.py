
"""
Código para avaliar o tempo de processamento de sinais
Será utilizado o sinal gerado com harmônicas
"""
"feito gabi 10/01"
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import functions.SignalGenerator as Generate_Signals
from functions.TS import calculate_ST_of_the_signal
import matplotlib.pyplot as plt
from plotST import plotST
# ADICIONAR AQUI OS PACOTES E FUNCOES DAS OUTRAS TRANSFORMADAS


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
resulting_voltages_withnoise_highsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, True, 40)
resulting_voltages_nonoise_highsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, False, 1000)

# Gerando os sinais com afundamento - com 128 amostras por ciclo
samples_per_cycle = 128
sampling_frequency = samples_per_cycle*frequency  # Change this to set the sampling frequency
resulting_voltages_withnoise_lowsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, True, 40)
resulting_voltages_nonoise_lowsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, False, 1000)


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
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, True, 40
)
time2, short_circuit_current_nonoise_highsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, False, 1000
)

# low frequency
samples_per_cycle = 128 # samples per cycle of the generated signal
sampling_frequency = samples_per_cycle*frequency
time1, short_circuit_current_withnoise_lowsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, True, 40
)
time2, short_circuit_current_nonoise_lowsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, False, 1000
)




''' Parte 2 - Analisa a Técnica de Processamento de Sinais'''
# A partir daqui apague e coloque a avaliação da sua técnica


# Criar uma instância da classe Stockwell

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

# Loop sobre os tipos de sinais
for nome_sinal, signal_values in zip(nome_sinais, vetor_sinais):
    # Determinar se é highsample ou lowsample com base no nome do sinal
    if 'highsample' in nome_sinal:
        samples_per_cycle = 2048
    elif 'lowsample' in nome_sinal:
        samples_per_cycle = 128
    else:
        raise ValueError(f"Tipo de sinal não reconhecido no nome: {nome_sinal}")

    ''' Iniciar a substituição por outra função aqui'''
    # Calcular a função desejada usando a função 'calcula_TS_do_sinal'

    if True: #samples_per_cycle == 128:
        if 'voltages' in nome_sinal:
            amp, ang = calculate_ST_of_the_signal(signal_values, samples_per_cycle, 3)

            print(nome_sinal + ' feito')
            plotST(nome_sinal, amp, samples_per_cycle, start_time, end_time, signal_values)

            # Salvar os resultados na estrutura
            resultados[nome_sinal] = {'Amplitude': amp, 'Ângulo': ang}
            ''' Finalizar a substituição por outra função aqui'''

        else:
            amp, ang = calculate_ST_of_the_signal(signal_values, samples_per_cycle, 3)

            print(nome_sinal + ' feito')
            plotST(nome_sinal, amp, samples_per_cycle, start_time, start_time, signal_values)

            # Salvar os resultados na estrutura
            resultados[nome_sinal] = {'Amplitude': amp, 'Ângulo': ang}
            ''' Finalizar a substituição por outra função aqui'''


# Exemplo de como acessar os resultados
for nome_sinal, resultado in resultados.items():
    print(f"Sinal: {nome_sinal}, Amplitude: {resultado['Amplitude']}, Ângulo: {resultado['Ângulo']}")
