import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pywt
import os

def see_functions():
    """
    Lists available functions in this file

    Returns
    -------
        prints the list of functions present in this files
    
    Examples
    --------
    >>> see_functions()
    """

    print("1 - wavelet_viewer")
    print("2 - evaluate_dwt_single_signal")
    print("3 - dwt_from_csv")
    print("4 - daubechies_wavelet_transform")

def list_wavelets():
    """
    Lists available wavelets functions

    Returns
    -------
        prints the available wavelet functions

    Examples
    --------
    >>> list_wavelets()
    """
    print("Wavelets Available:")
    for wave_name in pywt.wavelist():
        print(wave_name)

def list_discrete_wavelets():
    """
    Lists available discrete wavelets functions


    Returns
    -------
        prints the available discrete wavelet functions
    
    Examples
    --------
    >>> list_discrete_wavelets()
    """
    print("Discrete Wavelets Available:")
    for wave_name in pywt.wavelist():
        try:
            pywt.Wavelet(wave_name)
            print(wave_name)
        except:
            pass

def list_continuous_wavelets():
    """
    Lists available continuous wavelets functions

    Returns
    -------
        prints the available continuous wavelet functions
    
    Examples
    --------
    >>> list_continuous_wavelets()
    """
    print("Continuous Wavelets Available:")
    for wave_name in pywt.wavelist():
        try:
            pywt.Wavelet(wave_name)
        except:
            print(wave_name)

def wavelet_viewer(wave_name):
    """
    Plot wavelets function for a given wavelet function

    Parameters
    ----------
    wave_name : str
        name of wavelet function

    Returns
    -------
        plot the wavelet function [CA and CD]

    Examples
    --------
    >>> wavelet_viewer("db2")
    """
    if not isinstance(wave_name, str): raise ValueError("wave_name must be a string")

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
    """
    Evaluate Discrete Wavelet Transform using PYWT package.

    Parameters
    ----------
    data : array-like
        single-phase signal to perform transform
    wavelet_name : str
        name of mother wavelet
    mode : str, optional
        mode of signal extension (default="symmetric")
    axis : int, optional
        axis to perform transform (default=-1)

    Returns
    -------
    CA, CD : array-like
        Approximation and Detail coefficients

    Examples
    --------
    >>> import functions.TW as TW
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> y = np.sin(2*np.pi*60*np.linspace(0, 20/60, 1000))
    >>> y[len(y)//2:] *= 2
    >>> coefs = TW.TW_PYWT.evaluate_dwt_single_phase(y, 'db4')
    >>> plt.subplot(2, 1, 1)
    >>> plt.plot(coefs[0])
    >>> plt.title('Approximation')
    >>> plt.subplot(2, 1, 2)
    >>> plt.plot(coefs[1])
    >>> plt.title('Detail')
    """

    if not isinstance(data, np.ndarray, list, tuple): raise ValueError("data must be a array-like")
    if not isinstance(wavelet_name, str): raise ValueError("wavelet_name must be a string")

    cA, cD = pywt.dwt(data, mode=mode, wavelet=wavelet_name, axis=axis)

    return cA, cD

def evaluate_dwt_manually_single_phase(data, wavelet_name):
    """
    Evaluate Discrete Wavelet Transform using scientifc package NumPy for convolution.

    Parameters
    ----------
    data : array-like
        single-phase signal to perform transform
    wavelet_name : str
        name of mother wavelet

    Returns
    -------
    CA, CD : array-like
        Approximation and Detail coefficients

    Examples
    --------
    >>> import functions.TW as TW
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> y = np.sin(2*np.pi*60*np.linspace(0, 20/60, 1000))
    >>> y[len(y)//2:] *= 2
    >>> coefs = TW.TW_PYWT.evaluate_dwt_manually_single_phase(y, 'db4')
    >>> plt.subplot(2, 1, 1)
    >>> plt.plot(coefs[0])
    >>> plt.title('Approximation')
    >>> plt.subplot(2, 1, 2)
    >>> plt.plot(coefs[1])
    >>> plt.title('Detail')
    """

    wavelet = pywt.Wavelet(wavelet_name)
    dec_low = wavelet.dec_lo
    dec_high = wavelet.dec_hi
    cA = []
    cD = []

    cA_aux = np.convolve(data, dec_low)
    cD_aux = np.convolve(data, dec_high)

    for i in range(len(cA_aux)):
        if i % 2 == 1:
            cA.append(cA_aux[i])
            cD.append(cD_aux[i])
    cA = np.array(cA)
    cD = np.array(cD)

    return cA, cD

def dwt_from_signal_generator(signal_data, wavelet_name, level=1, save_to_csv=True):
    """
    Evaluate Discrete Wavelet Transform using scientifc package NumPy for convolution.

    Parameters
    ----------
    signal_data : dict
        dictionary with three-phase signal to perform transform
    wavelet_name : str
        name of mother wavelet
    level : int, optional
        level of decomposition (default=1)
    save_to_csv : bool, optional
        save the wavelet coefficients in a csv file (default=True)

    Returns
    -------
    wavelet_dataframe : DataFrame
        DataFrame with wavelet coefficients for each phase signal
    
    Examples
    --------
    >>> import functions.TW as TW
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> signal_data = {
    ...     "A": np.sin(2*np.pi*60*np.linspace(0, 20/60, 1000)),
    ...     "B": np.sin(2*np.pi*60*np.linspace(0, 20/60, 1000)),
    ...     "C": np.sin(2*np.pi*60*np.linspace(0, 20/60, 1000))
    ... }
    >>> wavelet_dataframe = TW.TW_PYWT.dwt_from_signal_generator(signal_data, 'db4')
    >>> plt.subplot(2, 1, 1)
    >>> plt.plot(wavelet_dataframe["phaseA_cA"])
    >>> plt.title('Approximation')
    >>> plt.subplot(2, 1, 2)
    >>> plt.plot(wavelet_dataframe["phaseA_cD"])
    >>> plt.title('Detail')
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
        if os.path.exists("wavelet_coefficients.csv"):
            print("ERROR: Couldn't save the csv file, it probably already exists, verify that.")
        else:
            wavelet_dataframe.to_csv("wavelet_coefficients.csv", mode='w')
            

    return wavelet_dataframe

def dwt_from_csv(csv_path, wavelet_name, level=1):
    """
    Function to evaluate Discrete Wavelet Transform on a dataset in csv file format.

    Parameters
    ----------
    csv_path : str
        path to dataset csv file with three-phase signals, with tension and current data, on your computer
    wavelet_name : str
        name of mother wavelet
    level : int, optional
        level of decomposition (default=1)

    Returns
    -------
    wavelet_dataframe : DataFrame
        DataFrame with wavelet coefficients of the dataset

    Examples
    --------
    >>> import functions.TW as TW
    >>> wavelet_dataframe = TW.TW_PYWT.dwt_from_csv("dataset.csv", 'db4')
    """

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



