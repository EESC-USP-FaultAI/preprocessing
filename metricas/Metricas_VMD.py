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
    T = len(signal)
    t = np.arange(1, T + 1) / T

    u = np.zeros((K, T))
    u_hat = np.zeros((K, T), dtype=complex)
    omega = np.zeros((K,))

    f_hat = np.fft.fftshift(np.fft.fft(signal))
    f_hat_plus = f_hat.copy()
    f_hat_plus[:T // 2] = 0

    u_hat_plus = np.zeros((K, T), dtype=complex)
    lambda_hat = np.zeros((T,), dtype=complex)

    for n in range(1000):
        u_hat_prev = u_hat.copy()

        for k in range(K):
            sum_uk = np.sum(u_hat_plus, axis=0) - u_hat_plus[k]
            u_hat_plus[k] = (f_hat_plus - sum_uk - lambda_hat / 2) / (1 + alpha * (t - omega[k]) ** 2)
            u_hat[k] = u_hat_plus[k] + np.conj(u_hat_plus[k])

        omega = np.angle(np.dot(u_hat, np.exp(-1j * 2 * np.pi * t)))
        omega = np.mean(omega)

        lambda_hat = lambda_hat + tau * (np.sum(u_hat_plus, axis=0) - f_hat_plus)

        if np.linalg.norm(u_hat - u_hat_prev) < tol:
            break

    for k in range(K):
        u[k, :] = np.real(np.fft.ifft(np.fft.ifftshift(u_hat[k])))

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
