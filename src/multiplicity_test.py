import numpy as np
import matplotlib.pyplot as plt
from simulator import ZetaPhaseTransistor, calculate_observables
from multiplicity import MultiplicityMonitor

def run_multiplicity_test(n_primes=10, n_composites=5, t_max=50):
    print(f"Starting Multiplicity Integrity Test (N_p={n_primes}, N_c={n_composites})...")
    
    # Initialize transistor with extended basis
    transistor = ZetaPhaseTransistor(
        n_primes=n_primes, 
        n_zeros=10, 
        n_composites=n_composites
    )
    
    # Initialize monitor
    monitor = MultiplicityMonitor(transistor.primes, n_witnesses=n_composites)
    
    print("Running simulation...")
    t, states = transistor.simulate(t_max=t_max)
    
    # Calculate standard observables
    v_circ, ipr, fidelity = calculate_observables(states, n_primes=n_primes)
    
    # Calculate Multiplicative Integrity (E_mult)
    print("Calculating Multiplicative Integrity (E_mult)...")
    e_mult = monitor.calculate_e_mult(states)
    
    print(f"Final E_mult: {e_mult[-1]:.4e}")
    
    # Plotting
    plt.figure(figsize=(12, 10))
    plt.subplot(4, 1, 1)
    plt.plot(t, v_circ)
    plt.title("Circular Phase Variance (Primes Only)")
    
    plt.subplot(4, 1, 2)
    plt.plot(t, ipr)
    plt.title("IPR (Full Basis)")
    
    plt.subplot(4, 1, 3)
    plt.plot(t, fidelity)
    plt.title("Fidelity (Full Basis)")
    
    plt.subplot(4, 1, 4)
    plt.plot(t, e_mult)
    plt.title("Multiplicative Integrity Error (E_mult)")
    plt.yscale('log')
    plt.xlabel("Time")
    
    plt.tight_layout()
    plt.savefig("/home/multiplicity/Prime-Gap Dynamics/multiplicity_integrity_test.png")
    print("Multiplicity test results saved to multiplicity_integrity_test.png")
    
    return t, e_mult

if __name__ == "__main__":
    run_multiplicity_test()
