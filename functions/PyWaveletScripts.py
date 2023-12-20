import comtrade
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pywt


def see_functions():
    print("1 - wavelet_viewer")
    print("2 - evaluate_dwt_single_signal")
    print("3 - dwt_from_csv")
    print("4 - daubechies_wavelet_transform")


def list_wavelets():
    print("Available Wavelet functions:")
    for wave_name in pywt.wavelist():
        print(wave_name)


def list_discrete_wavelets():
    print("Discrete Wavelets Available:")
    for wave_name in pywt.wavelist():
        try:
            pywt.Wavelet(wave_name)
            print(wave_name)
        except:
            pass


def list_continuous_wavelets():
    print("Continuous Wavelets Available:")
    for wave_name in pywt.wavelist():
        try:
            pywt.Wavelet(wave_name)
        except:
            print(wave_name)


def wavelet_viewer(wave_name):
    wave = pywt.Wavelet(wave_name)

    """Wavelet Properties"""
    print(wave)

    """Wavelet Functions"""
    phi, psi, x = wave.wavefun(level=4)

    plt.title(f"{wave_name} Wavelet Phi (Scaling) Function", color="blue")
    plt.plot(x, phi, color="blue")
    plt.show()

    plt.title(f"{wave_name} Wavelet Psi (Wave) Function", color="red")
    plt.plot(x, psi, color="red")
    plt.show()


def evaluate_dwt_single_phase(data, wavelet_name, mode="symmetric", axis=-1):
    cA, cD = pywt.dwt(data, mode=mode, wavelet=wavelet_name, axis=axis)
    t = np.linspace(0, 0.4, len(data))
    plt.figure(figsize=(30, 20))

    plt.subplot(3, 1, 1)
    plt.plot(t, data, color='black')
    plt.xlabel("Time")
    plt.ylabel("Data")
    plt.title("Original Signal", fontsize=20)

    plt.subplot(3, 1, 2)
    plt.plot(cA, color="red")
    plt.xlabel("Samples")
    plt.ylabel("cA")
    plt.title("Approximation Coefficients", fontsize=20)

    plt.subplot(3, 1, 3)
    plt.plot(cD, color="green")
    plt.xlabel("Samples")
    plt.ylabel("cD")
    plt.title("Detail Coefficients", fontsize=20)

    return cA, cD


def dwt_from_signal_generator(signal_data, wavelet_name, level=1, save_to_csv=True):

    """
    :param signal_data: Three-phase signal to apply Discrete Wavelet Transform.
    :param wavelet_name: Name of mother wavelet to effectuate DWT.
    :param level: Level of multi-level decomposition of DWT, default=1 to single level decomposition.
    :param save_to_csv: Save the wavelet coefficients in a csv file. default=True.
    :return: wavelet_dataframe: DataFrame with wavelet coefficients for each phase signal.
    """

    """Apply dwt in each phase of the signal"""
    phaseA_cA, phaseA_cD = pywt.wavedec(signal_data["A"], wavelet=wavelet_name, level=level)[:2]
    phaseB_cA, phaseB_cD = pywt.wavedec(signal_data["B"], wavelet=wavelet_name, level=level)[:2]
    phaseC_cA, phaseC_cD = pywt.wavedec(signal_data["C"], wavelet=wavelet_name, level=level)[:2]

    """Constructing DataFrame with Wavelet Coefficients"""
    wavelet_dataframe = pd.DataFrame()
    wavelet_dataframe["phaseA_cA"] = phaseA_cA
    wavelet_dataframe["phaseA_cD"] = phaseA_cD
    wavelet_dataframe["phaseB_cA"] = phaseB_cA
    wavelet_dataframe["phaseB_cD"] = phaseB_cD
    wavelet_dataframe["phaseC_cA"] = phaseC_cA
    wavelet_dataframe["phaseC_cD"] = phaseC_cD

    """Saving DataFrame in csv if wanted"""
    if save_to_csv:
        save = wavelet_dataframe.to_csv("wavelet_coefficients.csv", mode='x')
        if save is None:
            print("ERROR: Couldn't save the csv file, it probably already exists, verify that.")

    return wavelet_dataframe


