"""
Código para avaliar o tempo de processamento de sinais
Será utilizado o sinal gerado com harmônicas
"""
import numpy as np
import matplotlib.pyplot as plt
from functions.SignalGenerator.SignalGenerator import Generate_Signals

def vmd(X, alpha=200, tau=0.1, K=10, tol=1e-7, max_iter=500):
    """
    Variational Mode Decomposition (VMD) algorithm.

    Parameters:
    - X: Input signal (1D array)
    - alpha: Regularization parameter
    - tau: Center frequency parameter
    - K: Number of modes
    - tol: Tolerance for stopping criteria
    - max_iter: Maximum number of iterations

    Returns:
    - Modes: Decomposed modes
    """
    N = len(X)
    K = min(K, N // 2)  # Ensure K is not greater than half of the signal length

    # Initialization
    u = np.zeros((N, K))
    omega = np.zeros((N, K))
    alpha_k = alpha * np.ones((N, K))

    for iteration in range(max_iter):
        # Update modes
        for k in range(K):
            u[:, k] = np.fft.ifft(np.fft.fft(X) / (alpha_k[:, k] + 1j * omega[:, k]))

        # Update omegas
        for k in range(K - 1):
            omega[:, k] = np.angle(np.fft.fft(u[:, k + 1] - u[:, k]))

        omega[:, -1] = np.angle(np.fft.fft(X - u[:, -1]))

        # Update alphas
        alpha_k = alpha_k - tau * (np.sum(np.diff(omega, axis=1), axis=1, keepdims=True) - alpha_k * omega)

        # Stopping criteria
        if np.linalg.norm(X - np.sum(u, axis=1)) / np.linalg.norm(X) < tol:
            break

    return u
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
resulting_voltages_withnoise_highsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time,
                                                                               duration, sampling_frequency,
                                                                               involved_phases, 'True', 40)
resulting_voltages_nonoise_highsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time,
                                                                             duration, sampling_frequency,
                                                                             involved_phases, 'False', 1000)

# Gerando os sinais com afundamento - com 128 amostras por ciclo
samples_per_cycle = 128
sampling_frequency = samples_per_cycle * frequency  # Change this to set the sampling frequency
resulting_voltages_withnoise_lowsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time,
                                                                              duration, sampling_frequency,
                                                                              involved_phases, 'True', 40)
resulting_voltages_nonoise_lowsample = Generate_Signals.voltage_sag_short_circuit(sag_magnitude, start_time, end_time,
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
time1, short_circuit_current_withnoise_highsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'True', 40
)
time2, short_circuit_current_nonoise_highsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'False', 1000
)

# low frequency
samples_per_cycle = 128  # samples per cycle of the generated signal
sampling_frequency = samples_per_cycle * frequency
time1, short_circuit_current_withnoise_lowsample = Generate_Signals.short_circuit_current(
    amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, 'True', 40
)
time2, short_circuit_current_nonoise_lowsample = Generate_Signals.short_circuit_current(
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

#modes = vmd(resulting_voltages_withnoise_highsample['A'])
#signal_time = np.linspace(0, 0.5, len(resulting_voltages_withnoise_highsample['A']))

#modes = vmd(resulting_voltages_withnoise_lowsample['A'])
#signal_time = np.linspace(0, 1, len(resulting_voltages_withnoise_lowsample['A']))

#modes = vmd(resulting_voltages_nonoise_highsample['A'])
#signal_time = np.linspace(0, 0.5, len(resulting_voltages_nonoise_highsample['A']))

#modes = vmd(resulting_voltages_nonoise_lowsample['A'])
#signal_time = np.linspace(0, 1, len(resulting_voltages_nonoise_lowsample['A']))

#modes = vmd(short_circuit_current_withnoise_highsample)
#signal_time = np.linspace(0, 0.5, len(short_circuit_current_withnoise_highsample))

#modes = vmd(short_circuit_current_withnoise_lowsample)
#signal_time = np.linspace(0, 1, len(short_circuit_current_withnoise_lowsample))

#modes = vmd(short_circuit_current_nonoise_highsample)
#signal_time = np.linspace(0, 1, len(short_circuit_current_nonoise_highsample))

modes = vmd(short_circuit_current_nonoise_lowsample)
signal_time = np.linspace(0, 1, len(short_circuit_current_nonoise_lowsample))

# Plot the original signal and decomposed modes
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(signal_time, short_circuit_current_nonoise_lowsample, label='Original Signal')
plt.legend()

plt.subplot(2, 1, 2)
for i in range(modes.shape[1]):
    plt.plot(signal_time, modes[:, i], label=f'Mode {i + 1}')
plt.legend()

# Show the plots
plt.show()
