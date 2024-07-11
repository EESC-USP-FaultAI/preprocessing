import numpy as np
from scipy.stats import entropy
from functions.TS import ST as TS


def entropia(MAF):
    # Normalizar o sinal para formar uma distribuição de probabilidade
    signal_prob = np.array(MAF) / np.sum(MAF)

    # Calcular a entropia
    signal_entropy = entropy(signal_prob)
    
    return signal_entropy

def energia(TS):
    return [sum([x**2 for x in linha]) for linha in TS] 
    

def extract_feature_TS(sinal, tempo_inicio, sample_cycle):

    window_size = sample_cycle
    
    inicio_falta = int(tempo_inicio*sample_cycle*60)

    sinal_pre = sinal[inicio_falta-sample_cycle:inicio_falta]
    sinal_pos = sinal[inicio_falta:inicio_falta+sample_cycle]
    
    ts_pre = TS.calculate_ST_of_the_signal(sinal_pre, window_size, 1)
    ts_pos = TS.calculate_ST_of_the_signal(sinal_pos, window_size, 1)
        
    ts_pre = np.array(ts_pre)
    ts_pos = np.array(ts_pos)
    
    # Métrica de 1 ciclo de pos e 128 amostras pos ciclo  
    #### Ciclo de pré-falta
    MAT_pre = [max(linha) for linha in ts_pre.T[0]]
    Fn = max(MAT_pre) + min(MAT_pre)
    
    #### Ciclo de pós-falta    
    MAF = [max(linha) for linha in ts_pos[0]]
    MAT = [max(linha) for linha in ts_pos.T[0]]
        
    F1 = 1 - (max(MAT) + min(MAT)) - Fn
    F2 = entropia(MAF)
    F3 = max(MAF)
    MET = [x**2 for x in MAT]
    F4 = max(MET)
    F5 = max(MAT)
    
    # Métrica janela de 30ms e 256 harmonicos
    e = energia(ts_pos[0][0:5])   
    F6 = e[0]
    F7 = e[1]
    F8 = e[2]
    F9 = e[3]
    F10 = e[4]
    
    return F1, F2, F3, F4, F5, F6, F7, F8, F9, F10
    