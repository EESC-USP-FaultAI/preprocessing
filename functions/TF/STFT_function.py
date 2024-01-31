import numpy as np

class short_time_fourier_transform():
    def STFT(x, fs, frame_size, hop):
        """
        Perform STFT (Short-Time Fourier Transform).

        x: Input data.
        fs: Sampling rate.
        frame_size: Frame size.
        hop: Hop size
        """

        frame_samp = int(frame_size * fs)
        hop_samp = int(hop * fs)
        w = np.hanning(frame_samp)  # Hanning window
        X = np.array([np.fft.fft(w * x[i:i + frame_samp])
                      for i in range(0, len(x) - frame_samp, hop_samp)])
        return X
