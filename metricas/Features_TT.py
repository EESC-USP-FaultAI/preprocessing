import numpy as np
from functions.TT import clarke as clk
from functions.TT import componentes_simetricas as cs


def extract_feature_TT(signal_voltage_A, signal_corrent_A, signal_voltage_B, signal_corrent_B, signal_voltage_C, signal_corrent_C, tempo_inicio, sample_cycle):
    inicio_falta = int(tempo_inicio*sample_cycle*60)
    
    # Impedância incremental
    ia_super = signal_corrent_A[inicio_falta: inicio_falta+sample_cycle] - signal_corrent_A[inicio_falta-sample_cycle:inicio_falta]
    ib_super = signal_corrent_B[inicio_falta: inicio_falta+sample_cycle] - signal_corrent_B[inicio_falta-sample_cycle:inicio_falta]
    ic_super = signal_corrent_C[inicio_falta: inicio_falta+sample_cycle] - signal_corrent_C[inicio_falta-sample_cycle:inicio_falta]
    
    va_super = signal_voltage_A[inicio_falta: inicio_falta+sample_cycle] - signal_voltage_A[inicio_falta-sample_cycle:inicio_falta]
    vb_super = signal_voltage_B[inicio_falta: inicio_falta+sample_cycle] - signal_voltage_B[inicio_falta-sample_cycle:inicio_falta]
    vc_super = signal_voltage_C[inicio_falta: inicio_falta+sample_cycle] - signal_voltage_C[inicio_falta-sample_cycle:inicio_falta]
    
    I_componentes_simetricas = cs.comp_sim_ABCto012(np.fft.fft(ia_super)[1], np.fft.fft(ib_super)[1], np.fft.fft(ic_super)[1])
    V_componentes_simetricas = cs.comp_sim_ABCto012(np.fft.fft(va_super)[1], np.fft.fft(vb_super)[1], np.fft.fft(vc_super)[1])

    Z0 = V_componentes_simetricas[0]/I_componentes_simetricas[0]
    Z1 = V_componentes_simetricas[1]/I_componentes_simetricas[1]
    Z2 = V_componentes_simetricas[2]/I_componentes_simetricas[2]
    
    
    # Autovalores da matriz de clarke
    window_size = 3
    ia_window = signal_corrent_A[inicio_falta: inicio_falta+window_size*sample_cycle]
    ib_window = signal_corrent_B[inicio_falta: inicio_falta+window_size*sample_cycle]
    ic_window = signal_corrent_C[inicio_falta: inicio_falta+window_size*sample_cycle]
    
    i_alfa=[]
    i_beta=[]
    i_0 = []
    for i in range(0, len(ia_window)-sample_cycle):
        i_clarke = clk.clarke_ABCtoAB0(np.fft.fft(ia_window[i:i+sample_cycle])[1], 
                                       np.fft.fft(ib_window[i:i+sample_cycle])[1],
                                       np.fft.fft(ic_window[i:i+sample_cycle])[1])
    
        i_alfa.append(i_clarke[0])
        i_beta.append(i_clarke[1])
        i_0.append(i_clarke[2])
    
    
    A = np.array([i_alfa, i_beta, i_0])
    B = np.dot(A, A.T)
    
    eig_values = np.linalg.eig(B)[0] 
       
    return abs(complex(Z0)), abs(complex(Z1)), abs(complex(Z2)), abs(complex(eig_values[0])), abs(complex(eig_values[1])), abs(complex(eig_values[2]))