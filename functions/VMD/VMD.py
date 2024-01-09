import numpy as np
import matplotlib.pyplot as plt
from functions.SignalGenerator.GeraSinais import GeraSinais # Import the class from the module

def vmd(X, alpha=200, tau=0.1, K=10, tol=1e-7, max_iter=500):
    """
    Variational Mode Decomposition (VMD) algorithm.

    Parameters:
    - X: Input signal (1D array)
    - alpha: Regularization parameter
    - tau: Center frequency parameter
    - K: Number of modes
    - tol: Tolerance for stopping criteria
    - max_iter: Maximum number of iterations

    Returns:
    - Modes: Decomposed modes
    """
    N = len(X)
    K = min(K, N // 2)  # Ensure K is not greater than half of the signal length

    # Initialization
    u = np.zeros((N, K))
    omega = np.zeros((N, K))
    alpha_k = alpha * np.ones((N, K))

    for iteration in range(max_iter):
        # Update modes
        for k in range(K):
            u[:, k] = np.fft.ifft(np.fft.fft(X) / (alpha_k[:, k] + 1j * omega[:, k]))

        # Update omegas
        for k in range(K - 1):
            omega[:, k] = np.angle(np.fft.fft(u[:, k + 1] - u[:, k]))

        omega[:, -1] = np.angle(np.fft.fft(X - u[:, -1]))

        # Update alphas
        alpha_k = alpha_k - tau * (np.sum(np.diff(omega, axis=1), axis=1, keepdims=True) - alpha_k * omega)

        # Stopping criteria
        if np.linalg.norm(X - np.sum(u, axis=1)) / np.linalg.norm(X) < tol:
            break

    return u

# Example usage
sag_magnitude = 0.5  # Change this to set the sag magnitude
start_time = 0.1  # Change this to set the start time of the sag
end_time = 0.5  # Change this to set the end time of the sag
duration = 1.0  # Change this to set the duration of the sag
samples_per_cycle = 128
frequency = 60.0  # frequencia em Hz
sampling_frequency = samples_per_cycle * frequency  # Change this to set the sampling frequency
involved_phases = 'AB'  # Change this to set the involved phase or combination

# Example usage with noise
add_noise_sag = False  # Change this to True if you want to add noise
SNR_sag = 20  # Change this to set the SNR for the sag signal

resulting_voltages = GeraSinais.voltage_sag_short_circuit(
    sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, add_noise_sag, SNR_sag
)

# Plotting
'''for phase, voltage in resulting_voltages.items():
    plt.plot(np.arange(0, duration, 1 / sampling_frequency), voltage, label=f'Phase {phase}')'''

signal = np.array(resulting_voltages['A'])

# Apply VMD to decompose the signal
modes = vmd(signal)

# Plot the original signal and decomposed modes
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(np.arange(0, duration, 1 / sampling_frequency), signal, label='Original Signal')
plt.legend()

plt.subplot(2, 1, 2)
for i in range(modes.shape[1]):
    plt.plot(np.arange(0, duration, 1 / sampling_frequency), modes[:, i], label=f'Mode {i + 1}')
plt.legend()

plt.show()
