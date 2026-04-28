import numpy as np
import matplotlib.pyplot as plt
from simulator import ZetaPhaseTransistor, calculate_observables

def run_stability_comparison(betas=[0.0, 0.02, 0.05], t_max=100):
    print(f"Starting RH-Stability Stress Test (Betas={betas}, T_max={t_max})...")
    
    plt.figure(figsize=(12, 10))
    
    results = {}
    
    for beta in betas:
        print(f"  Simulating beta = {beta}...")
        transistor = ZetaPhaseTransistor(n_primes=20, n_zeros=10, beta=beta)
        t, states = transistor.simulate(t_max=t_max)
        
        v_circ, ipr, fidelity = calculate_observables(states)
        results[beta] = (t, v_circ, fidelity)
        
        plt.subplot(2, 1, 1)
        plt.plot(t, v_circ, label=f"beta={beta}")
        
        plt.subplot(2, 1, 2)
        plt.plot(t, fidelity, label=f"beta={beta}")
    
    plt.subplot(2, 1, 1)
    plt.title("Circular Phase Variance (V_circ)")
    plt.ylabel("Variance")
    plt.yscale('log')
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.title("Fidelity to Initial State")
    plt.ylabel("Fidelity")
    plt.xlabel("Time")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig("/home/multiplicity/Prime-Gap Dynamics/rh_stability_test.png")
    print("Stability test results saved to rh_stability_test.png")
    
    # Analyze instability signature
    print("\nInstability Analysis:")
    # We use t=1.0 as a baseline since t=0 has zero variance by construction
    baseline_idx = int(1.0 / (t[1] - t[0])) 
    for beta in betas:
        t, v_circ, _ = results[beta]
        growth = v_circ[-1] / v_circ[baseline_idx] if v_circ[baseline_idx] > 0 else 0
        print(f"  Beta {beta:<5}: Phase Variance Growth (T_max / T_1.0) = {growth:.2f}")

if __name__ == "__main__":
    run_stability_comparison()
