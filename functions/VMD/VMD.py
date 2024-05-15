#Código comentado linhas a linha em inglês

import numpy as np  # Import NumPy library for numerical operations

def vmd(X, alpha=200, tau=0.1, K=10, tol=1e-7, max_iter=500):
    """
    Variational Mode Decomposition (VMD) algorithm.

    Parameters
    ----------
    X : array
        Input signal (1D array).
    alpha : float, optional
        Regularization parameter (default is 200).
    tau : float, optional
        Center frequency parameter (default is 0.1).
    K : int, optional
        Number of modes (default is 10).
    tol : float, optional
        Tolerance for stopping criteria (default is 1e-7).
    max_iter : int, optional
        Maximum number of iterations (default is 500).

    Returns
    -------
    Modes : array
        Decomposed modes.

    Examples
    -------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from functions.VMD import vmd
    >>> signal = np.sin(2 * np.pi * 0.1 * np.arange(1000)) + np.sin(2 * np.pi * 0.5 * np.arange(1000))
    >>> modes = vmd(signal)
    >>> plt.plot(modes)
    """
    
    N = len(X)  # Length of the input signal
    K = min(K, N // 2)  # Ensure K is not greater than half of the signal length

    # Initialization
    u = np.zeros((N, K))  # Initialize the modes matrix
    omega = np.zeros((N, K))  # Initialize the center frequencies matrix
    alpha_k = alpha * np.ones((N, K))  # Initialize the regularization parameters matrix

    for iteration in range(max_iter):
        # Update modes
        for k in range(K):
            u[:, k] = np.fft.ifft(np.fft.fft(X) / (alpha_k[:, k] + 1j * omega[:, k]))

        # Update center frequencies (omegas)
        for k in range(K - 1):
            omega[:, k] = np.angle(np.fft.fft(u[:, k + 1] - u[:, k]))
        omega[:, -1] = np.angle(np.fft.fft(X - u[:, -1]))

        # Update regularization parameters (alphas)
        alpha_k = alpha_k - tau * (np.sum(np.diff(omega, axis=1), axis=1, keepdims=True) - alpha_k * omega)

        # Stopping criteria
        if np.linalg.norm(X - np.sum(u, axis=1)) / np.linalg.norm(X) < tol:
            break

    return u  # Return the decomposed modes

if __name__ == '__main__':
    import matplotlib.pyplot as plt  # Import Matplotlib library for plotting graphs
    from GeraSinais import GeraSinais  # Import GeraSinais class from GeraSinais module

    # Example usage
    sag_magnitude = 0.5  # Set the sag magnitude
    start_time = 0.1  # Set the start time of the sag
    end_time = 0.5  # Set the end time of the sag
    duration = 1.0  # Set the duration of the sag
    samples_per_cycle = 128  # Set the number of samples per cycle
    frequency = 60.0  # Set the frequency in Hz
    sampling_frequency = samples_per_cycle * frequency  # Set the sampling frequency
    involved_phases = 'AB'  # Set the involved phase or combination

    # Example usage with noise
    add_noise_sag = False  # Set whether to add noise
    SNR_sag = 20  # Set the SNR for the sag signal

    # Generate the three-phase voltage sag signal caused by short circuit
    resulting_voltages = GeraSinais.voltage_sag_short_circuit(
        sag_magnitude, start_time, end_time, duration, sampling_frequency, involved_phases, add_noise_sag, SNR_sag
    )

    # Plotting
    '''
    for phase, voltage in resulting_voltages.items():
        plt.plot(np.arange(0, duration, 1 / sampling_frequency), voltage, label=f'Phase {phase}')
    '''

    signal = np.array(resulting_voltages['A'])  # Convert the resulting voltage signal into a NumPy array

    # Apply VMD to decompose the signal into modes
    modes = vmd(signal)

    # Plot the original signal and decomposed modes
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.subplot(2, 1, 1)  # Create subplot for original signal
    plt.plot(np.arange(0, duration, 1 / sampling_frequency), signal, label='Original Signal')  # Plot the original signal
    plt.legend()  # Show legend

    plt.subplot(2, 1, 2)  # Create subplot for decomposed modes
    for i in range(modes.shape[1]):
        plt.plot(np.arange(0, duration, 1 / sampling_frequency), modes[:, i], label=f'Mode {i + 1}')  # Plot each mode
    plt.legend()  # Show legend

    plt.show()  # Display the plot