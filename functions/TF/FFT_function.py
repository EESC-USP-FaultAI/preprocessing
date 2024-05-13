import numpy as np


def FFT(x):  # FUNCTION THAT CALCULATES THE FFT OF A INPUT SIGNAL OF A VARIABLE (SIZE 2^n)

    N = len(x)

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


class fast_fourier_transform():
    def FFT(x):  # FUNCTION THAT CALCULATES THE FFT OF A INPUT SIGNAL OF A VARIABLE (SIZE 2^n)

        N = len(x)

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