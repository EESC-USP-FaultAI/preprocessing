import numpy as np
import matplotlib.pyplot as plt
from functions.SignalGenerator.SignalGenerator import GeraSinais


if __name__ == '__main__':

    def DFT(x): #CALCULA A DFT DE UM SINAL REAL DE UMA VARIÁVEL

        N = len(x) #lê o tamanho do vetor x e atribui para N
        n = np.arange(N) #cria um vetor (matriz linha) com N-1 elementos espaçados de 1 em 1
        k = n.reshape((N, 1)) #altera o formato para uma matriz coluna
        e = np.exp(-2j * np.pi * k * n / N)

        X = np.dot(e, x) #calcula o produto matricial (produto ponto a ponto)

        return X

    #CALCULANDO A DFT PARA O SINAL SINTÉTICO GERADO PELA GABI (SINAL COM HARMÔNICOS E RUÍDO)

    """
    Test 2 - Evaluating Generating Signals With Harmonics
    """
    # Exemplo de uso da função com harmonics_start_time = 0.1 segundos
    amplitude_fundamental = 10  # amplitude da fundamental
    samples_per_cycle = 128
    frequency = 60.0  # frequência em Hz
    harmonics = [2, 3, 5]
    amplitudes = [5, 3, 1]  # Adicione amplitudes correspondentes às harmônicas
    duration = 0.2
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

    X = DFT(generated_signal)

    #calculando a frequência
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
    plt.ylabel('DFT Normalized Amplitude |X(freq)|')
    plt.xlim(0, 420)
    plt.show()