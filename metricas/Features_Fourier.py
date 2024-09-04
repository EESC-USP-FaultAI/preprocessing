import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## Include the directory of the project in the path to import the "functions"
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import functions.TF as tf

    
sym_matrix = np.array([
    [1.0/3.0, 1.0/3.0, 1.0/3.0],
    [1.0/3.0, -0.5/3.0 - 0.86602540378/3.0*1j, -0.5/3.0 + 0.86602540378/3.0*1j],
    [1.0/3.0, -0.5/3.0 + 0.86602540378/3.0*1j, -0.5/3.0 - 0.86602540378/3.0*1j]
])

def first_paper_features(data_fft):
    '''
        Based Papaer: 
            Fourier Transform and Probabilistic Neural Network based Fault Detection in Distribution System Containing DGs

        Description:
            This paper used the DFT to classify the fault in the distribution system. The algorithm used by the author estimates the magnitude and angle of the phasors using the Modified Full Cycle Discrete Fourier Transform (MFCDFT). After that, the author calculates the positive sequence component model matrix from the estimated phasors. 

        The features extracted from the paper are the following:
            - i_1: Positive sequence component

        Additional features outside of the paper:
            - i_0: Zero sequence component
            - i_2: Negative sequence component
    '''
    i012 = np.abs(np.einsum('ij, jk->ik', sym_matrix, data_fft[:,:,1]))
    F1 = np.concatenate([i012.mean(axis=-1), i012.std(axis=-1), statistical_values(i012)])
    return F1

def second_paper_feature(data_fft):
    '''
    Based Papaer:
        Modified FFT based high impedance fault detection technique considering distribution non-linear loads: Simulation and experimental data analysis
    
    Description:
        This paper uses the energy of the harmonic components to detect high impedance faults

    The following features are calculated:
        - h2: Harmonic 2
        - h3: Harmonic 3
        - h5: Harmonic 5
        - h7: Harmonic 7
        - h5/h3: Ratio of Harmonic 5 and Harmonic 3
        - h7/h3: Ratio of Harmonic 7 and Harmonic 3
        - (h7+h5)/h1: Ratio of Harmonic 7 and Harmonic 5
    '''
    h1 = np.mean(data_fft[:, :, 1], axis=-1)
    h2 = np.mean(data_fft[:, :, 2], axis=-1)
    h3 = np.mean(data_fft[:, :, 3], axis=-1)
    h5 = np.mean(data_fft[:, :, 5], axis=-1)
    h7 = np.mean(data_fft[:, :, 7], axis=-1)
    return np.concatenate([h2, h3, h5, h7, h5/h3, h7/h3, (h7+h5)/h1])

def third_paper_feature(data_fft, data_fft_angle, angRef_pos:int=0):
    '''
    Based Papaer:
        Fault Detection on Distribution Network Planning Using Fast Fourier Transform-Based Steady State and Transient Response
    
    Description:
        Fault classifier using maximum voltage and it's angle

    The following features are calculated:
        - Vmax: Maximum voltage of each phase
        - AngVmax: Angle of the maximum voltage of each phase
    '''
    
    idx_max = np.argmax(data_fft[:,:,1], axis=-1)
    v_max = data_fft[np.arange(data_fft.shape[0]), idx_max,1]
    ang_max = data_fft_angle[np.arange(data_fft.shape[0]), idx_max,1] - np.angle(data_fft[angRef_pos, idx_max[angRef_pos],1])
    return np.concatenate([v_max, ang_max])

def fourth_paper_feature(data_fft):
    '''
    Based Papaer:
        Frequency Estimation of Distorted and Noisy Signals in Power Systems by FFT-Based Approach

    Description:
        Frequency estimation of distorted and noisy signals in power systems by FFT-based approach

    The following features are calculated:
    '''
    #
    # beta = (|X[k2]| - |X[k1]|) / (|X[k2]| + |X[k1]|)
    beta = (data_fft[:, 1:, 0] - data_fft[:, :-1, 0]) / (data_fft[:, 1:, 0] + data_fft[:, :-1, 0])