def dwt_from_csv(csv_path, wavelet_name, level=1):
    df = pd.read_csv(csv_path)

    "Voltage and Current signals"
    Va = df["Va"]
    Vb = df["Vb"]
    Vc = df["Vc"]
    Ia = df["Ia"]
    Ib = df["Ib"]
    Ic = df["Ic"]

    Va_cA, Va_cD = pywt.wavedec(Va, wavelet=wavelet_name, level=level)[:2]
    Vb_cA, Vb_cD = pywt.wavedec(Vb, wavelet=wavelet_name, level=level)[:2]
    Vc_cA, Vc_cD = pywt.wavedec(Vc, wavelet=wavelet_name, level=level)[:2]
    Ia_cA, Ia_cD = pywt.wavedec(Ia, wavelet=wavelet_name, level=level)[:2]
    Ib_cA, Ib_cD = pywt.wavedec(Ib, wavelet=wavelet_name, level=level)[:2]
    Ic_cA, Ic_cD = pywt.wavedec(Ic, wavelet=wavelet_name, level=level)[:2]

    """Constructing DataFrame with Wavelet Coefficients"""
    wavelet_dataframe = pd.DataFrame()
    wavelet_dataframe["Va_cA"] = Va_cA
    wavelet_dataframe["Vb_cA"] = Vb_cA
    wavelet_dataframe["Vc_cA"] = Vc_cA
    wavelet_dataframe["Ia_cA"] = Ia_cA
    wavelet_dataframe["Ib_cA"] = Ib_cA
    wavelet_dataframe["Ic_cA"] = Ic_cA
    wavelet_dataframe["Va_cD"] = Va_cD
    wavelet_dataframe["Vb_cD"] = Vb_cD
    wavelet_dataframe["Vc_cD"] = Vc_cD
    wavelet_dataframe["Ia_cD"] = Ia_cD
    wavelet_dataframe["Ib_cD"] = Ib_cD
    wavelet_dataframe["Ic_cD"] = Ic_cD

    """Saving DataFrame in csv"""
    save = wavelet_dataframe.to_csv(f"wavelet_coefficients.csv", mode='x')
    if save is None:
        print("ERROR: Couldn't save the csv file, it probably already exists, verify that.")

    return wavelet_dataframe


