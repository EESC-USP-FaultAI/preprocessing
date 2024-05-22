from matplotlib import pyplot as plt

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import functions.SignalGenerator as GeraSinais
import functions.TW.DTW as DWT

#Editado caio 19/01 - editado agora
def main():
    # Generate signals
    voltage_sag_signals = GeraSinais.voltage_sag_short_circuit(0.9, 0.01, 0.02, 0.03, 60, 'A', True, 30)

    # Example of fault signals
    time, fault_signals = GeraSinais.short_circuit_current(100, 60, 0.0125, 7, 0.5, 0.016, 256 * 60, True, 30)

    # Apply wavelet transform
    ca, cd = DWT.transform(fault_signals, 'db4')

    # Plotting generated signal
    plt.plot(time, fault_signals)
    plt.title('Short Circuit Current')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.grid(True)
    plt.show()


    # Plot the results
    DWT.plot(ca, cd)

    # Display coefficients
    print(f"\nCoeficientes de Aproximação: {ca}")
    print(f"Coeficientes de Detalhe: {cd}\n")


if __name__ == "__main__":
    main()
