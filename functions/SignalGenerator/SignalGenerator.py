import numpy as np


def voltage_sag_short_circuit(s:float, t1:float, t2:float, duration:float, fs:int, phases:str, add_noise=False, SNR=None):
    """
    Generate three-phase voltage sag caused by a short circuit.

    parameters
    ----------
    s : float
        Sag magnitude in per unit (pu).
    t1 : float
        Start time of the voltage sag in seconds.
    t2 : float
        End time of the voltage sag in seconds.
    duration : float
        Total duration of the simulation in seconds.
    fs : int
        Sampling frequency in Hertz.
    phases : str
        String indicating the involved phases ('A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC', etc.).
    add_noise : bool
        Boolean flag indicating whether to add noise to the signal.
    SNR : float
        Desired signal-to-noise ratio in decibels.

    returns
    -------
    voltage_sag : dict
        Dictionary containing three-phase voltage signals during the specified duration.

    Examples
    --------
    >>> import functions.SignalGenerator as sg
    >>> import matplotlib.pyplot as plt
    >>> V = sg.voltage_sag_short_circuit(0.5, 0.1, 0.2, 1, 10000, 'ABC', add_noise=False, SNR=20)
    >>> plt.plot(V['A'])
    """
    # Validate input parameters
    if not isinstance(s, (float, int)): raise TypeError('s must be a number')
    if not isinstance(t1, (float, int)): raise TypeError('t1 must be a number')
    if not isinstance(t2, (float, int)): raise TypeError('t2 must be a number')
    if not isinstance(duration, (float, int)): raise TypeError('duration must be a number')
    if not isinstance(fs, (float, int)): raise TypeError('fs must be an number')
    if not isinstance(phases, str): raise TypeError('phases must be a string')
    if not isinstance(add_noise, bool): raise TypeError('add_noise must be a boolean')
    if not isinstance(SNR, (float, int, type(None))): raise TypeError('SNR must be a float or None')
    if not t1 < t2: raise ValueError('t1 must be less than t2')
    if not (0 <= t1 < duration): raise ValueError('t1 must be between 0 and duration')
    if not (0 <= t2 < duration): raise ValueError('t2 must be between 0 and duration')
    if not (0 < s < 1): raise ValueError('s must be between 0 and 1')
    if not (fs > 0): raise ValueError('fs must be greater than 0')
    if not all([phase in ['A', 'B', 'C'] for phase in phases]): raise ValueError('phases must be a combination of A, B, and C')
    if SNR is not None and not (SNR > 0): raise ValueError('SNR must be greater than 0')
    if not (duration > 0): raise ValueError('duration must be greater than 0')
    if add_noise and SNR is None: raise ValueError('SNR must be specified when add_noise is True')
    
    # Generate time vector
    t = np.arange(0, duration, 1 / fs)

    # Step functions for start and end time
    u1 = np.heaviside(t - t1, 1)
    u2 = np.heaviside(t - t2, 1)

    # Voltage sag model equation (2)
    Vsag_A = (1 - s * (u1 - u2)) * np.sin(2 * np.pi * 60 * t)
    Vsag_B = (1 - s * (u1 - u2)) * np.sin(2 * np.pi * 60 * t - 2 * np.pi / 3)
    Vsag_C = (1 - s * (u1 - u2)) * np.sin(2 * np.pi * 60 * t + 2 * np.pi / 3)

    # Initialize all phases to their respective sine waves
    voltage_sag = {'A': np.sin(2 * np.pi * 60 * t),
                    'B': np.sin(2 * np.pi * 60 * t - 2 * np.pi / 3),
                    'C': np.sin(2 * np.pi * 60 * t + 2 * np.pi / 3)}

    # Set the voltage values for involved phases during the fault
    if 'A' in phases:
        voltage_sag['A'] = Vsag_A
    if 'B' in phases:
        voltage_sag['B'] = Vsag_B
    if 'C' in phases:
        voltage_sag['C'] = Vsag_C

    # Add noise if specified
    if add_noise:
        for phase in voltage_sag:
            voltage_sag[phase] = adicionar_ruido(voltage_sag[phase], SNR)

    return voltage_sag

