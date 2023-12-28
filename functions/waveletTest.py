from api.GeraSinais import GeraSinais
import api.MinhaWavelet as mw


def main():
    # Generate signals
    voltage_sag_signals = GeraSinais.voltage_sag_short_circuit(0.9, 0.01, 0.02, 0.03, 60, 'A', True, 30)

    # Example of fault signals
    time, fault_signals = GeraSinais.short_circuit_current(100, 60, 0.0125, 7, 0.5, 0.016, 32 * 60, False, 100)

    # Apply wavelet transform
    wavelet_instance = mw.MyWavelet
    ca, cd = wavelet_instance.dwt_single_name(fault_signals, 'db4')

    # Plot the results
    wavelet_instance.plot(ca, cd)

    # Display coefficients
    print(f"\nCoeficientes de Aproximação: {ca}")
    print(f"Coeficientes de Detalhe: {cd}\n")


if __name__ == "__main__":
    main()
