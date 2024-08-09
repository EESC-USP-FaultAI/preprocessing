import pandas as pd
import numpy as np
from scipy.linalg import svd
from scipy.signal import hilbert


def read_signals(file_path):
    return pd.read_csv(file_path)


def extract_signals(df, posi_falta):
    Va = df.iloc[3:, 1].values
    Vb = df.iloc[3:, 2].values
    Vc = df.iloc[3:, 3].values

    Va = Va[posi_falta:posi_falta + 22]
    Vb = Vb[posi_falta:posi_falta + 22]
    Vc = Vc[posi_falta:posi_falta + 22]

    return Va, Vb, Vc


def apply_vmd(signal, alpha=2000, tau=0, K=3, DC=0, init=1, tol=1e-7):
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
    N = len(signal)
    K = min(K, N // 2)  # Ensure K is not greater than half of the signal length

    # Initialization
    u = np.zeros((N, K), dtype=np.complex128)
    omega = np.zeros((N, K))
    alpha_k = alpha * np.ones((N, K))

    for iteration in range(1000):
        # Update modes
        for k in range(K):
            u[:, k] = np.fft.ifft(np.fft.fft(signal) / (alpha_k[:, k] + 1j * omega[:, k]))

        # Update omegas
        for k in range(K - 1):
            omega[:, k] = np.angle(np.fft.fft(u[:, k + 1] - u[:, k]))

        omega[:, -1] = np.angle(np.fft.fft(signal - u[:, -1]))

        # Update alphas
        alpha_k = alpha_k - tau * (np.sum(np.diff(omega, axis=1), axis=1, keepdims=True) - alpha_k * omega)

        # Stopping criteria
        if np.linalg.norm(signal - np.sum(u, axis=1)) / np.linalg.norm(signal) < tol:
            break

    return u


def process_signals(file_path, posi_falta):
    df = read_signals(file_path)
    Va, Vb, Vc = extract_signals(df, posi_falta)

    imf_va = apply_vmd(Va)
    s_va = svd(imf_va, full_matrices=False)[1]

    return s_va


def main():
    config1_path = 'E:/Doutorado/P&D - FaultAIFinder/P&D - Processamento/preprocessing/dados_testes/configuracao_1/tensao/dados_tensao_config_1.csv'
    config2_path = 'E:/Doutorado/P&D - FaultAIFinder/P&D - Processamento/preprocessing/dados_testes/configuracao_2/tensao/dados_tensao_config_2.csv'

    sinais_config1 = read_signals(config1_path)
    tempo = sinais_config1.iloc[3:, 0].values
    posi_falta = np.where(tempo == 0.103821620000000)[0][0]

    s1 = process_signals(config1_path, posi_falta)
    s2 = process_signals(config2_path, posi_falta)

    print("Singular values for configuration 1:", s1)
    print("Singular values for configuration 2:", s2)


if __name__ == "__main__":
    main()