def GenerateSignalWithHarmonics(amplitude_fundamental, samples_per_cycle, frequency, harmonics, amplitudes,
                                duration, harmonics_start_time, add_noise=False, SNR=None):
    """
    Generate a composite signal with fundamental and harmonic components.

    Parameters
    ----------
    amplitude_fundamental : float
        The amplitude of the fundamental sinusoidal waveform.
    samples_per_cycle : int
        The number of samples per cycle of the fundamental waveform.
    frequency : float
        The frequency of the fundamental waveform in hertz.
    harmonics : list[int]
        A list of integers representing the harmonics to be added to the fundamental waveform.
    amplitudes : list[float]
        A list of amplitudes corresponding to each harmonic in the harmonics list.
    duration : float
        The total duration of the generated signal in seconds.
    harmonics_start_time : float
        The time at which to start adding harmonics (if greater than 0).
    add_noise : bool
        Boolean flag indicating whether to add noise to the signal.
    SNR : float
        Desired signal-to-noise ratio in decibels.

    Returns
    -------
    time : numpy.ndarray
        An array representing the time vector for the generated signal.
    signal : numpy.ndarray
        An array representing the generated composite signal.

    Examples
    --------
    >>> import functions.SignalGenerator as sg
    >>> import matplotlib.pyplot as plt
    >>> time, signal = sg.GenerateSignalWithHarmonics(1, 256, 60, [3, 5], [0.2, 0.1], 1, 0.5, add_noise=False, SNR=20)
    >>> plt.plot(time, signal)
    """

    # Validate input parameters
    if not (isinstance(amplitude_fundamental, (float, int))): raise TypeError('amplitude_fundamental must be a number')
    if not (isinstance(samples_per_cycle, int)): raise TypeError('samples_per_cycle must be an integer')
    if not (isinstance(frequency, (float, int))): raise TypeError('frequency must be a number')
    if not (isinstance(harmonics, list)): raise TypeError('harmonics must be a list')
    if not (isinstance(amplitudes, list)): raise TypeError('amplitudes must be a list')
    if not (isinstance(duration, (float, int))): raise TypeError('duration must be a number')
    if not (isinstance(harmonics_start_time, (float, int))): raise TypeError('harmonics_start_time must be a number')
    if not (isinstance(add_noise, bool)): raise TypeError('add_noise must be a boolean')
    if not (isinstance(SNR, (float, int, type(None)))): raise TypeError('SNR must be a float or None')
    if not (amplitude_fundamental > 0): raise ValueError('amplitude_fundamental must be greater than 0')
    if not (samples_per_cycle > 0): raise ValueError('samples_per_cycle must be greater than 0')
    if not (frequency > 0): raise ValueError('frequency must be greater than 0')
    if not all([harmonic > 0 for harmonic in harmonics]): raise ValueError('harmonics must be greater than 0')
    if not all([amplitude > 0 for amplitude in amplitudes]): raise ValueError('amplitudes must be greater than 0')
    if not (duration > 0): raise ValueError('duration must be greater than 0')
    if not (harmonics_start_time <= duration): raise ValueError('harmonics_start_time must be greater than 0 and less than or equal to duration')
    if add_noise and SNR is None: raise ValueError('SNR must be specified when add_noise is True')
    if SNR is not None and not (SNR > 0): raise ValueError('SNR must be greater than 0')

    # Total time of the signal
    total_time = duration

    # Total number of samples
    total_samples = int(samples_per_cycle * (total_time * frequency))

    # Time by sample
    sample_time = 1.0 / (samples_per_cycle * frequency)

    #  Create a time vector
    time = np.arange(0, total_time, sample_time)

    # Gera a forma de onda inicial apenas com a fundamental
    signal = amplitude_fundamental * np.sin(2 * np.pi * frequency * time)

    # Add the harmonics at the specified time
    if harmonics_start_time > 0:
        start_index = int(harmonics_start_time / sample_time)
        for harmonic, amp in zip(harmonics, amplitudes):
            signal[start_index:] += amp * np.sin(2 * np.pi * frequency * harmonic * time[start_index:])

    # If the harmonics_start_time is 0, the harmonics starts since the beggining 

    # Add noise if specified
    if add_noise:
        signal = adicionar_ruido(signal, SNR)

    return time, signal
    
