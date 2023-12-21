import pywt


class WaveletTransform:

    @staticmethod
    def wavelet(family=None, kind=None, discrete=True, continuos=True, display=False):

        if family is not None and kind is not None:
            wavelets = pywt.wavelist(family, kind)
        elif family is not None:
            wavelets = pywt.wavelist(family=family)
        elif kind is not None:
            wavelets = pywt.wavelist(kind=kind)
        else:
            wavelets = pywt.wavelist()

        filter_wavelets = []

        for wavelet in wavelets:
            try:
                if discrete:
                    filter_wavelets.append(wavelet)
                else:
                    pass
            except:
                if continuos:
                    filter_wavelets.append(wavelet)
                else:
                    pass

        if display:
            print("Available Wavelet functions:")
            for wave_name in filter_wavelets:
                print(wave_name)
        return filter_wavelets

    @staticmethod
    def dwt(data, wavelet, mode='symmetric', axis=-1, level=1, details=True):

        """
        :param data: Input signal
        :param wavelet: Mother wavelet to use
        :param mode: Signal extension mode (ex: symmetric)
        :param axis: Axis over which to compute the DWT. If not given, the
        :param level: Multi-level analysis resolution
        :param details: Uses details values to get next level, if false is uses analysis signal
        last axis is used.
        :return: Approximation and detail the first level coefficients.
        """

        if level == 1:
            return pywt.dwt(data, wavelet, mode, axis)
        elif level > 1:

            (cA, cD) = pywt.dwt(data, wavelet, mode, axis)

            for i in range(1,level):
                if details:
                    a1, d1 = pywt.dwt(cD, wavelet, mode, axis)
                else:
                    a1, d1 = pywt.dwt(cA, wavelet, mode, axis)

                cA = a1
                cD = d1

            return cA, cD
        else:
            print('Error: Minimum signal level is 1.')
            return None




a = WaveletTransform
teste = a.wavelet(display=False)
print(len(teste))
