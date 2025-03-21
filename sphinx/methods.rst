
Modules
=======

Pre-Processing Methods
-----------------------

Methods Listed Belowe were implemented to be used as pre-processing methods for the fault detection algorithms.

*  `Fourier Transform (TF) <functions.TF>`

*  `Discrete Wavelet Transform (TW) <functions.TW>`

   -  `Python Implemented DWT (DTW) <functions.TW.DTW>`

   -  `PyWavelets Implemented DWT (TW_PYWT) <functions.TW.TW_PYWT>`

*  `Stockwell Transform (TS) <functions.TS>`

*  `Three-Phase Transform (TT) <functions.TT>`

*  `Variational mode decomposition (VMD) <functions.VMD>`


Utilities
---------

The methods listed below are utilities that can be used to generate synthetic data for testing the fault detection algorithms.

*  `Fault Signal Generator (SignalGenerator) <functions.SignalGenerator>`
*  `CSV Processing (CSVProcessing) <functions.CSVProcessing>`


.. toctree::
   :maxdepth: 1
   :hidden:
   :titlesonly:
   :caption: Pre-Processing Methods:
   
   Fourier Transform <functions.TF>
   
   Discrete Wavelet Transform <functions.TW>

   Stockwell Transform <functions.TS>

   Three-Phase Transform <functions.TT>

   Variational mode decomposition <functions.VMD>


.. toctree::
   :maxdepth: 1
   :hidden:
   :titlesonly:
   :caption: Utilities:

   Fault Signal Generator <functions.SignalGenerator>
   CSV Processing <functions.CSVProcessing>