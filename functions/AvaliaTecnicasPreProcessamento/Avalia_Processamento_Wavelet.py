
"""
Código para avaliar o tempo de processamento de sinais
Será utilizado o sinal gerado com harmônicas
"""
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter

from functions.SignalGenerator.GeraSinais import GeraSinais  # Import the class from the module
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
resulting_voltages_withnoise_highsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'True', 40)
resulting_voltages_nonoise_highsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'False', 1000)

# Gerando os sinais com afundamento - com 128 amostras por ciclo
samples_per_cycle = 128
sampling_frequency = samples_per_cycle*frequency  # Change this to set the sampling frequency
resulting_voltages_withnoise_lowsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'True', 40)
resulting_voltages_nonoise_lowsample = GeraSinais.voltage_sag_short_circuit(sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, 'False', 1000)


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
time1, short_circuit_current_withnoise_highsample = GeraSinais.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'True', 40
)
time2, short_circuit_current_nonoise_highsample = GeraSinais.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'False', 1000
)

# low frequency
samples_per_cycle = 128 # samples per cycle of the generated signal
sampling_frequency = samples_per_cycle*frequency
time1, short_circuit_current_withnoise_lowsample = GeraSinais.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'True', 40
)
time2, short_circuit_current_nonoise_lowsample = GeraSinais.short_circuit_current(
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

    if 'voltages' in nome_sinal:
        duration = 1.0
    else:
        duration = 0.5

    ca, cd = wavelet_instance.transform(signal_values, 'db4')
    tempo_sinal = np.linspace(0, duration, len(signal_values))
    tempo_cd = np.linspace(0, duration, len(cd))
    cd = list(map(lambda x: x**2, cd))
    cd_desconsiderados = cd[100:-100]

    indice_max = None
    valor = max(cd_desconsiderados)*0.9
    size = len(cd)
    for i, elemento in enumerate(cd):
        if i < 100 or i > size-100:
            continue
        if elemento >= valor:
            indice_max = i
            break

    tempo = tempo_cd[indice_max]
    y = [1 if t >= tempo else 0 for t in tempo_cd]
    y_sinal = [1 if t >= start_time else 0 for t in tempo_sinal]


    fig, axs = plt.subplots(3)  # 2 linhas de subplot
    fig.suptitle(nome_sinal)
    plt.subplots_adjust(hspace=1.0)

    # Plotando o seno
    axs[0].plot(tempo_sinal, signal_values)
    axs[0].set_title('Signal')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Amplitude [pu]')

    # Plotando o cosseno
    axs[1].plot(tempo_cd, cd)
    axs[1].set_title('DWT')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Amplitude [pu]')

    # Plotando o cosseno
    axs[2].plot(tempo_cd, y, label='Real trip')
    axs[2].plot(tempo_sinal, y_sinal, linestyle='--', label='Ideal trip')
    axs[2].legend()
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Amplitude [pu]')
    axs[2].set_title('Trip')

    # Padronizando o eixo y para três casas decimais
    # Criando um formatador personalizado para o eixo y
    def formatador_cientifico(valor, pos):
        return "{:.1e}".format(valor)

    # Configurando o formatador personalizado para o eixo y
    for ax in axs.flat:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(formatador_cientifico))

    plt.subplots_adjust(left=0.22)

    plt.show()

    #print(nome_sinal)

    # Salvar os resultados na estrutura
    #resultados[nome_sinal] = {'Amplitude': amp, 'Ângulo': ang}
    #''' Finalizar a substituição por outra função aqui'''
# Exemplo de como acessar os resultados
for nome_sinal, resultado in resultados.items():
    print(f"Sinal: {nome_sinal}, Amplitude: {resultado['Amplitude']}, Ângulo: {resultado['Ângulo']}")