def statistical_values(data):
    """
    Calculate statistical values from the input data.

    Parameters:
    data: numpy.ndarray
        Input data

    Returns:
    numpy.ndarray
        Statistical values (centroid, variance, skewness, kurtosis)
    """

    if len(data.shape) < 3:
        while len(data.shape) < 3:
            data = data[np.newaxis, ...]

    centroid_all = np.sum(data[:, :, :] * np.arange(data.shape[2]), axis=-1) / np.sum(data[:, :, :], axis=-1)
    centroid = np.mean(centroid_all, axis=-1)

    variance_all = np.var(data, axis=-1)
    variance = np.mean(variance_all, axis=-1)

    skewness_all = np.mean((data - centroid_all[:, :, np.newaxis])**3, axis=-1) / variance_all**1.5
    skewness = np.mean(skewness_all, axis=-1)

    kurtosis_all = np.mean((data - centroid_all[:, :, np.newaxis])**4, axis=-1) / variance_all**2
    kurtosis = np.mean(kurtosis_all, axis=-1)

    return np.concatenate([centroid, variance, skewness, kurtosis])

def dft_features(data, fs:int, base_freq:int=60):
    """
    Calculate the DFT features from the input data.

    Parameters
    ----------
    data : array-like
        Input data, 3 phase current and 3 phase voltage
    fs : int
        Sampling frequency
    base_freq : int, optional
        Base frequency, by default 60

    Returns
    -------
    array
        DFT features
    """
    if not isinstance(data, np.ndarray): data = np.array(data)
    if len(data.shape) == 1:
        data = data[np.newaxis, :]
    
    N = fs//base_freq

    if data.shape[1] < N: raise ValueError("Input data is too short for the given base frequency")
    assert data.shape[1] >= N, "Input data is too short for the given base frequency"

    slides = np.lib.stride_tricks.sliding_window_view(data, window_shape=N, axis=-1)
    data_fft = np.fft.fft(slides, axis=-1)
    # data_fft = np.apply_along_axis(tf.FFT, -1, slides)
    data_fft_angle = np.angle(data_fft[:,:,:N//2])
    data_fft = np.abs(data_fft[:,:,:N//2]) / (N//2)

    if data.shape[0] > 3:
        # The Paper uses Symetrical Components, it needs the value of the 3 phase current
        # I'm supposing that the 3 phase current is the first 3 channels
        # F1 = first_paper_features(data_fft[:3])
        F2 = second_paper_feature(data_fft[:3])
    elif data.shape[0] == 2:
        # F1 = first_paper_features(data_fft[:2])
        F2 = second_paper_feature(data_fft[:2])
    else: 
        # F1 = np.zeros((1,))
        F2 = np.zeros((1,))
        assert False, "The input data must have at least 3 channels"

    if data.shape[0] == 6:
        # The Paper uses the maximum voltage and its angle
        # I'm supposing that the voltage is the last 3 channels
        F3 = third_paper_feature(data_fft[3:], data_fft_angle[3:], 0)
    elif data.shape[0] == 2:
        F3 = third_paper_feature(data_fft[1:], data_fft_angle[1:], 0)
    else:
        F3 = np.zeros((1,))
        assert False, "The input data must have at least 3 channels"
    F4 = statistical_values(data_fft)
    return np.concatenate([F2,F3,F4])


if __name__ == '__main__':
    # Case 1
    df = pd.read_csv(r'C:\Users\alail\Downloads\dados_testes\configuracao_1\corrente\dados_cru_corrente_config_1.csv', skiprows=1)
    signal = df.to_numpy()
    signal = signal[:, 1:4].T
    df = pd.read_csv(r'C:\Users\alail\Downloads\dados_testes\configuracao_1\tensao\dados_cru_tensao_config_1.csv', skiprows=1)
    signal2 = df.to_numpy()
    signal2 = signal2[:, 1:4].T
    signal = np.concatenate([signal, signal2], axis=0)
    case_1_features = dft_features(signal, 30720, 60)

    # Case 2
    df = pd.read_csv(r'C:\Users\alail\Downloads\dados_testes\configuracao_2\corrente\dados_cru_corrente_config_2.csv', skiprows=1)
    signal = df.to_numpy()
    signal = signal[:, 1:4].T
    df = pd.read_csv(r'C:\Users\alail\Downloads\dados_testes\configuracao_2\tensao\dados_cru_tensao_config_2.csv', skiprows=1)
    signal2 = df.to_numpy()
    signal2 = signal2[:, 1:4].T
    signal = np.concatenate([signal, signal2], axis=0)
    case_2_features = dft_features(signal, 30720, 60)

    features = np.vstack([case_1_features, case_2_features])
    df = pd.DataFrame(features.T, columns=['Case 1', 'Case 2'])
    print(df)


