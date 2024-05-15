'''
Variational mode decomposition (:mod:`functions.VMD`)
====================================

This module contains the implementation of the variational mode decomposition (VMD) algorithm.

.. autosummary::
    :toctree: functions.TF/
    
    vmd

.. toctree::
    :maxdepth: 1

    vmd <functions.VMD.vmd>

'''


from .VMD import vmd

__all__ = ["vmd"]