def short_circuit_current(amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, fs, add_noise=False, SNR=None):
    """
    Generate short circuit current waveform.

    Parameters
    ----------
    amplitude : float
        Initial amplitude of the current waveform.
    frequency : float
        Frequency of the sinusoidal component.
    short_circuit_time : float
        Time at which the short circuit occurs.
    increase_factor : float
        Factor determining the increase in current during short circuit.
    decay_factor : float
        Exponential decay factor after the increase.
    duration : float
        Total duration of the waveform.
    fs : int
        Sampling frequency.
    add_noise : bool
        Boolean flag indicating whether to add noise to the signal.
    SNR : float
        Desired signal-to-noise ratio in decibels.

    Returns
    -------
    time : numpy.ndarray
        Time vector.
    current : numpy.ndarray
        Short circuit current waveform.

    Examples
    --------
    >>> import functions.SignalGenerator as sg
    >>> import matplotlib.pyplot as plt
    >>> time, current = sg.short_circuit_current(1, 60, 0.5, 2, 0.1, 1, 10000, add_noise=False, SNR=20)
    >>> plt.plot(time, current)
    """

    # Validate input parameters
    if not (isinstance(amplitude, (float, int))): raise TypeError('amplitude must be a number')
    if not (isinstance(frequency, (float, int))): raise TypeError('frequency must be a number')
    if not (isinstance(short_circuit_time, (float, int))): raise TypeError('short_circuit_time must be a number')
    if not (isinstance(increase_factor, (float, int))): raise TypeError('increase_factor must be a number')
    if not (isinstance(decay_factor, (float, int))): raise TypeError('decay_factor must be a number')
    if not (isinstance(duration, (float, int))): raise TypeError('duration must be a number')
    if not (isinstance(fs, (float, int))): raise TypeError('fs must be an Number')
    if not (isinstance(add_noise, bool)): raise TypeError('add_noise must be a boolean')
    if not (isinstance(SNR, (float, int, type(None)))): raise TypeError('SNR must be a float or None')
    if not (amplitude >= 0): raise ValueError('amplitude must be greater than 0')
    if not (frequency > 0): raise ValueError('frequency must be greater than 0')
    if not (short_circuit_time >= 0): raise ValueError('short_circuit_time must be greater than or equal to 0')
    if not (increase_factor > 0): raise ValueError('increase_factor must be greater than 0')
    if not (decay_factor > 0): raise ValueError('decay_factor must be greater than 0')
    if not (duration > 0): raise ValueError('duration must be greater than 0')
    if not (fs > 0): raise ValueError('fs must be greater than 0')
    if add_noise and SNR is None: raise ValueError('SNR must be specified when add_noise is True')
    if SNR is not None and not (SNR > 0): raise ValueError('SNR must be greater than 0')
    
    # Generate time vector
    time = np.arange(0, duration, 1 / fs)

    # Generate short circuit current waveform
    current = amplitude * np.sin(2 * np.pi * frequency * time)

    # Apply short circuit effect after short_circuit_time
    short_circuit_mask = time >= short_circuit_time
    current[short_circuit_mask] *= increase_factor
    current[short_circuit_mask] *= np.exp(-(time[short_circuit_mask] - short_circuit_time) * decay_factor)

    # Add noise if specified
    if add_noise:
        current = adicionar_ruido(current, SNR)

    return time, current
    
