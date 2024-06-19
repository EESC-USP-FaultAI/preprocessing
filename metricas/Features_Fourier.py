import numpy as np
import pandas as pd

## Include the directory of the project in the path to import the "functions"
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import functions.TF as tf

def dft_features(data, fs:int, base_freq:int=60):
    """
    Calculate DFT features of the input data.
    Parameters:
    data: numpy.ndarray
        Input data. Shape: (n_channels, n_samples)
    fs: int
        Sampling frequency
    base_freq: int
        Base frequency of the input data. Default: 60
    Returns:
    numpy.ndarray
        DFT features of the input data
    """
    if len(data.shape) == 1:
        data = data[np.newaxis, :]
    
    N = fs//base_freq

    if data.shape[1] < N: raise ValueError("Input data is too short for the given base frequency")
    assert data.shape[1] >= N, "Input data is too short for the given base frequency"

    slides = np.lib.stride_tricks.sliding_window_view(data, window_shape=N, axis=-1)
    data_fft = np.fft.fft(slides, axis=-1)
    # data_fft = np.apply_along_axis(tf.FFT, -1, slides)
    data_fft = np.abs(data_fft[:,:,:N//2]) / (N//2)

    h1 = np.mean(data_fft[:, :, 1], axis=-1)
    h2 = np.mean(data_fft[:, :, 2], axis=-1)
    h3 = np.mean(data_fft[:, :, 3], axis=-1)
    h5 = np.mean(data_fft[:, :, 5], axis=-1)
    h7 = np.mean(data_fft[:, :, 7], axis=-1)

    centroid_all = np.sum(data_fft[:, :, :] * np.arange(N//2), axis=-1) / np.sum(data_fft[:, :, :], axis=-1)
    centroid = np.mean(centroid_all, axis=-1)

    variance_all = np.var(data_fft, axis=-1)
    variance = np.mean(variance_all, axis=-1)

    skewness_all = np.mean((data_fft - centroid_all[:, :, np.newaxis])**3, axis=-1) / variance_all**1.5
    skewness = np.mean(skewness_all, axis=-1)

    kurtosis_all = np.mean((data_fft - centroid_all[:, :, np.newaxis])**4, axis=-1) / variance_all**2
    kurtosis = np.mean(kurtosis_all, axis=-1)

    return np.concatenate([h2, h3, h5, h7, h5/h3, h7/h3, (h7+h5)/h1, centroid, variance, skewness, kurtosis])


if __name__ == '__main__':
    df = pd.read_csv(r'C:\Users\alail\Downloads\dados_testes\configuracao_2\corrente\dados_cru_corrente_config_2.csv', skiprows=1)
    signal = df.to_numpy()
    signal = signal[:, 1:4]

    features = dft_features(signal[:,0], 30720, 60)

    print(features)