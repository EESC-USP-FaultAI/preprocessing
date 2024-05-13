import functions
from functions.TW import TW_PYWT
from functions.SignalGenerator.SignalGenerator import GeraSinais
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':


    """Generating Signal"""
    amplitude = 100.00     # Peak amplitude of the current waveform
    frequency = 60.0        # Frequency of the sinusoidal component (60 Hz)
    short_circuit_time = 0.1  # Time at which the short circuit occurs (in seconds)
    increase_factor = 7.0   # Factor determining the increase in current during short circuit
    decay_factor = 5.0      # Exponential decay factor after the increase
    duration = 0.5         # Total duration of the waveform (in seconds)
    samples_per_cycle = 128 # samples per cycle of the generated signal
    sampling_frequency = samples_per_cycle*frequency

    # Example usage with noise
    add_noise_current = True  # Change this to True if you want to add noise
    SNR_current = 60  # Change this to set the SNR for the short circuit current signal

    # Generate short circuit current waveform
    time, short_circuit_current = GeraSinais.short_circuit_current(
        amplitude, frequency, short_circuit_time, increase_factor, decay_factor, duration, sampling_frequency, add_noise_current, SNR_current
    )

    # Plotting generated signal
    plt.plot(time, short_circuit_current)
    plt.title('Short Circuit Current')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.grid(True)
    plt.show()


    """Wavelet Testing"""

    functions.TW.TW_PYWT.list_wavelets()  # Showing wavelets available.
    wave_name = input("Write the name of the wavelet you wanna choose: (db4)")  # User chooses the wavelet they want.
    mode = input("Write the mode of signal extension: (symmetric)")
    print(f"You choose {wave_name} wavelet")
    print(f"You choose {mode} signal extension mode")
    # PyWaveletScripts.wavelet_viewer(wave_name)  # Showing chosen wavelet properties.
    cA1, cD1 = functions.TW.TW_PYWT.evaluate_dwt_single_phase(short_circuit_current, wave_name, mode=mode)  # Evaluating DWT
    cA2, cD2 = functions.TW.TW_PYWT.evaluate_dwt_manually_single_phase(short_circuit_current, wave_name)

    # Plotting Approximation Coefficients
    fig1, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(cA1, label="Package")
    ax2.plot(cA2, label="Manual")
    ax1.set_title("cA Package calculation")
    ax2.set_title("cA Manual calculation")
    ax1.set_xlabel("Sample")
    ax2.set_xlabel("Sample")
    ax1.set_ylabel("cA")
    ax2.set_ylabel("cA")
    ax1.grid(True)
    ax2.grid(True)
    ax1.legend()
    ax2.legend()
    plt.show()


    # Plotting Detail Coefficients
    fig2, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(cD1, label="Package")
    ax2.plot(cD2, label="Manual")
    ax1.set_title("cD Package calculation")
    ax2.set_title("cD Manual calculation")
    ax1.set_xlabel("Sample")
    ax2.set_xlabel("Sample")
    ax1.set_ylabel("cA")
    ax2.set_ylabel("cA")
    ax1.grid(True)
    ax2.grid(True)
    ax1.legend()
    ax2.legend()
    plt.show()

    print(f"cA with package: {cA1}")
    print(f"cA manually: {cA2}")
    print(f"cD with package: {cD1}")
    print(f"cD manually: {cD2}")

    print(f"Euclidean distance cA: {np.sqrt(np.sum(np.square(cA1 - cA2)))}")
    print(f"Euclidean distance cD: {np.sqrt(np.sum(np.square(cD1 - cD2)))}")
