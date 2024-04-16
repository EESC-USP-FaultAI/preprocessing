from matplotlib import pyplot as plt

from functions.TW.DTW import DWT
#from functions.ProcessamentoCSV.Dunno import data_selection
import numpy as np
import pandas as pd

def data_selection(file_path, file_meas, meas, single_phase=None):
    """
    Select the voltage/current data given its name on file "medicoes.csv".
    :param file_path: Path to csv with voltage and current data
    :param meas: measurement name based on "medicoes.csv" file.
    :param single_phase: select the phase (A, B or C) to extract single phase data. If None
    returns three-phase data (default=None).
    :return: Return voltage/current data as an 1D/2D array. Returns zeros if an error occurred.
    """
    meas = meas + ":"
    phases = ["A", "B", "C"]
    meas_names = pd.read_csv(file_meas, header=None)[0].values
    col_indexes = []
    if single_phase is None:
        for i in range(len(meas_names)):
            if meas in meas_names[i]:
                col_indexes.append(i)
    else:
        phase_num = phases.index(single_phase) + 1
        for i in range(len(meas_names)):
            if meas+str(phase_num) in meas_names[i]:
                col_indexes.append(i)
    try:
        data = pd.read_csv(file_path, header=None, usecols=col_indexes)[:].values
    except FileNotFoundError as e:
        print(e)
        data = np.zeros(9216)

    return data


data = data_selection('Z:\\modelo_simulacoes\\results_Modelo_Aero_INTEGRADO_LOOP_v5\\resultados\\caso_100_.csv',
                      'Z:\\modelo_simulacoes\\medicoes.csv',
                      'Vmed_B1', 'A')
signal_values = data[:,0]

# Criar uma instância da classe Wavelet
wavelet_instance = DWT()

ca, cd = wavelet_instance.transform(signal_values, 'db4')

# Generate time arrays for the signal and its DWT
signal_time = np.linspace(0, 0.3, len(signal_values))
cd_time = np.linspace(0, 0.3, len(cd))

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
