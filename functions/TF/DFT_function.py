import numpy as np
class discrete_fourier_transform():
    def DFT(x): #CALCULA A DFT DE UM SINAL REAL DE UMA VARIÁVEL

        N = len(x) #lê o tamanho do vetor x e atribui para N
        n = np.arange(N) #cria um vetor (matriz linha) com N-1 elementos espaçados de 1 em 1
        k = n.reshape((N, 1)) #altera o formato para uma matriz coluna
        e = np.exp(-2j * np.pi * k * n / N)

        X = np.dot(e, x) #calcula o produto matricial (produto ponto a ponto)

        return X
