import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def get_first_n_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                break
        else:
            primes.append(num)
        num += 1
    return np.array(primes)

def get_zeta_zeros(k):
    # First 15 nontrivial zeta zero imaginary parts (t_n)
    t_vals = np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446248, 59.347044, 60.831779, 65.112544
    ])
    return t_vals[:k]

class ZetaPhaseTransistor:
    def __init__(self, n_primes=20, n_zeros=10, alpha=1.0, eta=0.3, gamma_0=0.15, 
                 custom_gnorm=None, n_composites=0, beta=0.0):
        self.n_primes = n_primes
        self.n_zeros = n_zeros
        self.alpha = alpha
        self.eta = eta
        self.gamma_0 = gamma_0
        self.n_composites = n_composites
        self.beta = beta
        
        self.primes = get_first_n_primes(n_primes)
        self.gaps = np.diff(self.primes)
        
        if custom_gnorm is not None:
            self.gnorm = custom_gnorm
        else:
            self.gnorm = np.log1p(self.gaps) / np.log1p(self.gaps.max())
        
        self.t_n = get_zeta_zeros(n_zeros)
        self.gamma_n = gamma_0 / np.sqrt(np.arange(1, n_zeros + 1))
        self.phi_n = np.random.uniform(0, 2 * np.pi, n_zeros)
        
        # Extended basis logic
        self.total_dim = n_primes + n_composites
        if n_composites > 0:
            from multiplicity import get_composite_witnesses
            self.witnesses = get_composite_witnesses(self.primes, n_composites)
        else:
            self.witnesses = []

        # Static Hamiltonian components
        self.H_prime = np.zeros((self.total_dim, self.total_dim), dtype=complex)
        # Prime diagonal
        for i in range(n_primes):
            self.H_prime[i, i] = self.alpha / self.primes[i]
        
        # Composite diagonal (Lawful Energy: E_n = sum(e_i * E_pi))
        for i, (val, factors) in enumerate(self.witnesses):
            energy = 0
            for p_idx, exp in factors:
                energy += exp * (self.alpha / self.primes[p_idx])
            self.H_prime[n_primes + i, n_primes + i] = energy
        
        self.H_gap = np.zeros((self.total_dim, self.total_dim), dtype=complex)
        for i in range(n_primes - 1):
            coupling = self.eta * self.gnorm[i]
            self.H_gap[i, i+1] = coupling
            self.H_gap[i+1, i] = coupling
            # Future extension: add composite-composite hopping or prime-composite leakage

    def lambda_t(self, t):
        # ADR-005: Exponential envelope e^(beta * t)
        envelope = np.exp(self.beta * t)
        modulation = np.sum(self.gamma_n * envelope * np.cos(self.t_n * t + self.phi_n))
        return max(0.1, 1.0 + modulation)

    def schrodinger_rhs(self, t, psi):
        H_t = self.H_prime + self.lambda_t(t) * self.H_gap
        return -1j * (H_t @ psi)

    def simulate(self, t_max=100, dt=0.05):
        t_eval = np.arange(0, t_max, dt)
        
        # Initialize prime amplitudes (uniform)
        psi0_prime = np.ones(self.n_primes, dtype=complex) / np.sqrt(self.n_primes)
        
        if self.n_composites > 0:
            # Initialize composite amplitudes multiplicatively: c_n = product(c_pi^ei)
            psi0_comp = np.zeros(self.n_composites, dtype=complex)
            for i, (val, factors) in enumerate(self.witnesses):
                target = 1.0
                for p_idx, exp in factors:
                    target *= (psi0_prime[p_idx] ** exp)
                psi0_comp[i] = target
            psi0 = np.concatenate([psi0_prime, psi0_comp])
            # Re-normalize total state
            psi0 /= np.linalg.norm(psi0)
        else:
            psi0 = psi0_prime
        
        sol = solve_ivp(
            self.schrodinger_rhs,
            (0, t_max),
            psi0,
            t_eval=t_eval,
            method='DOP853',
            rtol=1e-8,
            atol=1e-10
        )
        return sol.t, sol.y.T

def calculate_observables(states, n_primes=None):
    # states shape: (time, basis_size)
    if n_primes is None:
        n_primes = states.shape[1]
    
    prime_states = states[:, :n_primes]
    
    # 1. Circular Phase Variance (on primes only)
    phases = np.angle(prime_states)
    mean_phase = np.angle(np.mean(np.exp(1j * phases), axis=1))
    dev = np.angle(np.exp(1j * (phases - mean_phase[:, None])))
    v_circ = np.mean(dev**2, axis=1)
    
    # 2. Inverse Participation Ratio (IPR) - full basis
    probs = np.abs(states)**2
    ipr = np.sum(probs**2, axis=1)
    
    # 3. Fidelity to initial state - full basis
    psi0 = states[0]
    fidelity = np.abs(states @ np.conj(psi0))**2
    
    return v_circ, ipr, fidelity

if __name__ == "__main__":
    print("Initializing Zeta Phase Transistor Simulator...")
    transistor = ZetaPhaseTransistor(n_primes=20, n_zeros=10)
    
    print("Running simulation...")
    t, states = transistor.simulate(t_max=50)
    
    v_circ, ipr, fidelity = calculate_observables(states)
    
    print("Simulation complete. Basic stats:")
    print(f"Final Circular Phase Variance: {v_circ[-1]:.4f}")
    print(f"Final IPR: {ipr[-1]:.4f}")
    print(f"Final Fidelity: {fidelity[-1]:.4f}")
    
    # Optional: Plotting
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(t, v_circ)
    plt.title("Circular Phase Variance")
    plt.subplot(3, 1, 2)
    plt.plot(t, ipr)
    plt.title("Inverse Participation Ratio (IPR)")
    plt.subplot(3, 1, 3)
    plt.plot(t, fidelity)
    plt.title("Fidelity to Initial State")
    plt.tight_layout()
    plt.savefig("/home/multiplicity/Prime-Gap Dynamics/pilot_simulation.png")
    print("Pilot plot saved to pilot_simulation.png")
