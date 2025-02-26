# Signal Processing and Metrics Calculation

This repository contains various modules and scripts for signal processing and metrics calculation. The project includes functionalities for preprocessing, feature extraction, and evaluation of signals using different methods such as wavelet transform, Fourier transform, and variational mode decomposition (VMD).

## Project Structure

```plaintext
├── __pycache__/
├── .gitignore
├── .idea/
├── docs/
├── functions/
├── metricas/
├── README.md
├── rotinas/
├── signal.svg
├── sphinx/
```

### Key Directories and Files

- **functions/**: Contains various signal processing functions and metrics calculators.
- **metricas/**: Contains Jupyter notebooks and scripts for feature extraction and metrics calculation.
- **docs/**: Documentation files generated using Sphinx.

## Installation

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```

## Usage

### Signal Processing

This example shows how to use the `TW_PYWT.evaluate_dwt_single_phase` function from the `functions.TW` module to perform a discrete wavelet transform (DWT) on a signal and visualize the results using Matplotlib.

```python
import functions.TW as TW
import numpy as np
import matplotlib.pyplot as plt
y = np.sin(2*np.pi*60*np.linspace(0, 20/60, 1000))
y[len(y)//2:] *= 2
coefs = TW.TW_PYWT.evaluate_dwt_single_phase(y, 'db4')
plt.subplot(2, 1, 1)
plt.plot(coefs[0])
plt.title('Approximation')
plt.subplot(2, 1, 2)
plt.plot(coefs[1])
plt.title('Detail')
```

### Feature Extraction

The metricas module contains Jupyter notebooks for feature extraction. For example, you can extract features using Fourier Transform:

```python
from Features_Fourier import dft_features

data = ...  # Your signal data
features = dft_features(data)
```

## Documentation

The documentation is generated using Sphinx and can be found in the docs directory.