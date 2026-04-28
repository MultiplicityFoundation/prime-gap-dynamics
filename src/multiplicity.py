import numpy as np

def get_composite_witnesses(primes, n_composites=10):
    """
    Generates the first n_composites that can be formed from the given primes.
    Returns a list of tuples: (composite_value, factor_indices)
    where factor_indices is a list of (prime_index, exponent).
    """
    witnesses = []
    # For simplicity, we'll just generate some small composites: p_i * p_j
    # and powers p_i^2
    n_p = len(primes)
    
    # Powers
    for i in range(n_p):
        witnesses.append((primes[i]**2, [(i, 2)]))
    
    # Pairs
    for i in range(n_p):
        for j in range(i + 1, n_p):
            witnesses.append((primes[i] * primes[j], [(i, 1), (j, 1)]))
    
    # Sort by value and take first n_composites
    witnesses.sort(key=lambda x: x[0])
    return witnesses[:n_composites]

class MultiplicityMonitor:
    def __init__(self, primes, n_witnesses=10):
        self.primes = primes
        self.witnesses = get_composite_witnesses(primes, n_witnesses)
        self.n_p = len(primes)
        self.n_w = len(self.witnesses)
        
    def calculate_e_mult(self, states):
        """
        Calculates E_mult(t) as the mean squared error between 
        composite amplitudes and the product of their factor amplitudes.
        states: (time, total_basis_size) 
        where basis is [p1, ..., pN, w1, ..., wK]
        """
        n_t = states.shape[0]
        e_mult = np.zeros(n_t)
        
        for t in range(n_t):
            psi = states[t]
            prime_amps = psi[:self.n_p]
            comp_amps = psi[self.n_p:]
            
            errors = []
            for i, (val, factors) in enumerate(self.witnesses):
                # Target amplitude according to Multiplicity Theory: c_n = product(c_pi^ei)
                target = 1.0
                for p_idx, exp in factors:
                    target *= (prime_amps[p_idx] ** exp)
                
                # We normalize the target to match the local scale if necessary, 
                # but here we measure raw complex distance.
                actual = comp_amps[i]
                errors.append(np.abs(actual - target)**2)
            
            e_mult[t] = np.mean(errors)
            
        return e_mult
