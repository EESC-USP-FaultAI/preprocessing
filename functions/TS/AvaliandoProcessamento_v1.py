
"""
Código para avaliar o tempo de processamento de sinais
Será utilizado o sinal gerado com harmônicas
"""

from GeraSinais import GeraSinais  # Import the class from the module
from StockwellTransform import Stockwell
import time
import matplotlib.pyplot as plt
import numpy as np

# Passo 1: Gera o sinal sintético
amplitude_fundamental = 10  # amplitude da fundamental
samples_per_cycle = 128
frequency = 60.0  # frequencia em Hz
harmonics = [2, 3, 5]
amplitudes = [5, 3, 1]  # Adicione amplitudes correspondentes às harmônicas
duration = 0.2
harmonics_start_time = 0.1  # tempo em segundos para começar a adicionar as harmônicas
add_noise_harmonics = False  # Change this to True if you want to add noise
SNR_harmonics = 15  # Change this to set the SNR for the harmonics signal

tempo_sinal, signal = GeraSinais.GenerateSignalWithHarmonics(
    amplitude_fundamental, samples_per_cycle, frequency, harmonics, amplitudes, duration, harmonics_start_time, add_noise_harmonics, SNR_harmonics
)

# Passo 2: Avalia o tempo de processamrnto do sinal
# Criar uma instância da classe Stockwell
stockwell_instance = Stockwell()
# Chamar o método calcula_TS_do_sinal da instância stockwell_instance
start_time = time.time()
amp, ang = stockwell_instance.calcula_TS_do_sinal(signal, samples_per_cycle, 3)
end_time = time.time()
tempo_total = end_time - start_time

# plot a linha 1 (fundamental) e as linhas onde tiverem as harmônicas
# Número de harmônicas
num_harm = len(harmonics) + 1

# Criar subplots para 'amp'
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

plt.suptitle(f'Tempo de Processamento: {tempo_total:.4f} segundos', y=1.02)
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