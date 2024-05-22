import numpy as np


def DFT(x): #EVALUATE THE DFT OF A ONE DIMENTIONAL INPUT SIGNAL
    '''
    Evaluate the Discrete Fourier Transform of a one dimentional input signal

    Parameters
    ----------
    x : array
        The input time series.

    Returns
    -------
    X : array
        The Discrete Fourier Transform of the input signal.

    Examples
    --------
    >>> import functions.TF as tf
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> t = np.linspace(0, 10/60, 4800)
    >>> x = np.sin(2*np.pi*60*t) + 0.5*np.sin(2*np.pi*180*t)
    >>> x = list(x)
    >>> x_dft = tf.DFT(x)
    >>> freq = np.arange(0, 4800) / (10/60)
    >>> plt.stem(freq[0:100], x_dft[0:100])
    >>> plt.xticks(np.arange(0, max(freq[0:100]), 60))
    '''

    if not isinstance(x, (np.ndarray, list, tuple)): raise ValueError('Input signal must be an array-like object.')

    N = len(x) #reads the size of vector x and assigns it to N
    n = np.arange(N) #creates a vector (row matrix) with N-1 elements spaced 1 by 1
    k = n.reshape((N, 1)) #changes the format to a column matrix
    e = np.exp(-2j * np.pi * k * n / N)

    X = np.dot(e, x) #perform the DFT calculating the matrix product (point-to-point product)

    return X


# class discrete_fourier_transform():
#     def DFT(x): #EVALUATE THE DFT OF A ONE DIMENTIONAL INPUT SIGNAL

#         N = len(x) #reads the size of vector x and assigns it to N
#         n = np.arange(N) #creates a vector (row matrix) with N-1 elements spaced 1 by 1
#         k = n.reshape((N, 1)) #changes the format to a column matrix
#         e = np.exp(-2j * np.pi * k * n / N)

#         X = np.dot(e, x) #perform the DFT calculating the matrix product (point-to-point product)

#         return X
