"""
If the user wants to calculate the ST of a signal, they should use the method:
    def calculate_ST_of_the_signal(self, signal, window_size, k):

"""

import numpy as np

# function
def toeplitz(vetor, tam):
    n = len(vetor)
    matriz_toeplitz = [[0] * n for _ in range(tam)]

    for i in range(tam):
        for j in range(n):
            matriz_toeplitz[i][j] = vetor[abs(i - j)]

    return np.array(matriz_toeplitz)

# Stockwell Class 
class Stockwell():
    
    def calculate_ST_of_the_signal(self, signal, window_size, k):
        '''
        :param signal: vetor numpy
        :param window_size: int that represents the window size
        :param k: ST scale factor. It is usually 1.
        :return: Matrix "amp" with the amplitude and matrix "ang" with the angle of each smple of the ST-output matrixda S-matriz
        '''
        t0 = 0
        t1 = window_size

        for j in range(1, int(len(signal)/window_size)+1):
            st = self.window_ST(signal, t0, t1, k) # Calculate the ST at each window of the input signal
            if j == 1:
                amp = st[1]
                ang = st[2]
            else:
                amp = np.concatenate([amp, st[1]], 1)
                ang = np.concatenate([ang, st[2]], 1)

            t0 = t1
            t1 = t0+window_size
        return amp, ang

    def window_ST(self, signal, t0, t1, k):
        '''
        :param signal: numpy input vector 
        :param t0: Initial sample to mark the input of the evaluated window 
        :param t1: Last sample of the window 
        :param k: ST scale factor
        :return: st is the ST output matrix, A is the st amplitude and and is the ST angles at each sample of the window
        '''
        def angle(matrix):
            result = []
            for line in matrix:
                aux = []
                for i in line:
                    if abs(i) < 0.0001:
                        ang = 0
                    else:
                        ang = i.real / abs(i)

                    aux.append(np.arccos(ang))
                result.append(aux)
            return result

        x = signal[t0:t1] # Windowing of the signals according to the first (t0) and last (1) samples of the window   
        st = self.stockwell_transform(x, k)

        A = 2*abs(st) # Calculate the amplitude of ST output matrix 
        ang=angle(st) # Calculate the angle of ST output matrix 
        return st, A, ang

    def stockwell_transform(self, signal, k):
        '''
        The function implements the Dash ST algorithm
        :param signal: vetor numpy
        :param k: ST scale factor
        :return: S-matrix
        '''
        N = len(signal)
        nhaf = N // 2
        odvn = N%2

        f = np.array([i / N for i in range(nhaf + 1)] + [-1 * j / N for j in range(nhaf - 1 + odvn, 0, -1)]) # Vetor com as frequências avaliadas pela TS
        Hft = np.fft.fft(signal) # Fourier Transform of the input signal
        invfk = 1 / f[1:nhaf + 1] #

        W = np.transpose(2 * np.pi * np.outer(f, invfk))
        G = np.exp((-k * W ** 2) / 2)  # Assembly of the Gaussian windows

        HW = toeplitz(Hft, nhaf+1) # Remodeling the frequency spectra for a NXN vector
        HW = HW[1:nhaf + 1, :]

        ST = np.fft.ifft(HW * G, axis=1) # Applying the Gaussian Window
        st0 = np.mean(signal) * np.ones(N) # Calculating the input signal DC component
        ST = np.vstack([st0, ST])

        return ST
