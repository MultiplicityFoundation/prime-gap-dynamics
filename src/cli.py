import argparse
import sys
import os

# Add current directory to path to allow imports if run from project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulator import ZetaPhaseTransistor, calculate_observables
from validation import run_validation_ensemble, report_results, plot_validation
from multiplicity_test import run_multiplicity_test
from rh_stability import run_stability_comparison

def main():
    parser = argparse.ArgumentParser(
        description="Prime-Gap Dynamics: Zeta Phase Transistor Research CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Research command to execute")
    
    # --- Simulate Command ---
    sim_parser = subparsers.add_parser("simulate", help="Run a single pilot simulation")
    sim_parser.add_argument("--primes", type=int, default=20, help="Number of primes")
    sim_parser.add_argument("--zeros", type=int, default=10, help="Number of zeta zeros")
    sim_parser.add_argument("--t_max", type=float, default=50, help="Simulation time")
    sim_parser.add_argument("--alpha", type=float, default=1.0, help="Energy scale (alpha)")
    sim_parser.add_argument("--eta", type=float, default=0.3, help="Coupling strength (eta)")
    
    # --- Validate Command ---
    val_parser = subparsers.add_parser("validate", help="Run statistical validation ensemble (Null Model)")
    val_parser.add_argument("--runs", type=int, default=50, help="Number of null realizations")
    val_parser.add_argument("--primes", type=int, default=20, help="Number of primes")
    val_parser.add_argument("--t_max", type=float, default=50, help="Simulation time")
    
    # --- Multiplicity Command ---
    mult_parser = subparsers.add_parser("multiplicity", help="Check Multiplicative Integrity (E_mult)")
    mult_parser.add_argument("--primes", type=int, default=10, help="Number of primes")
    mult_parser.add_argument("--composites", type=int, default=5, help="Number of composite witnesses")
    mult_parser.add_argument("--t_max", type=float, default=50, help="Simulation time")
    
    # --- Stability Command ---
    stab_parser = subparsers.add_parser("stability", help="Run RH-Stability stress test (Beta-offset)")
    stab_parser.add_argument("--betas", type=float, nargs="+", default=[0.0, 0.02, 0.05], help="List of beta values")
    stab_parser.add_argument("--t_max", type=float, default=100, help="Simulation time")

    args = parser.parse_args()

    if args.command == "simulate":
        print(f"Running Pilot Simulation (N_p={args.primes}, N_z={args.zeros})...")
        transistor = ZetaPhaseTransistor(
            n_primes=args.primes, 
            n_zeros=args.zeros, 
            alpha=args.alpha, 
            eta=args.eta
        )
        t, states = transistor.simulate(t_max=args.t_max)
        v_circ, ipr, fidelity = calculate_observables(states)
        print(f"Final Circular Phase Variance: {v_circ[-1]:.4f}")
        print(f"Final Fidelity: {fidelity[-1]:.4f}")
        print("Results saved via internal simulator defaults if run script-wise.")

    elif args.command == "validate":
        results, null_metrics = run_validation_ensemble(
            n_runs=args.runs, 
            n_primes=args.primes, 
            t_max=args.t_max
        )
        report_results(results)
        plot_validation(results, null_metrics)

    elif args.command == "multiplicity":
        run_multiplicity_test(
            n_primes=args.primes, 
            n_composites=args.composites, 
            t_max=args.t_max
        )

    elif args.command == "stability":
        run_stability_comparison(
            betas=args.betas, 
            t_max=args.t_max
        )

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
