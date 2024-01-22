import matplotlib.pyplot as plt
import numpy as np
from functions.SignalGenerator.GeraSinais import GeraSinais


def FFT(x): #FUNÇÃO QUE CALCULA A FFT DE UM SINAL REAL DE UMA VARIÁVEL (TAMANHO 2^n)
               #COMO GARANTIR 2^N? DEFINIDO PELA TAXA DE AMOSTRAGEM?
    N = len(x)

    if N == 1:
        return x
    else:
        X_even = FFT(x[::2]) #SEPARANDO OS ÍNDICES PARES x[start:stop:step]
        X_odd = FFT(x[1::2]) #SEPARANDO OS ÍNDICES ÍMPARES
        factor = \
            np.exp(-2j*np.pi*np.arange(N)/N) #EXPONENCIAIS COMPLEXAS (FREQ. FUND.)

        X = np.concatenate( \
            [X_even + factor[:int(N/2)] * X_odd,
             X_even + factor[int(N/2):] * X_odd])
        return X #RETORNA O VETOR TRANSFORMADO

#CALCULANDO A FFT PARA O SINAL SINTÉTICO GERADO PELA GABI (SINAL COM HARMÔNICOS E RUÍDO)

"""
Test 2 - Evaluating Generating Signals With Harmonics
"""
# Exemplo de uso da função com harmonics_start_time = 0.1 segundos
amplitude_fundamental = 10  # amplitude da fundamental
samples_per_cycle = 128
frequency = 60.0  # frequência em Hz
harmonics = [2, 3, 5]
amplitudes = [5, 3, 1]  # Adicione amplitudes correspondentes às harmônicas
duration = 16*(1/frequency) #como garantir o tamanho 2^n?
harmonics_start_time = 0.1  # tempo em segundos para começar a adicionar as harmônicas

# Example usage with noise
add_noise_harmonics = True  # Change this to True if you want to add noise
SNR_harmonics = 15  # Change this to set the SNR for the harmonics signal

time, generated_signal = GeraSinais.GenerateSignalWithHarmonics(
    amplitude_fundamental, samples_per_cycle, frequency, harmonics, amplitudes, duration, harmonics_start_time, add_noise_harmonics, SNR_harmonics
)

# Plota a forma de onda
plt.plot(time, generated_signal)
plt.title('Signal with Harmonics')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

X = FFT(generated_signal)


N = len(X)
n = np.arange(N)
T = N/(samples_per_cycle/(1/frequency)) #T = N/taxa_de_amostragem
freq = n/T

#plotando o espectro de amplitude

n_oneside = N//2
#pega apenas um lado das frequências
f_oneside = freq[:n_oneside]

#normaliza a amplitude
X_oneside =X[:n_oneside]/n_oneside

plt.figure(figsize = (12, 6))
plt.stem(f_oneside, abs(X_oneside), 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel('Frequency (Hz)')
plt.ylabel('FFT Normalized Amplitude |X(freq)|')
plt.xlim(0, 420)
plt.show()
#redução da amplitude de alguns harmonicos?