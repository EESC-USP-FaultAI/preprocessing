import pandas as pd
import numpy as np
from scipy.signal import hilbert
from PyEMD import EMD

def process_signals(file_path_1, file_path_2, fault_time, max_imf=10):
    """
    Function to process the voltage signals from two CSV files.
    Input:
        file_path_1 - path to the first CSV file
        file_path_2 - path to the second CSV file
        fault_time - time at which the fault occurs
        max_imf - maximum number of IMFs to be extracted by the EMD
    """
    def calculate_energy(signal):
        """
        Function to calculate the energy of a signal.
        Input:
            signal - array with the signal values
        Output:
            E - energy of the signal
        """
        return np.sum(signal ** 2)

    def process_signal(file_path):
        """
        Inner function to process the voltage signal from a CSV file.
        Input:
            file_path - path to the CSV file
        Output:
            energy, standard deviation of amplitude, standard deviation of phase
        """
        # Read data from the CSV file
        signals = pd.read_csv(file_path)

        # Get the values of the necessary columns
        time = signals.iloc[3:, 0].values
        fault_position = np.where(time == fault_time)[0][0]

        Va = signals.iloc[3:, 1].values
        Vb = signals.iloc[3:, 2].values
        Vc = signals.iloc[3:, 3].values

        # Select the range of interest
        Va = Va[fault_position-64:fault_position+63]
        Vb = Vb[fault_position-64:fault_position+63]
        Vc = Vc[fault_position-64:fault_position+63]

        # Perform EMD on the Va signal
        emd = EMD()
        imf1 = emd.emd(Va, max_imf=max_imf)

        # Calculate the energy, standard deviation, and phase of the first IMF
        energy = calculate_energy(imf1[:, 0])
        std_dev = np.std(np.abs(imf1[:, 0]))
        phase = np.angle(hilbert(imf1[:, 0]))
        phase_std_dev = np.std(phase)

        return energy, std_dev, phase_std_dev

    # Process the first signal
    energy_1, std_dev_1, phase_std_dev_1 = process_signal(file_path_1)
    print(f'Configuration 1 - Energy: {energy_1}, Standard Deviation: {std_dev_1}, Phase Standard Deviation: {phase_std_dev_1}')

    # Process the second signal
    energy_2, std_dev_2, phase_std_dev_2 = process_signal(file_path_2)
    print(f'Configuration 2 - Energy: {energy_2}, Standard Deviation: {std_dev_2}, Phase Standard Deviation: {phase_std_dev_2}')

# Examples of using the function
file_path_1 = 'E:/Doutorado/P&D - FaultAIFinder/P&D - Processamento/preprocessing/dados_testes/configuracao_1/tensao/dados_tensao_config_1.csv'
file_path_2 = 'E:/Doutorado/P&D - FaultAIFinder/P&D - Processamento/preprocessing/dados_testes/configuracao_2/tensao/dados_tensao_config_2.csv'
fault_time = 0.103821620000000

process_signals(file_path_1, file_path_2, fault_time)


