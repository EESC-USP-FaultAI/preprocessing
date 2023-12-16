import numpy as np
import pywt

#wavelet_mae1 = pywt.Wavelet('db4')
#print(wavelet_mae1)


def convolucao_sinais(sinal, filtro):
    len_sinal = len(sinal)
    len_filtro = len(filtro)
    len_resultado = max(len_sinal - len_filtro + 1, 0)

    resultado = [0] * len_resultado

    for i in range(len_resultado):
        for j in range(len_filtro):
            resultado[i] += sinal[i + j] * filtro[j]

    return resultado



def wavedec(sinal, wavelet_mae, compressao=1.0, translacao=0.0):
    """
    Implementação básica da transformada wavelet discreta com parâmetros de compressão e translação.

    Parâmetros:
    - sinal: array-like
        O sinal a ser transformado.
    - wavelet_mae: str
        Nome da wavelet mãe.
    - compressao: float, opcional (padrão=1.0)
        Fator de compressão para os coeficientes.
    - translacao: float, opcional (padrão=0.0)
        Fator de translação para os coeficientes.

    Retorna:
    - coef_aproximacao: list
        Lista contendo os coeficientes de aproximação da transformada wavelet.
    - coef_detalhe: list
        Lista contendo os coeficientes de detalhe da transformada wavelet.
    """
    # Obtém a wavelet mãe
    wavelet_mae = pywt.Wavelet(wavelet_mae)

    n = len(sinal)
    h = len(wavelet_mae.dec_lo)

    # Inicializa as listas de coeficientes
    coef_aproximacao = []
    coef_detalhe = []

    while n >= h:
        # Obtém os coeficientes da wavelet mãe
        dec_lo = wavelet_mae.dec_lo
        dec_hi = wavelet_mae.dec_hi

        dec_lo = [x * compressao for x in dec_lo]
        dec_hi = [x * compressao for x in dec_hi]

        dec_lo = [x + translacao for x in dec_lo]
        dec_hi = [x + translacao for x in dec_hi]

        # Convolução do sinal com os coeficientes da wavelet mãe
        #aproximacao = np.convolve(sinal, dec_lo, mode='valid') * compressao + translacao
        #detalhes = np.convolve(sinal, dec_hi, mode='valid') * compressao + translacao
        aproximacao = convolucao_sinais(sinal, dec_lo)
        detalhes = convolucao_sinais(sinal, dec_hi)

        # Armazena os coeficientes de aproximação e detalhes
        coef_aproximacao.append(aproximacao)
        coef_detalhe.append(detalhes)

        # Atualiza o sinal para o próximo nível
        sinal = aproximacao

        # Divide o tamanho do sinal pela metade
        n //= 2

    # Adiciona o último nível de aproximação
    coef_aproximacao.append(sinal)

    # Inverte as listas para que o nível mais baixo seja o primeiro
    coef_aproximacao.reverse()
    coef_detalhe.reverse()

    return coef_aproximacao, coef_detalhe


# Exemplo de uso
sinal_entrada = np.random.rand(128)  # Substitua isso pelo seu sinal de entrada
wavelet_mae = 'db4'  # Substitua isso pelo nome da wavelet mãe desejada
fator_compressao = 1.0  # Substitua pelo fator de compressão desejado
fator_translacao = 0.0  # Substitua pelo fator de translação desejado

coef_aproximacao, coef_detalhe = wavedec(sinal_entrada, wavelet_mae, compressao=fator_compressao,
                                         translacao=fator_translacao)
print("Coeficientes de Aproximação:", coef_aproximacao)
print("Coeficientes de Detalhe:", coef_detalhe)
