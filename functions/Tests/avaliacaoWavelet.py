
"""
Código para avaliar o tempo de processamento de sinais
"""

from functions.SignalGenerator.SignalGenerator import GeraSinais
from functions.TW.DTW import DWT
import time
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    # Passo 1: Gera o sinal sintético
    amplitude_fundamental = 10  # amplitude da fundamental
    samples_per_cycle = 128
    frequency = 60.0  # frequencia em Hz
    harmonics = [2, 3, 5]
    amplitudes = [5, 3, 1]  # Adicione amplitudes correspondentes às harmônicas
    duration = 0.2
    harmonics_start_time = 0.1  # tempo em segundos para começar a adicionar as harmônicas
    add_noise_harmonics = True  # Change this to True if you want to add noise
    SNR_harmonics = 30  # Change this to set the SNR for the harmonics signal

    tempo_sinal, signal = GeraSinais.GenerateSignalWithHarmonics(
        amplitude_fundamental, samples_per_cycle, frequency, harmonics, amplitudes, duration, harmonics_start_time, add_noise_harmonics, SNR_harmonics
    )

    # Passo 2: Avalia o tempo de processamrnto do sinal
    # Criar uma instância da classe Wavelet
    wavelet_instance = DWT()
    # Chamar o método calcula_DWT_do_sinal da instância DWT_instance

    start_time = time.time()
    ca, cd = wavelet_instance.transform(signal, 'db4')
    end_time = time.time()

    tempo_execucao_milissegundos = (end_time - start_time)

    print(f'Tempo de Processamento: {tempo_execucao_milissegundos:.4f} s')
