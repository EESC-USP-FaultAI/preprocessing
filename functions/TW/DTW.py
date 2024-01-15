import matplotlib.pyplot as plt
import numpy as np


class DWT:
    @staticmethod
    def name(wavelet):
        """
        Returns the coefficients of the chosen wavelet.

        Parameters:
        - wavelet (str): The name of the desired wavelet.

        Returns:
        - List of low-pass (f_low) and high-pass (f_hi) decomposition coefficients.
        """
        if wavelet == 'db4':
            f_hi = [-0.2303778133088965, 0.7148465705529157,
                    -0.6308807679298589, -0.027983769416859854,
                    0.18703481171909309, 0.030841381835560764,
                    -0.0328830116668852, -0.010597401785069032]
            f_low = [-0.010597401785069032, 0.0328830116668852,
                     0.030841381835560764, -0.18703481171909309,
                     -0.027983769416859854, 0.6308807679298589,
                     0.7148465705529157, 0.2303778133088965]
            return [f_low, f_hi]

        return [None, None]

    @staticmethod
    def transform(data=None, *args, wavelet='db4', dec_low=None, dec_hi=None):
        """
        Performs a single step of the DWT based on the chosen wavelet or with explicit coefficients.

        Parameters:
        - data (array): The input time series.
        - *args: Variable positional arguments.
        - wavelet (str): The name of the desired wavelet.
        - dec_low (array): Low-pass coefficients for decomposition.
        - dec_hi (array): High-pass coefficients for decomposition.

        Returns:
        - List containing approximation (ca) and detail (cd) coefficients.
        """
        if not isinstance(wavelet, str):
            dec_low, dec_hi = args
        else:
            dec_low, dec_hi = DWT.name(wavelet)

        if data is None or dec_low is None or dec_hi is None:
            print("Invalid arguments")
            return [[], []]

        n = len(dec_low) - 1
        x0 = np.flip(data[0:n])
        x1 = np.flip(data[len(data) - n:len(data)])
        xn = np.concatenate((x0, data, x1))

        ca1 = np.convolve(xn, dec_low, mode='valid')
        ca = []

        cd1 = np.convolve(xn, dec_hi, mode='valid')
        cd = []

        for i in range(0, len(cd1)):
            if i % 2 != 0:
                cd.append(cd1[i])
                ca.append(ca1[i])

        return [ca, cd]

    @staticmethod
    def plot(ca, cd):
        """
        Plots the approximation (ca) and detail (cd) coefficients.

        Parameters:
        - ca (array): Approximation coefficients.
        - cd (array): Detail coefficients.

        Returns:
        - None
        """
        fig1, (ax1, ax2) = plt.subplots(2, 1)
        ax1.plot(ca)
        ax2.plot(cd)
        ax2.set_xlabel("Sample")
        ax1.set_ylabel("cA")
        ax2.set_ylabel("cD")
        ax1.grid(True)
        ax2.grid(True)
        plt.grid(True)
        plt.show()