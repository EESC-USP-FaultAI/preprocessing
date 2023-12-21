from api.GeraSinais import GeraSinais
from waveletTransform import WaveletTransform

# Entrar com os sinais gerados

# Exemplo do sinal de um afundamento de tensão
sinais_sag = GeraSinais.voltage_sag_short_circuit(.9, 0.01, 0.02, 0.03, 60, 'A',
                                                  True, 30)

# Exemplo dos sinais de uma falta
sinais_fault = GeraSinais.short_circuit_current(100, 60, 0.0125, 7,
                                                0.5, .016, 128, False, 100)

ca, cd = WaveletTransform.dwt(sinais_fault,'db4')

mca, mcd = WaveletTransform.mdwt(sinais_fault,'db4')

#coef_aproximacao, coef_detalhe = wavedec(sinal_entrada, wavelet_mae, compressao=fator_compressao,
#                                         translacao=fator_translacao)
print("Coeficientes de Aproximação função pronta:", ca)
print("Coeficientes de Detalhe função pronta:", cd)

# TODO: Está com erro a função própria
print("Coeficientes de Aproximação nossa função:", mca)
print("Coeficientes de Detalhe nossa função:", mcd)