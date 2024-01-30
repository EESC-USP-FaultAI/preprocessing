
"""
Código para avaliar o tempo de processamento de sinais
Será utilizado o sinal gerado com harmônicas
"""
from functions.SignalGenerator.GeraSinais import GeraSinais  # Import the class from the module
from functions.TT import componentes_simetricas as cs
from functions.TT import clarke
from functions.TT import park
from plotTT import plotTT
import numpy as np
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
resulting_voltages_withnoise_highsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'True', 40)
resulting_voltages_nonoise_highsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'False', 1000)

# Gerando os sinais com afundamento - com 128 amostras por ciclo
samples_per_cycle = 128
sampling_frequency = samples_per_cycle*frequency  # Change this to set the sampling frequency
resulting_voltages_withnoise_lowsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'True', 40)
resulting_voltages_nonoise_lowsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'False', 1000)


''' Parte 2 - Analisa a Técnica de Processamento de Sinais'''
# A partir daqui apague e coloque a avaliação da sua técnica


# Tipos de sinais já carregados no ambiente Python
resulting_voltages_withnoise_highsample_A = resulting_voltages_withnoise_highsample['A']
resulting_voltages_nonoise_highsample_A = resulting_voltages_nonoise_highsample['A']
resulting_voltages_withnoise_lowsample_A = resulting_voltages_withnoise_lowsample['A']
resulting_voltages_nonoise_lowsample_A = resulting_voltages_nonoise_lowsample['A']

vetor_sinais = [
    resulting_voltages_withnoise_highsample,
    resulting_voltages_nonoise_highsample,
    resulting_voltages_withnoise_lowsample,
    resulting_voltages_nonoise_lowsample
]

nome_sinais = [
    'resulting_voltages_withnoise_highsample',
    'resulting_voltages_nonoise_highsample',
    'resulting_voltages_withnoise_lowsample',
    'resulting_voltages_nonoise_lowsample'
]

# Estrutura para armazenar os resultados
resultados = {}

print("Gerou todos os sinais")

# Filtro para obter o fasor
def DFT(sinal, N):
    length = len(sinal)
    harmonico = 0
    for n in range(0, length):
        harmonico += sinal[n] * np.e ** (complex(0, -1) * n * (2 * np.pi) / N)

    return 2 * harmonico / length


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

    Va = signal_values['A']
    Vb = signal_values['B']
    Vc = signal_values['C']

    if True: #samples_per_cycle == 128:
        print(nome_sinal)
        Vpos = []
        Vneg = []
        Vzero = []

        Valfa = []
        Vbeta = []
        Vzer0 = []

        vD = []
        vQ = []
        v0 = []
        for i in range(0, len(Va) - samples_per_cycle):
            A = DFT(Va[i:i + samples_per_cycle], samples_per_cycle)
            B = DFT(Vb[i:i + samples_per_cycle], samples_per_cycle)
            C = DFT(Vc[i:i + samples_per_cycle], samples_per_cycle)
            # Componentes simétricas
            vetAB0 = cs.comp_sim_ABCto012(A, B, C)
            Vpos.append(vetAB0[1])
            Vneg.append(vetAB0[2])
            Vzero.append(vetAB0[0])

            # Clarke
            vetAB0 = clarke.clarke_ABCtoAB0(A, B, C, True)
            Valfa.append(vetAB0[1])
            Vbeta.append(vetAB0[2])
            Vzer0.append(vetAB0[0])

            # Parke
            comp = 0  # i*2*np.pi/amostras
            vetAB0 = park.park_ABCtoDQ(A, B, C, comp, True)
            v0.append(vetAB0[0])
            vD.append(vetAB0[1])
            vQ.append(vetAB0[2])

        plotTT(signal_values, [Vpos, Vneg, Vzero], [Valfa, Vbeta, Vzer0], [vD, vQ, v0], nome_sinal, samples_per_cycle)