from matplotlib import pyplot as plt
from functions.TW.DTW import DWT
from functions.ProcessamentoCSV.Dunno import data_selection
import numpy as np

# Select data from CSV files
data = data_selection('Z:\\modelo_simulacoes\\results_Modelo_Aero_INTEGRADO_LOOP_v5\\resultados\\caso_1_.csv',
                      'Vmed_B1',
                      'Z:\\modelo_simulacoes\\medicoes.csv',
                      'A')


def applyDWTSignal(signal, dwt, time=0.3, plot=False):
    """
    Apply Discrete Wavelet Transform to a signal and optionally plot the result.

    Parameters:
        signal (array_like): The input signal.
        dwt (str): The type of wavelet to use for the transformation.
        time (float): Duration time of signal
        plot (bool, optional): Whether to plot the original signal and its DWT. Defaults to False.

    Returns:
        tuple: A tuple containing the approximation coefficients (ca) and detail coefficients (cd).
    """

    signal_values = signal

    # Create an instance of the Wavelet class
    wavelet_instance = DWT()

    # Perform DWT on the signal
    ca, cd = wavelet_instance.transform(signal_values, dwt)

    if plot:
        # Generate time arrays for the signal and its DWT
        signal_time = np.linspace(0, time, len(signal_values))
        cd_time = np.linspace(0, time, len(cd))

        # Create subplots for each aspect of the analysis
        fig, axs = plt.subplots(2)

        # Adjust subplot layout
        plt.subplots_adjust(left=0.22)
        plt.subplots_adjust(hspace=1.0)

        # Plot the original signal
        axs[0].plot(signal_time, signal_values)
        axs[0].set_title('Signal')
        axs[0].set_xlabel('Time [s]')
        axs[0].set_ylabel('Amplitude [pu]')

        # Plot the DWT
        axs[1].plot(cd_time, cd)
        axs[1].set_title('DWT')
        axs[1].set_xlabel('Time [s]')
        axs[1].set_ylabel('Amplitude [pu]')

        plt.show()

    return ca, cd


# Example usage
approximation_coefficients, detail_coefficients = applyDWTSignal(data[:, 0], 'db4', 0.3, True)
