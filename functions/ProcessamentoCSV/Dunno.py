import numpy as np
import pandas as pd


def data_selection_mod_Alailton(file_path, meas, single_phase=None):
    """
    Select the voltage/current data given its name on file "medicoes.csv".
    :param file_path: Path to csv with voltage and current data
    :param meas: measurement name based on "medicoes.csv" file.
    :param single_phase: select the phase (A, B or C) to extract single phase data. If None
    returns three-phase data (default=None).
    :return: Return voltage/current data as an 1D/2D array. Returns zeros if an error occurred.
    """

    # O arquivo "medicoes.csv" é local e não está no mesmo diretório que o arquivo que chama a função
    import os
    curDir = os.path.dirname(__file__) # Pega o diretório do arquivo atual "Dunno.py"
    medicoesPath = os.path.join(curDir, "medicoes.csv") # Junta o diretório atual com o nome do arquivo "medicoes.csv"

    meas = meas + ":"
    phases = ["A", "B", "C"]
    meas_names = pd.read_csv(medicoesPath, header=None)[0].values
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

def data_selection(file_path, meas, single_phase=None):
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
    meas_names = pd.read_csv("medicoes.csv", header=None)[0].values
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

