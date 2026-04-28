import numpy as np
import matplotlib.pyplot as plt
from simulator import ZetaPhaseTransistor, calculate_observables
import time

def run_validation_ensemble(n_runs=50, n_primes=20, n_zeros=10, t_max=50):
    print(f"Starting Validation Ensemble (N_primes={n_primes}, N_runs={n_runs})...")
    
    # 1. True Model Run
    transistor_true = ZetaPhaseTransistor(n_primes=n_primes, n_zeros=n_zeros)
    t, states_true = transistor_true.simulate(t_max=t_max)
    v_true, ipr_true, fid_true = calculate_observables(states_true, n_primes=n_primes)
    
    true_metrics = {
        'v_circ': np.mean(v_true),
        'ipr': np.mean(ipr_true),
        'fidelity': np.mean(fid_true)
    }
    
    # 2. Null Model Ensemble (Shuffled Gaps)
    gnorm_base = transistor_true.gnorm.copy()
    null_metrics = {'v_circ': [], 'ipr': [], 'fidelity': []}
    
    start_time = time.time()
    for i in range(n_runs):
        if (i+1) % 10 == 0:
            print(f"  Progress: {i+1}/{n_runs}...")
            
        shuffled_gnorm = np.random.permutation(gnorm_base)
        transistor_null = ZetaPhaseTransistor(
            n_primes=n_primes, 
            n_zeros=n_zeros, 
            custom_gnorm=shuffled_gnorm
        )
        # Ensure identical zero phases for fair comparison per run if needed, 
        # but here we follow ADR-003 standard of ensemble distribution.
        
        _, states_null = transistor_null.simulate(t_max=t_max)
        v_n, ipr_n, fid_n = calculate_observables(states_null, n_primes=n_primes)
        
        null_metrics['v_circ'].append(np.mean(v_n))
        null_metrics['ipr'].append(np.mean(ipr_n))
        null_metrics['fidelity'].append(np.mean(fid_n))
    
    duration = time.time() - start_time
    print(f"Ensemble complete in {duration:.2f}s.")
    
    # 3. Statistical Analysis
    results = {}
    for key in true_metrics:
        true_val = true_metrics[key]
        null_vals = np.array(null_metrics[key])
        mean_null = np.mean(null_vals)
        std_null = np.std(null_vals)
        z_score = (true_val - mean_null) / std_null if std_null > 0 else 0
        
        results[key] = {
            'true': true_val,
            'null_mean': mean_null,
            'null_std': std_null,
            'z_score': z_score
        }
    
    return results, null_metrics

def report_results(results):
    print("\n" + "="*40)
    print("ZETA PHASE TRANSISTOR VALIDATION REPORT")
    print("="*40)
    print(f"{'Metric':<12} | {'True':<8} | {'Null μ':<8} | {'Z-Score':<8}")
    print("-" * 40)
    for key, data in results.items():
        print(f"{key:<12} | {data['true']:<8.4f} | {data['null_mean']:<8.4f} | {data['z_score']:<8.4f}")
    print("="*40)

def plot_validation(results, null_metrics):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    metrics = list(results.keys())
    
    for i, key in enumerate(metrics):
        axes[i].hist(null_metrics[key], bins=15, alpha=0.6, label='Null Ensemble', color='gray')
        axes[i].axvline(results[key]['true'], color='red', linestyle='--', linewidth=2, label='True Prime Order')
        axes[i].set_title(f"Distribution of {key}")
        axes[i].set_xlabel("Value")
        axes[i].legend()
    
    plt.tight_layout()
    plt.savefig("/home/multiplicity/Prime-Gap Dynamics/validation_results.png")
    print("Validation plots saved to validation_results.png")

if __name__ == "__main__":
    # Standard validation run: 20 primes, 50 null realizations
    results, null_metrics = run_validation_ensemble(n_runs=50, n_primes=20)
    report_results(results)
    plot_validation(results, null_metrics)
