

import numpy as np
import warnings
warnings.simplefilter("ignore", np.ComplexWarning)

# function
def toeplitz(vetor, tam):
    n = len(vetor)
    matriz_toeplitz = [[0] * n for _ in range(tam)]

    for i in range(tam):
        for j in range(n):
            matriz_toeplitz[i][j] = vetor[abs(i - j)]

    return np.array(matriz_toeplitz)

def calculate_ST_of_the_signal(signal, window_size, k):
    '''
    Calculate the Stockwell Transform of the input signal on a window basis

    Parameters
    ----------
    signal : numpy array
        Input signal.
    window_size : int
        Window size.
    k : int
        ST scale factor.
    
    Returns
    -------
    amp : numpy array
        Matrix "amp" with the amplitude of each sample of the ST-output matrix.
    ang : numpy array
        Matrix "ang" with the angle of each sample of the ST-output matrix.

    Examples
    --------
    >>> import functions.TS as TS
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> t = np.linspace(0, 4/60, 8192)
    >>> signal = np.sin(60*2*np.pi*t) + np.sin(180*2*np.pi*t)
    >>> signal_ST = TS.calculate_ST_of_the_signal(signal, 8192//16, 1)
    >>> for i in range(1, 9, 2):
    >>>     plt.plot(signal_ST[0][i, :], label=f'Harm {i}º')
    >>> plt.legend()
    '''

    if not isinstance(signal, np.ndarray): raise TypeError('The input signal must be a numpy array')
    if not isinstance(window_size, int): raise TypeError('The window size must be an integer')
    if not isinstance(k, int): raise TypeError('The ST scale factor must be an integer')
    if not window_size > 0: raise ValueError('The window size must be greater than zero')
    if not k > 0: raise ValueError('The ST scale factor must be greater than zero')

    window_size = int(window_size)
    t0 = 0
    t1 = window_size

    for j in range(1, int(len(signal)/window_size)+1):
        st = window_ST(signal, t0, t1, k) # Calculate the ST at each window of the input signal
        if j == 1:
            amp = st[1]
            ang = st[2]
        else:
            amp = np.concatenate([amp, st[1]], 1)
            ang = np.concatenate([ang, st[2]], 1)

        t0 = t1
        t1 = t0+window_size
    return amp, ang

def stockwell_transform(signal, k):
    '''
    Calculate the Stockwell Transform of the input signal

    Parameters
    ----------
    signal : numpy array
        Input signal.
    k : int
        ST scale factor.
    
    Returns
    -------
    ST : numpy array
        ST output matrix.
    '''
    N = len(signal)
    nhaf = N // 2
    odvn = N%2

    # f = np.array([i / N for i in range(nhaf + 1)] + [-1 * j / N for j in range(nhaf - 1 + odvn, 0, -1)]) # Vetor com as frequências avaliadas pela TS
    f = np.concatenate([
        np.arange(nhaf + 1) / N,
        -1 * np.arange(nhaf - 1 + odvn, 0, -1) / N
    ])

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

def angle_vectorized(matrix):
    divisors = np.divide(matrix.real, np.abs(matrix), out=np.zeros_like(matrix), where=np.abs(matrix) > 0.0001)
    angles_rad = np.arccos(divisors.real)
    return angles_rad

def window_ST(signal, t0, t1, k):
    '''
    :param signal: numpy input vector 
    :param t0: Initial sample to mark the input of the evaluated window 
    :param t1: Last sample of the window 
    :param k: ST scale factor
    :return: st is the ST output matrix, A is the st amplitude and and is the ST angles at each sample of the window
    '''

    x = signal[t0:t1] # Windowing of the signals according to the first (t0) and last (1) samples of the window   
    st = stockwell_transform(x, k)

    A = 2*abs(st) # Calculate the amplitude of ST output matrix 
    # ang=angle(st) # Calculate the angle of ST output matrix 
    ang = angle_vectorized(st) # Calculate the angle of ST output matrix 
    return st, A, ang



# # Stockwell Class 
# class Stockwell():
    
#     def calculate_ST_of_the_signal(self, signal, window_size, k):
#         '''
#         :param signal: vetor numpy
#         :param window_size: int that represents the window size
#         :param k: ST scale factor. It is usually 1.
#         :return: Matrix "amp" with the amplitude and matrix "ang" with the angle of each smple of the ST-output matrixda S-matriz
#         '''
#         t0 = 0
#         t1 = window_size

#         for j in range(1, int(len(signal)/window_size)+1):
#             st = self.window_ST(signal, t0, t1, k) # Calculate the ST at each window of the input signal
#             if j == 1:
#                 amp = st[1]
#                 ang = st[2]
#             else:
#                 amp = np.concatenate([amp, st[1]], 1)
#                 ang = np.concatenate([ang, st[2]], 1)

#             t0 = t1
#             t1 = t0+window_size
#         return amp, ang

#     def window_ST(self, signal, t0, t1, k):
#         '''
#         :param signal: numpy input vector 
#         :param t0: Initial sample to mark the input of the evaluated window 
#         :param t1: Last sample of the window 
#         :param k: ST scale factor
#         :return: st is the ST output matrix, A is the st amplitude and and is the ST angles at each sample of the window
#         '''
#         def angle(matrix):
#             result = []
#             for line in matrix:
#                 aux = []
#                 for i in line:
#                     if abs(i) < 0.0001:
#                         ang = 0
#                     else:
#                         ang = i.real / abs(i)

#                     aux.append(np.arccos(ang))
#                 result.append(aux)
#             return result

#         x = signal[t0:t1] # Windowing of the signals according to the first (t0) and last (1) samples of the window   
#         st = self.stockwell_transform(x, k)

#         A = 2*abs(st) # Calculate the amplitude of ST output matrix 
#         ang=angle(st) # Calculate the angle of ST output matrix 
#         return st, A, ang

#     def stockwell_transform(self, signal, k):
#         '''
#         The function implements the Dash ST algorithm
#         :param signal: vetor numpy
#         :param k: ST scale factor
#         :return: S-matrix
#         '''
#         N = len(signal)
#         nhaf = N // 2
#         odvn = N%2

#         f = np.array([i / N for i in range(nhaf + 1)] + [-1 * j / N for j in range(nhaf - 1 + odvn, 0, -1)]) # Vetor com as frequências avaliadas pela TS
#         Hft = np.fft.fft(signal) # Fourier Transform of the input signal
#         invfk = 1 / f[1:nhaf + 1] #

#         W = np.transpose(2 * np.pi * np.outer(f, invfk))
#         G = np.exp((-k * W ** 2) / 2)  # Assembly of the Gaussian windows

#         HW = toeplitz(Hft, nhaf+1) # Remodeling the frequency spectra for a NXN vector
#         HW = HW[1:nhaf + 1, :]

#         ST = np.fft.ifft(HW * G, axis=1) # Applying the Gaussian Window
#         st0 = np.mean(signal) * np.ones(N) # Calculating the input signal DC component
#         ST = np.vstack([st0, ST])

#         return ST
