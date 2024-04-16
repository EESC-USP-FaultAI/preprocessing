import numpy as np
import pandas as pd


def data_selection(data_file_path, meas, meas_file_path="medicoes.csv", single_phase=None):
    """
    Select the voltage/current data given its name on file "medicoes.csv".
    :param data_file_path: Path to csv with voltage and current data
    :param meas: measurement name based on "medicoes.csv" file.
    :param meas_file_path: Path to csv file "medicoes.csv" in your computer.
    :param single_phase: select the phase (A, B or C) to extract single phase data. If None returns three-phase data (default=None).
    :return: Return voltage/current data as an 1D/2D array. Returns zeros if an error occurred.

    Example:
        >>> data_selection(data_file_path="caso_1_.csv", meas="Vmed_B1", meas_file_path="medicoes.csv", single_phase="A")
        returns Voltage Bus 1 data from "caso_1_.csv" file for single phase "A".
    """
    meas = meas + ":"
    phases = ["A", "B", "C"]  # Correspondent vector for each phase number
    meas_names = pd.read_csv(meas_file_path, header=None)[0].values  # Extracting measurement names from "medicoes.csv" file
    col_indexes = []
    # Dealing with single phase cases
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
        data = pd.read_csv(data_file_path, header=None, usecols=col_indexes)[:].values
    except FileNotFoundError as e:
        print(e)
        data = np.zeros(9216)

    return data


def case_selection(data_folder_path, meas="Vmed_B1", meas_file_path="medicoes.csv", single_phase=None, scenarios_file_path="Cenarios_inic.csv", resistence=None, fault_type=None, angle=None, local=None):
    """
    Select the voltage/current data given the scenario parameters.
    :param data_folder_path: Path to folder with csv files of voltage and current data
    :param meas: measurement name based on "medicoes.csv" file.
    :param meas_file_path: Path to csv file "medicoes.csv" in your computer.
    :param single_phase: select the phase (A, B or C) to extract single phase data. If None returns three-phase data (default=None).
    :param scenarios_file_path: Path to csv file "Cenarios_inic.csv" in your computer
    :param resistence: Desired value of resistence evaluated in the scenario.
    :param fault_type: Desired fault_type evaluated in the scenario.
    :param angle:Desired value of incidence angle evaluated in the scenario.
    :param local:Desired local evaluated in the scenario.
    :return: Return voltage/current data as an 2D/3D array where first dimension is respective for each scenario.
    Returns zeros for each scenario in which an error occurred.
    """
    # Reading file with scenarios information
    scenarios_DF = pd.read_csv(scenarios_file_path, header=None)

    # Extracting parameter values from all scenarios
    resistence_values = scenarios_DF[1].values
    fault_type_values = scenarios_DF[3].values
    angle_values = scenarios_DF[7].values
    local_values = scenarios_DF[9].values

    # Selecting cases with desired parameters
    cases = []
    for i in range(scenarios_DF.shape[0]):
        valid = 1
        if resistence is not None:
            if resistence_values[i] != resistence:
                valid = 0
        if fault_type is not None:
            if fault_type_values[i] != fault_type:
                valid = 0
        if angle is not None:
            if angle_values[i] != angle:
                valid = 0
        if local is not None:
            if local_values[i] != local:
                valid = 0

        if valid:
            cases.append(f"caso_{i+1}_.csv")

    # Obtaining data from each case
    final_data = []
    for case_file in cases:
        meas = meas + ":"
        phases = ["A", "B", "C"]  # Correspondent vector for each phase number
        meas_names = pd.read_csv(meas_file_path, header=None)[
            0].values  # Extracting measurement names from "medicoes.csv" file
        col_indexes = []
        # Dealing with single phase cases
        if single_phase is None:
            for i in range(len(meas_names)):
                if meas in meas_names[i]:
                    col_indexes.append(i)
        else:
            phase_num = phases.index(single_phase) + 1
            for i in range(len(meas_names)):
                if meas + str(phase_num) in meas_names[i]:
                    col_indexes.append(i)
        try:
            data = pd.read_csv(data_folder_path + case_file, header=None, usecols=col_indexes)[:].values
        except FileNotFoundError as e:
            print(e)
            data = np.zeros(9216)
        final_data.append(data)

    final_data = np.array(final_data)

    return final_data
