import numpy as np

'''
Metricas de preprocessamentop para wavelet
'''

'''
Listando:
- Média (ok)
- Mediana (ok)
- Desvio Padrão (ok) / Variância (ok)
- Kurtosis (Curtose)
- Entropia
    - Entropia de Shannon / Rényi (generalizada);
    - Permutation Entropy;
- Energia do sinal
    - Energia dos coeficientes da Wavelet.
'''


def mean(coef):
    """
    Calculate mean value of wavelet coefficients.
    :param coef: Coefficients obtained with Wavelet Transform
    :return: Mean value of the given wavelet coefficients.
    """
    data_sum = 0  # Variable to store sum of values
    data_length = len(coef)  # Number of samples

    # Loop to sum up of coefficients values
    for i in range(data_length):
        data_sum += coef[i]

    coef_mean = data_sum / data_length  # Compute mean value

    return coef_mean


def median(coef):
    """
    Calculate median value of wavelet coefficients
    :param coef: Coefficients obtained with Wavelet Transform
    :return: Median value of the given wavelet coefficients
    """
    data_length = len(coef)  # Number of samples

    # Loop to sort coefficients values
    count = 0  # Auxiliary variable to sort values
    while count < data_length - 1:
        for i in range(count+1, data_length):
            smaller = coef[i]
            smaller_id = i
            if smaller > coef[i]:
                smaller = coef[i]
                smaller_id = i
            coef[smaller_id] = coef[count]
            coef[count] = smaller
        count += 1

    # Compute median value
    n_mean = data_length / 2
    if data_length % 2 == 0:  # Even number of values
        coef_median = (coef[n_mean] + coef[n_mean-1])/2
    else:  # Odd number of values
        coef_median = coef[int(n_mean)]

    return coef_median


def variance(coef):
    """
    Calculate variance of wavelet coefficients
    :param coef: Coefficients obtained with Wavelet Transform
    :return: Variance value of the given wavelet coefficients
    """
    data_length = len(coef)  # Number of values
    mean_value = mean(coef)  # Mean value of coefficients

    square_diff_sum = 0  # variable to stor sum of square differences

    # Loop to compute sum of square differences
    for i in range(data_length):
        square_diff_sum += (coef[i] - mean_value)**2

    # Compute variance of values
    coef_variance = square_diff_sum / (data_length - 1)

    return coef_variance


def standard_deviation(coef):
    """
    Calculate standard deviation of wavelet coefficients
    :param coef: Coefficients obtained with Wavelet Transform
    :return: Standard deviation value of the given wavelet coefficients
    """

    # following: S = sqrt(variance)
    variance_value = variance(coef)

    # Compute standard deviation value
    coef_std_dev = np.sqrt(variance_value)

    return coef_std_dev

'''
Análise da energia do sinal atraves de tal e tal
'''


'''
Função para calcular a entropia do sinal
'''


'''
Funções para calcular a energia e a densidade de energia
'''