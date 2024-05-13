import numpy as np
class discrete_fourier_transform():
    def DFT(x): #EVALUATE THE DFT OF A ONE DIMENTIONAL INPUT SIGNAL

        N = len(x) #reads the size of vector x and assigns it to N
        n = np.arange(N) #creates a vector (row matrix) with N-1 elements spaced 1 by 1
        k = n.reshape((N, 1)) #changes the format to a column matrix
        e = np.exp(-2j * np.pi * k * n / N)

        X = np.dot(e, x) #perform the DFT calculating the matrix product (point-to-point product)

        return X
