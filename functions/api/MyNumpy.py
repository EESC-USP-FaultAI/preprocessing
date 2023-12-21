def convolution(sinal, filtro):
    len_sinal = len(sinal)
    len_filtro = len(filtro)
    len_resultado = max(len_sinal - len_filtro + 1, 0)

    result = [0] * len_resultado

    for i in range(len_resultado):
        for j in range(len_filtro):
            result[i] += sinal[i + j] * filtro[j]

    return result