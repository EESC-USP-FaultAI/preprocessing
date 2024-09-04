import numpy as np
import functions.TW as TW
import pandas as pd

# Função para dividir o sinal em janelas de um tamanho dado (amostras/ciclo)
def split_signal(s, window_size=512):
    """
    Splits the signal into windows of a given size.

    Parameters:
    - signal (array-like): Signal to be split.
    - window_size (int): Size of the windows.

    Returns:
    - list: List of windows.
    """

    windows = []
    if s.ndim == 1:
        for i in range(0, len(s), window_size):
            windows.append(s[i:i + window_size])
    else:
        for i in range(0, len(s[:, 1]), window_size):
            windows.append(s[i:i + window_size, :])
    return windows


"""
Function for the first metric,

Based on the article: One-Ended Fault Location Method Based on Machine Learning Models

"""


def energy_of_signal(s):

    sinal_janelado = split_signal(s)
    s = sinal_janelado[2]

    # The Clarke transformation is applied to the signal, which is a transformation used to convert a three-phase
    # system into a two-phase system.
    clark = clark_zero_transform(s)

    # The Discrete Wavelet Transform (DWT) is applied to the zero sequence component of the signal. The DWT is a tool
    # that can be used to analyze different components of a signal. In this case, we are using the DWT to decompose
    # the signal into its high and low frequency components. The 'evaluate_dwt_single_phase' function returns two
    # sets of coefficients: cA (approximation) and cD (detail). We are only interested in the detail coefficients (
    # cD), which represent the high frequency component of the signal.
    [_, cD] = TW.TW_PYWT.evaluate_dwt_single_phase(clark, 'db4')

    # The energy of the signal is calculated from the detail coefficients. Energy is a measure of the magnitude of
    # the signal and is calculated as the sum of the squares of the coefficients.
    energy = energy_sum_of_squares(cD)

    # The standard deviation of the detail coefficients is calculated.
    # The standard deviation is a measure of the variation or dispersion of the coefficients.
    std = standard_deviation(cD)

    # The function returns the energy and the standard deviation of the signal.
    return energy, std


"""
Function for the second metric,

Based on the article: Application of Machine Learning for Fault Classification and Location in a Radial Distribution 
Grid
"""
def calculate_metrics(s, level, wavelet):
    cD = []
    cA_temp = s

    # Perform the DWT on the signal for the given number of levels
    for _ in range(level):
        cA_temp, cD_temp = TW.TW_PYWT.evaluate_dwt_single_phase(cA_temp, wavelet)
        cD = cD_temp  # Atualiza a lista cD

    # Calculate the metrics for the detail coefficients
    metrics = [func(cD) for func in
               [skewness, mean, energy_sum_of_squares, entropy, standard_deviation, kurtosis]]
    return metrics

def metricas_yordanos(s, level=1, wavelet='db4', phase=1):
    """
    This function calculates several statistical measures for a given signal. The signal is first decomposed using the
    Discrete Wavelet Transform (DWT).

    Parameters:
    - s (matrix-like): The signal to be analyzed.
    - level (int): The level of decomposition in the DWT. Default is 1.
    - wavelet (str): The name of the wavelet to be used in the DWT. Default is 'db4'.

    Returns:
    - list: A list containing the calculated metrics for the signal. The metrics are as follows:
        - F1: Skewness of the signal.
        - F2: Mean of the signal.
        - F3: Energy of the signal, calculated using the sum of squares method.
        - F4: Entropy of the signal.
        - F5: Standard deviation of the signal.
        - F6: Kurtosis of the signal.
    """

    sinal_janelado = split_signal(s)
    s = sinal_janelado[2]

    data_phases = []
    dim = s.ndim
    if dim == 1:
        
        metrics = calculate_metrics(s, level, wavelet)
        data_phases.append(metrics)
    else:
        for i in range(s.shape[1]):
            metrics = calculate_metrics(s[:, i], level, wavelet)
            data_phases.append(metrics)

    return data_phases[phase-1]


# Implementação manual de skewness
def skewness(s):
    """
    Calculates the skewness of a signal.

    Parameters:
    - signal (array-like): Signal to be analyzed.

    Returns:
    - float: Skewness of the signal.
    """

    mean_value = sum(s) / len(s)
    variance = sum((x - mean_value) ** 2 for x in s) / len(s)
    std = variance ** 0.5
    skew = sum((x - mean_value) ** 3 for x in s) / (len(s) * std ** 3)
    return skew


# Implementação manual de mean
def mean(s):
    """
    Calculates the mean of a signal.

    Parameters:
    - signal (array-like): Signal to be analyzed.

    Returns:
    - float: Mean of the signal.
    """

    mean_value = sum(s) / len(s)
    return mean_value


# Implementação manual da entropy
def entropy(s):
    """
    Calculates the entropy of a signal.

    Parameters:
    - signal (array-like): Signal to be analyzed.

    Returns:
    - float: Entropy of the signal.
    """
    # Add a small positive constant to avoid undefined logarithm values
    s = s + 1e-10

    entropy_value = sum(-x * np.log(np.abs(x)) for x in s)
    return entropy_value


# Implementação manual da kurtosis
def kurtosis(s):
    """
    Calculates the kurtosis of a signal.

    Parameters:
    - signal (array-like): Signal to be analyzed.

    Returns:
    - float: Kurtosis of the signal.
    """

    mean_value = sum(s) / len(s)
    variance = sum((x - mean_value) ** 2 for x in s) / len(s)
    std = variance ** 0.5
    kurtosis_value = sum((x - mean_value) ** 4 for x in s) / (len(s) * std ** 4)
    return kurtosis_value


def energy_sum_of_squares(coef):
    """
    Calculates the energy of a signal using the sum of squares method.

    Parameters:
    - coef (array-like): Coefficients representing the signal.

    Returns:
    - float: Energy of the signal.
    """

    energy = sum(abs(c) ** 2 for c in coef)
    return energy


# Métrica de calcular desvio padrão de um vetor sem usar nenhuma biblioteca, comentado parametros e retorno
def standard_deviation(s):
    """
    Calculates the standard deviation of a signal.

    Parameters:
    - signal (array-like): Signal to be analyzed.

    Returns:
    - float: Standard deviation of the signal.
    """

    mean_value = sum(s) / len(s)
    variance = sum((x - mean_value) ** 2 for x in s) / len(s)
    return variance ** 0.5


def clark_zero_transform(s):
    result = 1 / 3 * (s[:, 0] + s[:, 1] + s[:, 2])
    return result


if __name__ == '__main__':
    # Load the signal
    df = pd.read_csv('C:\\Users\\caio\\Desktop\\dados_testes\\configuracao_2\\corrente\\'
                    'dados_cru_corrente_config_2.csv', skiprows=1)
    # Convert signal to matrix and remove the timestamp
    signal = df.to_numpy()
    signal = signal[:, 1:4]

    f1, f2, f3, f4, f5, f6 = metricas_yordanos(signal, 1, 'db4', 1)
    print(f2)

    energia, std = energy_of_signal(signal)
    print(energia)
