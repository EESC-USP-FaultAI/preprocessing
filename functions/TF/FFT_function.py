import numpy as np

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

class fast_fourier_transform():
    def FFT(x):  # FUNÇÃO QUE CALCULA A FFT DE UM SINAL REAL DE UMA VARIÁVEL (TAMANHO 2^n)
# COMO GARANTIR 2^N? DEFINIDO PELA TAXA DE AMOSTRAGEM?

        N = len(x)

        if N == 1:
            return x
        else:
            X_even = FFT(x[::2])  # SEPARANDO OS ÍNDICES PARES x[start:stop:step]
            X_odd = FFT(x[1::2])  # SEPARANDO OS ÍNDICES ÍMPARES
            factor = \
                np.exp(-2j * np.pi * np.arange(N) / N)  # EXPONENCIAIS COMPLEXAS (FREQ. FUND.)

        X = np.concatenate( \
            [X_even + factor[:int(N / 2)] * X_odd,
            X_even + factor[int(N / 2):] * X_odd])
        return X  # RETORNA O VETOR TRANSFORMADO