def adicionar_ruido(sinal, SNR):
    """
        Adds Gaussian noise to a signal.

        Parameters:
        - signal: numpy array representing the original signal.
        - SNR: Desired signal-to-noise ratio in decibels.

        Returns:
        - noisy_signal: numpy array representing the signal with added noise.
    """
    def gerar_ruido_gaussiano():
        result = 0
        p = 1

        while p > 0:
            temp2 = np.random.rand()
            if temp2 == 0:
                p = 1
            else:
                p = -1

        temp1 = np.cos(2.0 * np.pi * np.random.rand())
        result = np.sqrt(-2.0 * np.log(temp2)) * temp1

        return result

    sinalr = np.zeros_like(sinal)

    for n in range(len(sinal)):
        R = sinal[n] / (np.sqrt(2) * 10 ** (SNR / 20))
        ruido_n = gerar_ruido_gaussiano() * R
        sinalr[n] = sinal[n] + ruido_n

    return sinalr


# # Input Class
# class Generate_Signals:
#     # Function that generates voltage swells under faults
#     @staticmethod
#     def voltage_sag_short_circuit(s, t1, t2, duration, fs, phases, add_noise=False, SNR=None):
#         """
#         Generate three-phase voltage sag caused by a short circuit.

#         Parameters:
#         - s: Sag magnitude in per unit (pu).
#         - t1: Start time of the voltage sag in seconds.
#         - t2: End time of the voltage sag in seconds.
#         - duration: Total duration of the simulation in seconds.
#         - fs: Sampling frequency in Hertz.
#         - phases: String indicating the involved phases ('A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC', etc.).
#         - add_noise: Boolean flag indicating whether to add noise to the signal.
#         - SNR: Desired signal-to-noise ratio in decibels.

#         Returns:
#         - voltage_sag: Dictionary containing three-phase voltage signals during the specified duration.
#           Each phase may have a voltage sag during the specified time interval.
#         """
#         import numpy as np
#         # Generate time vector
#         t = np.arange(0, duration, 1 / fs)

#         # Step functions for start and end time
#         u1 = np.heaviside(t - t1, 1)
#         u2 = np.heaviside(t - t2, 1)

#         # Voltage sag model equation (2)
#         Vsag_A = (1 - s * (u1 - u2)) * np.sin(2 * np.pi * 60 * t)
#         Vsag_B = (1 - s * (u1 - u2)) * np.sin(2 * np.pi * 60 * t - 2 * np.pi / 3)
#         Vsag_C = (1 - s * (u1 - u2)) * np.sin(2 * np.pi * 60 * t + 2 * np.pi / 3)

#         # Initialize all phases to their respective sine waves
#         voltage_sag = {'A': np.sin(2 * np.pi * 60 * t),
#                        'B': np.sin(2 * np.pi * 60 * t - 2 * np.pi / 3),
#                        'C': np.sin(2 * np.pi * 60 * t + 2 * np.pi / 3)}

#         # Set the voltage values for involved phases during the fault
#         if 'A' in phases:
#             voltage_sag['A'] = Vsag_A
#         if 'B' in phases:
#             voltage_sag['B'] = Vsag_B
#         if 'C' in phases:
#             voltage_sag['C'] = Vsag_C

#         # Add noise if specified
#         if add_noise:
#             for phase in voltage_sag:
#                 voltage_sag[phase] = Generate_Signals.adicionar_ruido(voltage_sag[phase], SNR)

#         return voltage_sag
#     @staticmethod
#     def GenerateSignalWithHarmonics(amplitude_fundamental, samples_per_cycle, frequency, harmonics, amplitudes,
#                                     duration, harmonics_start_time, add_noise=False, SNR=None):
#         import numpy as np
#         """
#         Generate a composite signal with fundamental and harmonic components.

#         Parameters:
#         - amplitude_fundamental: The amplitude of the fundamental sinusoidal waveform.
#         - samples_per_cycle: The number of samples per cycle of the fundamental waveform.
#         - frequency: The frequency of the fundamental waveform in hertz.
#         - harmonics: A list of integers representing the harmonics to be added to the fundamental waveform.
#         - amplitudes: A list of amplitudes corresponding to each harmonic in the harmonics list.
#         - duration: The total duration of the generated signal in seconds.
#         - harmonics_start_time: The time at which to start adding harmonics (if greater than 0).
#         - add_noise: Boolean flag indicating whether to add noise to the signal.
#         - SNR: Desired signal-to-noise ratio in decibels.

