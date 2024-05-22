"""
Fault Signal Conditions Generator Package
=========================================

Code to generate fault and non-linear signals.

.. autosummary::
   :toctree: generated/

   voltage_sag_short_circuit 
   short_circuit_current
   GenerateSignalWithHarmonics

questions: gabrielanuneslopes@usp.br
"""

from .SignalGenerator import voltage_sag_short_circuit, short_circuit_current, GenerateSignalWithHarmonics

__all__ = [
    'voltage_sag_short_circuit',
    'GenerateSignalWithHarmonics',
    'short_circuit_current',
]
