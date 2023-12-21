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


a = WaveletTransform
teste = a.wavelet(display=False)
print(len(teste))
