
from . import fft_c

__all__ = ['fft', 'fft_faster']

def fft(x):
    return fft_c.fft(x.copy())

def fft_faster(x):
    return fft_c.fft_inplace(x.copy())