#         Returns:
#         - time: An array representing the time vector for the generated signal.
#         - signal: An array representing the generated composite signal.
#         """

#         # Total time of the signal
#         total_time = duration

#         # Total number of samples
#         total_samples = int(samples_per_cycle * (total_time * frequency))

#         # Time by sample
#         sample_time = 1.0 / (samples_per_cycle * frequency)

#         #  Create a time vector
#         time = np.arange(0, total_time, sample_time)

#         # Gera a forma de onda inicial apenas com a fundamental
#         signal = amplitude_fundamental * np.sin(2 * np.pi * frequency * time)

#         # Add the harmonics at the specified time
#         if harmonics_start_time > 0:
#             start_index = int(harmonics_start_time / sample_time)
#             for harmonic, amp in zip(harmonics, amplitudes):
#                 signal[start_index:] += amp * np.sin(2 * np.pi * frequency * harmonic * time[start_index:])

#         # If the harmonics_start_time is 0, the harmonics starts since the beggining 

#         # Add noise if specified
#         if add_noise:
#             signal = Generate_Signals.adicionar_ruido(signal, SNR)

#         return time, signal
#     @staticmethod
#     def short_circuit_current(amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, fs,
#                               add_noise=False, SNR=None):
#         import numpy as np
#         """
#         Generate short circuit current waveform.

#         Parameters:
#         - amplitude: Initial amplitude of the current waveform.
#         - frequency: Frequency of the sinusoidal component.
#         - short_circuit_time: Time at which the short circuit occurs.
#         - increase_factor: Factor determining the increase in current during short circuit.
#         - decay_factor: Exponential decay factor after the increase.
#         - duration: Total duration of the waveform.
#         - fs: Sampling frequency.
#         - add_noise: Boolean flag indicating whether to add noise to the signal.
#         - SNR: Desired signal-to-noise ratio in decibels.

#         Returns:
#         - time: Time vector.
#         - current: Short circuit current waveform.
#         """
#         # Generate time vector
#         time = np.arange(0, duration, 1 / fs)

#         # Generate short circuit current waveform
#         current = amplitude * np.sin(2 * np.pi * frequency * time)

#         # Apply short circuit effect after short_circuit_time
#         short_circuit_mask = time >= short_circuit_time
#         current[short_circuit_mask] *= increase_factor
#         current[short_circuit_mask] *= np.exp(-(time[short_circuit_mask] - short_circuit_time) * decay_factor)

#         # Add noise if specified
#         if add_noise:
#             current = Generate_Signals.adicionar_ruido(current, SNR)

#         return time, current
#     @staticmethod
#     def add_noise(sinal, SNR):
#         """
#     Adds Gaussian noise to a signal.

#     Parameters:
#     - signal: numpy array representing the original signal.
#     - SNR: Desired signal-to-noise ratio in decibels.

#     Returns:
#     - noisy_signal: numpy array representing the signal with added noise.
#     """

#         import numpy as np

#         def gerar_ruido_gaussiano():
#             result = 0
#             p = 1

#             while p > 0:
#                 temp2 = np.random.rand()
#                 if temp2 == 0:
#                     p = 1
#                 else:
#                     p = -1

#             temp1 = np.cos(2.0 * np.pi * np.random.rand())
#             result = np.sqrt(-2.0 * np.log(temp2)) * temp1

#             return result

#         sinalr = np.zeros_like(sinal)

#         for n in range(len(sinal)):
#             R = sinal[n] / (np.sqrt(2) * 10 ** (SNR / 20))
#             ruido_n = gerar_ruido_gaussiano() * R
#             sinalr[n] = sinal[n] + ruido_n

#         return sinalr
