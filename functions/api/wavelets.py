import numpy as np

#TODO: Esse código será removido depois

def morlet_wavelet(t, freq, sigma):
    return np.exp(-t**2 / (2 * sigma**2)) * np.exp(2j * np.pi * freq * t)

def symlet_wavelet(t, j, k):

    #Em que t = tempo
    # j parâmetro de escala
    # k parâmetro de translação

    # A função será zero caso tempo negativo
    if t < 0:
        return 0

    if t < j - k:
        return np.exp(-t / 2) * np.sin(2 * np.pi * t)

    if t < j + k:
        return np.exp(-t / 2) * (np.sin(2 * np.pi * t) + np.cos(2 * np.pi * t))

    # A função será zero para t maior que j + k.
    return 0