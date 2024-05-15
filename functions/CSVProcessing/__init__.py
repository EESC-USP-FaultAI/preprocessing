"""
CSV Processing (:mod:`functions.CSVProcessing`)
===============================================

This module is used to process the CSV files. It contains two functions:

.. autosummary::
    :toctree: functions.TF/
    
    data_selection
    case_selection

.. toctree::
    :maxdepth: 1

    data_selection <functions.CSVProcessing.data_selection>
    case_selection <functions.CSVProcessing.case_selection>

"""







from .Dunno import data_selection, case_selection


__all__ = ["data_selection", "case_selection"]