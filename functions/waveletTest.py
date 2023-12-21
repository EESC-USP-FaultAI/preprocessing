from api.GeraSinais import GeraSinais

# Entrar com os sinais gerados

# Exemplo do sinal de um afundamento de tensão
sinais_sag = GeraSinais.voltage_sag_short_circuit(.9, 0.01, 0.02, 0.03, 60, 'A',
                                                  True, 30)

# Exemplo dos sinais de uma falta
sinais_fault = GeraSinais.short_circuit_current(100, 60, 0.0125, 7,
                                                0.5, .016, 128, False, 100)