def daubechies_wavelet_transform(db_name, cfg_file, dat_file, file_path, level=1):
    rec = comtrade.load(cfg_file, dat_file)  # Loading dataset with Comtrade

    dfCom = rec.to_dataframe()  # Converting dataset into DataFrame

    """Voltage and Current on Local Terminal"""
    Va_loc = dfCom["Vloca: Vloca"]
    Vb_loc = dfCom["Vlocb: Vlocb"]
    Vc_loc = dfCom["Vlocc: Vlocc"]
    Ia_loc = dfCom["Iloca: Iloca"]
    Ib_loc = dfCom["Ilocb: Ilocb"]
    Ic_loc = dfCom["Ilocc: Ilocc"]

    """Voltage and Current on Remote Terminal"""
    Va_rem = dfCom["Vrema: Vrema"]
    Vb_rem = dfCom["Vremb: Vremb"]
    Vc_rem = dfCom["Vremc: Vremc"]
    Ia_rem = dfCom["Irema: Irema"]
    Ib_rem = dfCom["Iremb: Iremb"]
    Ic_rem = dfCom["Iremc: Iremc"]

    # mid = len(Va_rem) / 2  # Middle Index for data split

    """Applying Wavelet Transform with Daubechies"""
    if level <= 0:
        print("You put a negative value as the level of the transform, setting the value to default: 1")
        level = 1
    Va_loc_cA, Va_loc_cD = pywt.wavedec(Va_loc, wavelet=db_name, level=level)[:2]
    Vb_loc_cA, Vb_loc_cD = pywt.wavedec(Vb_loc, wavelet=db_name, level=level)[:2]
    Vc_loc_cA, Vc_loc_cD = pywt.wavedec(Vc_loc, wavelet=db_name, level=level)[:2]
    Ia_loc_cA, Ia_loc_cD = pywt.wavedec(Ia_loc, wavelet=db_name, level=level)[:2]
    Ib_loc_cA, Ib_loc_cD = pywt.wavedec(Ib_loc, wavelet=db_name, level=level)[:2]
    Ic_loc_cA, Ic_loc_cD = pywt.wavedec(Ic_loc, wavelet=db_name, level=level)[:2]
    Va_rem_cA, Va_rem_cD = pywt.wavedec(Va_rem, wavelet=db_name, level=level)[:2]
    Vb_rem_cA, Vb_rem_cD = pywt.wavedec(Vb_rem, wavelet=db_name, level=level)[:2]
    Vc_rem_cA, Vc_rem_cD = pywt.wavedec(Vc_rem, wavelet=db_name, level=level)[:2]
    Ia_rem_cA, Ia_rem_cD = pywt.wavedec(Ia_rem, wavelet=db_name, level=level)[:2]
    Ib_rem_cA, Ib_rem_cD = pywt.wavedec(Ib_rem, wavelet=db_name, level=level)[:2]
    Ic_rem_cA, Ic_rem_cD = pywt.wavedec(Ic_rem, wavelet=db_name, level=level)[:2]

    """Constructing DataFrame with Wavelet Coefficients"""
    wavelet_dataframe = pd.DataFrame()
    wavelet_dataframe["Va_loc_cA"] = Va_loc_cA
    wavelet_dataframe["Vb_loc_cA"] = Vb_loc_cA
    wavelet_dataframe["Vc_loc_cA"] = Vc_loc_cA
    wavelet_dataframe["Ia_loc_cA"] = Ia_loc_cA
    wavelet_dataframe["Ib_loc_cA"] = Ib_loc_cA
    wavelet_dataframe["Ic_loc_cA"] = Ic_loc_cA
    wavelet_dataframe["Va_loc_cD"] = Va_loc_cD
    wavelet_dataframe["Vb_loc_cD"] = Vb_loc_cD
    wavelet_dataframe["Vc_loc_cD"] = Vc_loc_cD
    wavelet_dataframe["Ia_loc_cD"] = Ia_loc_cD
    wavelet_dataframe["Ib_loc_cD"] = Ib_loc_cD
    wavelet_dataframe["Ic_loc_cD"] = Ic_loc_cD
    wavelet_dataframe["Va_rem_cA"] = Va_rem_cA
    wavelet_dataframe["Vb_rem_cA"] = Vb_rem_cA
    wavelet_dataframe["Vc_rem_cA"] = Vc_rem_cA
    wavelet_dataframe["Ia_rem_cA"] = Ia_rem_cA
    wavelet_dataframe["Ib_rem_cA"] = Ib_rem_cA
    wavelet_dataframe["Ic_rem_cA"] = Ic_rem_cD
    wavelet_dataframe["Va_rem_cD"] = Va_rem_cD
    wavelet_dataframe["Vb_rem_cD"] = Vb_rem_cD
    wavelet_dataframe["Vc_rem_cD"] = Vc_rem_cD
    wavelet_dataframe["Ia_rem_cD"] = Ia_rem_cD
    wavelet_dataframe["Ib_rem_cD"] = Ib_rem_cD
    wavelet_dataframe["Ic_rem_cD"] = Ic_rem_cD

    """Saving DataFrame in csv"""
    save = wavelet_dataframe.to_csv(f"{file_path}_wavelet_coefficients.csv", mode='x')
    if save is None:
        print("ERROR: Couldn't save the csv file, it probably already exists, verify that.")

    return wavelet_dataframe


def wt_coefficients_metrics(wave_coefficients_df, folder_name):
    return
