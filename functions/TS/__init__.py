'''
Stockwell Transform Functions
=============================

.. autosummary::
    :toctree: generated/
    
    calculate_ST_of_the_signal
    stockwell_transform

.. note::
    If the user wants to calculate the ST of a signal, they should use the method:
    def `calculate_ST_of_the_signal(self, signal, window_size, k)`
'''


from .ST import calculate_ST_of_the_signal, stockwell_transform

__all__ = [
    'calculate_ST_of_the_signal',
    'stockwell_transform',
]