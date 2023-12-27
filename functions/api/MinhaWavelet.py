class MinhaWavelet:
    def wavelet(wavelet):

        if wavelet == 'db4':
            f_hi = [-0.2303778133088965, 0.7148465705529157,
                        -0.6308807679298589, -0.027983769416859854,
                        0.18703481171909309, 0.030841381835560764,
                        -0.0328830116668852, -0.010597401785069032]
            f_low = [-0.010597401785069032, 0.0328830116668852,
                        0.030841381835560764, -0.18703481171909309,
                        -0.027983769416859854, 0.6308807679298589,
                        0.7148465705529157, 0.2303778133088965]
            return [f_low, f_hi]


        return [None, None]

    def dwt_single(data, wavelet='db4'):
        import numpy as np

        [dec_low, dec_hi] = MinhaWavelet.wavelet(wavelet)

        n = len(dec_low) - 1

        x0 = np.flip(data[0:n])
        x1 = np.flip(data[len(data) - n:len(data)])
        xn = np.concatenate((x0, data, x1))

        ca1 = np.convolve(xn, dec_low, mode='valid')
        ca = []

        cd1 = np.convolve(xn, dec_hi, mode='valid')
        cd = []

        for i in range(0, len(cd1)):
            if i % 2 != 0:
                cd.append(cd1[i])
                ca.append(ca1[i])

        return [ca, cd]

x = [ 0.00000000e+00,  5.00000000e+01,  8.66025404e+01,  1.00000000e+02, 8.66025404e+01,  5.00000000e+01,  5.66553890e-14, -5.00000000e+01,  -8.66025404e+01, -7.00000000e+02, -6.05796944e+02, -3.49514226e+02]

f = MinhaWavelet

[ca, cd] = f.dwt_single(data=x)

print(cd)