import numpy as np

def toeplitz(vetor, tam):
    n = len(vetor)
    matriz_toeplitz = [[0] * n for _ in range(tam)]

    for i in range(tam):
        for j in range(n):
            matriz_toeplitz[i][j] = vetor[abs(i - j)]

    return np.array(matriz_toeplitz)

class Stockwell():
    def calcula_TS_do_sinal(self, sinal, tamanho_da_janela):
        '''
        :param sinal: vetor numpy
        :param tamanho_da_janela: int que representa o tamanho da janela avaliada
        :return: matriz amp com a amplitude de cada amostra da S-matriz e matriz ang com o ângulo de cada amostra da S-matriz
        '''
        t0 = 0
        t1 = tamanho_da_janela

        for j in range(1, int(len(sinal)/tamanho_da_janela)+1):
            st = self.TS_da_janelada(sinal, t0, t1) #Calcula a TS janela a janela do sinal de entrada
            if j == 1:
                amp = st[1]
                ang = st[2]
            else:
                amp = np.concatenate([amp, st[1]], 1)
                ang = np.concatenate([ang, st[2]], 1)

            t0 = t1
            t1 = t0+tamanho_da_janela
        return amp, ang

    def TS_da_janelada(self, sinal, t0, t1):
        '''
        :param sinal: vetor numpy a ser avaliado
        :param t0: amostra inicial que marca o começo da janela avaliada no sinal
        :param t1: amostra final que marca o fim da janela avaliada no sinal
        :return: st é S-matriz, A é a amplitude de cada amostra da S-matriz e ang é o ângulo de cada amostra da S-matriz
        '''
        def angle(matrix):
            result = []
            for line in matrix:
                aux = []
                for i in line:
                    aux.append(np.arccos(i.real/abs(i)))
                result.append(aux)
            return result

        x = sinal[t0:t1] #Janelamento do sinal de entrada de acordo com a amostra de início t0 e de fim t1
        st = self.transformada_de_stockwell(x)

        A = 2*abs(st) #Calcula a amplitude de cada entrada da S-matriz
        ang=angle(st) #Calcula o ângulo de cada entrada da S-matriz
        return st, A, ang

    def transformada_de_stockwell(self, sinal):
        '''
        A função implementa o algoritmo de Dash
        :param sinal: vetor numpy
        :return: S-matriz
        '''
        k = 1  # fator de escala
        N = len(sinal)
        nhaf = N // 2
        odvn = N%2

        f = np.array([i / N for i in range(nhaf + 1)] + [-1 * j / N for j in range(nhaf - 1 + odvn, 0, -1)]) # Vetor com as frequências avaliadas pela TS
        Hft = np.fft.fft(sinal) #Transformada rápida de Fourier sobre o sinal de entrada
        invfk = 1 / f[1:nhaf + 1] #

        W = np.transpose(2 * np.pi * np.outer(f, invfk))
        G = np.exp((-k * W ** 2) / 2)  #Montagem das janelas gaussianas


        HW = toeplitz(Hft, nhaf+1) #Remodelagem do espectro de frequência de um vetor 1XN para um vetor NXN
        HW = HW[1:nhaf + 1, :]

        ST = np.fft.ifft(HW * G, axis=1) #Aplicação da janela gaussiana

        st0 = np.mean(sinal) * np.ones(N) #Cálculo da componente CC do sinal de entrada
        ST = np.vstack([st0, ST])

        return ST