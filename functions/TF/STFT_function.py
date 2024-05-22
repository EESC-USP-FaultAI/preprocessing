import numpy as np


def STFT(x, fs, frame_size, hop):
    """
    Perform the Short-Time Fourier Transform (STFT).

    Parameters
    ----------
    x : array-like
        The input signal.
    fs : int
        The sampling frequency.
    frame_size : float
        The frame size.
    hop : float
        The hop size.

    Returns
    -------
    X : array
        The STFT of the input signal.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import functions.TF as tf
    >>> t = np.linspace(0, 5/60, 4800)
    >>> x = np.sin(2*np.pi*60*t)
    >>> x[len(x)//2:] += (0.5*np.sin(2*np.pi*180*t) + 0.2*np.sin(2*np.pi*300*t))[len(x)//2:]
    >>> X = tf.STFT(x, 80, 0.05, 0.025)
    >>> plt.colorbar(plt.imshow(np.abs(X.T), aspect='auto', origin='lower'))
    """

    if not isinstance(x, (np.ndarray, list, tuple)): raise ValueError('Input signal must be an array-like object.')
    if not isinstance(fs, (float, int)): raise ValueError('Sampling frequency must be an number.')
    if not isinstance(frame_size, (float, int)): raise ValueError('Frame size must be a number.')
    if not isinstance(hop, (float, int)): raise ValueError('Hop size must be a number.')

    frame_samp = int(frame_size * fs)
    hop_samp = int(hop * fs)
    w = np.hanning(frame_samp)  #Hanning window
    X = np.array([np.fft.fft(w * x[i:i + frame_samp])
                    for i in range(0, len(x) - frame_samp, hop_samp)])
    return X


# class short_time_fourier_transform():
#     def STFT(x, fs, frame_size, hop):
#         """Perform STFT (Short-Time Fourier Transform).
#         x: Input signal.
#         fs: Sampling frequency.
#         frame_size: Frame size.
#         hop: Hop size
#         """

#         frame_samp = int(frame_size * fs)
#         hop_samp = int(hop * fs)
#         w = np.hanning(frame_samp)  #Hanning window
#         X = np.array([np.fft.fft(w * x[i:i + frame_samp])
#                       for i in range(0, len(x) - frame_samp, hop_samp)])
#         return X
