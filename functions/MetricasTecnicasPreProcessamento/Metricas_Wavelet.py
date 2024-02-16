import numpy as np
import scipy as sc  # Used for testing

'''
Metricas de preprocessamentop para wavelet
'''

'''
Listando:
- Média (ok)
- Mediana (ok)
- Desvio Padrão (ok) / Variância (ok)
- Kurtosis (Curtose) (ok)
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
    :return: Mean value of given wavelet coefficients.
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
    :return: Median value of given wavelet coefficients
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
    n_mean = int(data_length / 2)
    if data_length % 2 == 0:  # Even number of values
        coef_median = (coef[n_mean] + coef[n_mean-1])/2
    else:  # Odd number of values
        coef_median = coef[int(n_mean)]

    return coef_median


def variance(coef, ddof=0):
    """
    Calculate variance of wavelet coefficients
    :param coef: Coefficients obtained with Wavelet Transform
    :param ddof: “Delta Degrees of Freedom”: the divisor used in the calculation
    is N - ddof, where N represents the number of elements. By default ddof is zero.
    :return: Variance value of given wavelet coefficients
    """
    data_length = len(coef)  # Number of values
    mean_value = mean(coef)  # Mean value of coefficients

    square_diff_sum = 0  # variable to stor sum of square differences

    # Loop to compute sum of square differences
    for i in range(data_length):
        square_diff_sum += abs(coef[i] - mean_value)**2

    # Compute variance of values
    coef_variance = square_diff_sum / (data_length-ddof)

    return coef_variance


def standard_deviation(coef, ddof=0):
    """
    Calculate standard deviation of wavelet coefficients
    :param coef: Coefficients obtained with Wavelet Transform
    :param ddof: “Delta Degrees of Freedom”: the divisor used in the calculation
    is N - ddof, where N represents the number of elements. By default ddof is zero.
    :return: Standard deviation value of given wavelet coefficients
    """

    # following: S = sqrt(variance)
    variance_value = variance(coef, ddof=ddof)

    # Compute standard deviation value
    coef_std_dev = np.sqrt(variance_value)

    return coef_std_dev


def kurtosis(coef, fisher=True):  # Fisher's Kurtosis
    """
    Calculate kurtosis (Fisher or Pearson) of wavelet coefficients
    :param coef: Coefficients obtained with Wavelet Transform
    :param fisher: If true subtract 3.0 from the result to give 0.0 for a normal distribution (default=true)
    :return: Kurtosis value of given wavelet coefficients
    """
    data_length = len(coef)  # Number of values
    mean_value = mean(coef)  # Mean value of coefficients
    square_variance_value = variance(coef)**2  # Square variance of coefficients

    forth_diff_sum = 0  # variable to stor sum of square differences

    # Loop to compute sum of forth differences
    for i in range(data_length):
        forth_diff_sum += (coef[i] - mean_value) ** 4

    # Compute forth central moment
    forth_moment_value = forth_diff_sum / data_length

    # Compute kurtosis value
    if fisher:
        coef_kurtosis = (forth_moment_value / square_variance_value) - 3.0
    else:
        coef_kurtosis = (forth_moment_value / square_variance_value)

    return coef_kurtosis


def shannon_entropy(coef):
    # Preciso descobrir o que está errado...
    """
    Calculate Shannon Entropy of wavelet coefficients
    :param coef: Coefficients obtained with Wavelet Transform
    :return: Shannon Entropy value of given wavelet coefficients
    """
    data_log_sum = 0  # Variable to store sum of values
    data_length = len(coef)  # Number of values

    # Compute Probability Mass Function
    unique_values, counts = np.unique(coef, return_counts=True)
    pmf_values = counts / data_length
    pmf_dict = dict(zip(unique_values, pmf_values))

    # Probability values of each coefficient
    pmfi = []
    for i in range(data_length):
        pmfi.append(pmf_dict.get(coef[i]))
    pmfi = np.array(pmfi)

    # Normalize values
    if np.sum(pmfi) != 1:
        pmfi = pmfi / np.sum(pmfi)

    # Loop to compute sum of all possible values of x
    for k in range(data_length):
        pk = pmfi[k]
        data_log_sum += pk*np.log2(pk)

    # Compute the shannon entropy as the negative of log sum
    coef_shanon_entropy = -data_log_sum

    return coef_shanon_entropy



""" Quick Test """
a = [1, 2, 3, 4, 5, 6, 7, 10, 12, 53, 60, 12, 45, 214]
a = np.array(a)

print("Array a:", a)
# Mean
print("Mean using numpy: %.4f" % (np.mean(a)))
print("Mean using function: %.4f" % (mean(a)))
# Median
print("Median using numpy: %.4f" % (np.median(a)))
print("Median using function: %.4f" % (median(a)))
# Variance
print("Variance using numpy: %.4f" % (np.var(a, ddof=1)))
print("Variance using function: %.4f" % (variance(a, ddof=1)))
# Standard Deviation
print("Variance using numpy: %.4f" % (np.std(a, ddof=1)))
print("Variance using function: %.4f" % (standard_deviation(a, ddof=1)))
# Kurtosis
print("Kurtosis using scipy: %.4f" % (sc.stats.kurtosis(a)))
print("Kurtosis using function: %.4f" % (kurtosis(a)))
# Shannon Entropy
print("Shannon Entropy using scipy: %.4f" % (sc.stats.entropy(a, base=2)))
print("Shannon Entropy using function: %.4f" % (shannon_entropy(a)))


'''
Análise da energia do sinal atraves de tal e tal
'''


'''
Função para calcular a entropia do sinal
'''


'''
Funções para calcular a energia e a densidade de energia
'''