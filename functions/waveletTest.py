from api.GeraSinais import GeraSinais
from waveletTransform import WaveletTransform


# Entrar com os sinais gerados

# Exemplo do sinal de um afundamento de tensão
sinais_sag = GeraSinais.voltage_sag_short_circuit(.9, 0.01, 0.02, 0.03, 60, 'A',
                                                  True, 30)

# Exemplo dos sinais de uma falta
time, sinais_fault = GeraSinais.short_circuit_current(100, 60, 0.0125, 7,
                                                0.5, .016, 8*60, False, 100)

time2, sinais_fault2 = GeraSinais.short_circuit_current(100, 60, 0.0125, 7,
                                                0.5, .016, 12*60, False, 100)

print('falta')
print(sinais_fault2)

ca, cd = WaveletTransform.dwt(sinais_fault,'db4')


print("Vetor: {}".format(sinais_fault))

#coef_aproximacao, coef_detalhe = wavedec(sinal_entrada, wavelet_mae, compressao=fator_compressao,
#                                         translacao=fator_translacao)

print("     ")
print("Coeficientes de Aproximação função pronta:", ca)
print("Coeficientes de Detalhe função pronta:", cd)
print("     ")


import numpy as np
import pywt

def evaluate_dwt_manually_single_phase(data, wavelet_name):
    """
    Evaluate Discrete Wavelet Transform using scientifc package NumPy for convolution.
    :param data: single-phase signal to perform transform
    :param wavelet_name: name of mother wavelet
    :return: Approximation and Detail coefficients
    """
    wavelet = pywt.Wavelet(wavelet_name)
    dec_low = wavelet.dec_lo
    dec_high = wavelet.dec_hi
    cA = []
    cD = []

    cA_aux = np.convolve(data, dec_low)
    cD_aux = np.convolve(data, dec_high)

    for i in range(len(cA_aux)):
        if i % 2 == 1:
            cA.append(cA_aux[i])
            cD.append(cD_aux[i])
    cA = np.array(cA)
    cD = np.array(cD)

    return cA, cD


ca1, cd1 = evaluate_dwt_manually_single_phase(sinais_fault,'db4')


print("     ")
print("Coeficientes de Aproximação função pronta1:", ca1)
print("Coeficientes de Detalhe função pronta1:", cd1)
print("     ")

print(pywt.Wavelet('db4').dec_lo)