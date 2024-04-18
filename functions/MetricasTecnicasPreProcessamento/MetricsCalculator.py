import numpy as np
import scipy as sc  # Used for testing


def mean(coef):
    """
    Calculate the mean value of wavelet coefficients.

    Parameters:
    coef (array-like): Coefficients obtained with Wavelet Transform.

    Returns:
    float: Mean value of given wavelet coefficients.
    """
    data_sum = sum(coef)
    data_length = len(coef)
    coef_mean = data_sum / data_length
    return coef_mean


def median(coef):
    """
    Calculate the median value of wavelet coefficients.

    Parameters:
    coef (array-like): Coefficients obtained with Wavelet Transform.

    Returns:
    float: Median value of given wavelet coefficients.
    """
    sorted_coef = sorted(coef)
    data_length = len(coef)
    n_mean = data_length // 2
    if data_length % 2 == 0:  # Even number of values
        coef_median = (sorted_coef[n_mean] + sorted_coef[n_mean - 1]) / 2
    else:  # Odd number of values
        coef_median = sorted_coef[n_mean]
    return coef_median


def variance(coef, ddof=0):
    """
    Calculate the variance of wavelet coefficients.

    Parameters:
    coef (array-like): Coefficients obtained with Wavelet Transform.
    ddof (int, optional): Delta Degrees of Freedom. The divisor used in the calculation
    is N - ddof, where N represents the number of elements. By default ddof is zero.

    Returns:
    float: Variance value of given wavelet coefficients.
    """
    mean_value = mean(coef)
    data_length = len(coef)
    square_diff_sum = sum((x - mean_value) ** 2 for x in coef)
    coef_variance = square_diff_sum / (data_length - ddof)
    return coef_variance


def standard_deviation(coef, ddof=0):
    """
    Calculate the standard deviation of wavelet coefficients.

    Parameters:
    coef (array-like): Coefficients obtained with Wavelet Transform.
    ddof (int, optional): Delta Degrees of Freedom. The divisor used in the calculation
    is N - ddof, where N represents the number of elements. By default ddof is zero.

    Returns:
    float: Standard deviation value of given wavelet coefficients.
    """
    variance_value = variance(coef, ddof=ddof)
    coef_std_dev = np.sqrt(variance_value)
    return coef_std_dev


def kurtosis(coef, fisher=True):  # Fisher's Kurtosis
    """
    Calculate the kurtosis (Fisher or Pearson) of wavelet coefficients.

    Parameters:
    coef (array-like): Coefficients obtained with Wavelet Transform.
    fisher (bool, optional): If True, subtract 3.0 from the result to give 0.0 for a normal distribution (default=True).

    Returns:
    float: Kurtosis value of given wavelet coefficients.
    """
    mean_value = mean(coef)
    variance_value = variance(coef)
    data_length = len(coef)
    forth_diff_sum = sum((x - mean_value) ** 4 for x in coef)
    forth_moment_value = forth_diff_sum / data_length
    if fisher:
        coef_kurtosis = (forth_moment_value / (variance_value ** 2)) - 3.0
    else:
        coef_kurtosis = forth_moment_value / (variance_value ** 2)
    return coef_kurtosis


def shannon_entropy(coef, base=None):
    """
    Calculate the Shannon Entropy of wavelet coefficients.

    Parameters:
    coef (array-like): Coefficients obtained with Wavelet Transform.
    base (float, optional): The logarithmic base to use, defaults to e (natural logarithm).

    Returns:
    float: Shannon Entropy value of given wavelet coefficients.
    """
    data_sum = sum(abs(x) for x in coef)
    pmf = [abs(x) / data_sum for x in coef]
    data_log_sum = sum(pk * np.log(pk) for pk in pmf if pk != 0)
    coef_shannon_entropy = -data_log_sum
    if base is not None:
        coef_shannon_entropy /= np.log(base)
    return coef_shannon_entropy


"""Energy of signal"""


def energy_sum_of_squares(coef):
    """
    Calculates the energy of a signal using the sum of squares method.

    Parameters:
    coef (array-like): Coefficients representing the signal.

    Returns:
    float: Energy of the signal.
    """
    energy = sum(abs(c) ** 2 for c in coef)
    return energy


def energy_parseval(coef):
    """
    Calculates the energy of a signal using Parseval's theorem.

    Parameters:
    coef (array-like): Coefficients representing the signal.

    Returns:
    float: Energy of the signal.
    """
    energy = energy_sum_of_squares(coef)
    return energy / len(coef)


def energy_mean_power(coef):
    """
    Calculates the energy of a signal using the mean power method.

    Parameters:
    coef (array-like): Coefficients representing the signal.

    Returns:
    float: Energy of the signal.
    """
    energy = energy_sum_of_squares(coef)
    return energy / len(coef)


def energy_autocorrelation(coef):
    """
    Calculates the energy of a signal using the autocorrelation method.

    Parameters:
    coef (array-like): Coefficients representing the signal.

    Returns:
    float: Energy of the signal.
    """
    autocorr = np.correlate(coef, coef, mode='full')
    energy = sum(abs(ac) for ac in autocorr)
    return energy


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
print("Shannon Entropy using function: %.4f" % (shannon_entropy(a, base=2)))