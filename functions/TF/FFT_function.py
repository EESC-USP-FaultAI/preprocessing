import numpy as np


def FFT(x): 
    '''
    Function that calculates the Fast Fourier Transform (FFT) of a input signal (2^n).

    Parameters
    ----------
    x : array
        The input time series.

    Returns
    -------
    X : array
        The Fast Fourier Transform of the input signal.

    Examples
    --------
    >>> import functions.TF as tf
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> t = np.linspace(0, 10/60, 4096)
    >>> x = np.sin(2*np.pi*60*t) + 0.5*np.sin(2*np.pi*180*t)
    >>> x = list(x)
    >>> x_fft = np.abs(tf.FFT(x))
    >>> freq = np.arange(0, len(x_fft)) / (10/60)
    >>> plt.stem(freq[0:100], x_fft[0:100])
    >>> plt.xticks(np.arange(0, max(freq[0:100]), 60))
    '''

    if not isinstance(x, (np.ndarray, list, tuple)): raise ValueError('Input signal must be an array-like object.')
    
    N = len(x)

    if not N & (N - 1) == 0: raise ValueError('Input signal must have a length of 2^n.')

    if N == 1:
        return x
    else:
        X_even = FFT(x[0::2])  # SEPARATING EVEN INDEXES x[start:stop:step]
        X_odd = FFT(x[1::2])  # SEPARATING ODD INDIXES
        factor = \
            np.exp(-2j * np.pi * np.arange(N) / N)  # COMPLEX EXPONENTIALS (FUND. FREQ.)

        X = np.concatenate( \
            [X_even + factor[:int(N / 2)] * X_odd,
             X_even + factor[int(N / 2):] * X_odd])
        return X  # RETURN THE VECTOR TRANSFORMED


# class fast_fourier_transform():
#     def FFT(x):  # FUNCTION THAT CALCULATES THE FFT OF A INPUT SIGNAL OF A VARIABLE (SIZE 2^n)

#         N = len(x)

#         if N == 1:
#             return x
#         else:
#             X_even = FFT(x[0::2])  # SEPARATING EVEN INDEXES x[start:stop:step]
#             X_odd = FFT(x[1::2])  # SEPARATING ODD INDIXES
#             factor = \
#                 np.exp(-2j * np.pi * np.arange(N) / N)  # COMPLEX EXPONENTIALS (FUND. FREQ.)

#         X = np.concatenate( \
#             [X_even + factor[:int(N / 2)] * X_odd,
#              X_even + factor[int(N / 2):] * X_odd])
#         return X  # RETURN THE VECTOR TRANSFORMED