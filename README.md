# Prime-Gap Dynamics: Zeta Phase Transistor Test Harness

A quantum control research platform for probing the intersection of analytic number theory and dynamical stability. The project implements a finite-dimensional Hamiltonian system driven by prime frequencies, gap-modulated hopping, and zeta-zero modulation, using a resource-bounded simulation protocol suitable for falsifiable numerical experiments.[web:185][web:186]

## Project overview

The Zeta Phase Transistor treats mathematical structure as an active control law rather than as passive description. In this formulation, primes act as phase carriers, prime gaps act as coupling structure, and zeta-zero frequencies drive the time-dependent envelope of the Hamiltonian.[web:183][web:185]

The core working model is

\[
H(t) = H_{\text{prime}} + \lambda(t) H_{\text{gap}},
\]

where the diagonal term encodes inverse-prime weighting and the hopping term encodes log-normalized adjacent prime gaps, producing a stable finite-dimensional physics engine for numerical study.[web:184][web:186]

### Core hypotheses

- **The Prime Advantage.** The sequential ordering of prime gaps is a dynamical resource that improves phase synchronization and coherence relative to shuffled-gap controls.
- **Lawful Becoming.** Structural identity can be tracked through multiplicative interaction rules and monitored through a multiplicative integrity functional.
- **RH as Stability.** The Riemann Hypothesis is modeled as a stability condition for the transistor’s phase envelope, with off-critical perturbations represented by an exponential envelope parameter.

## Latest results

Current baseline results from the v2.0 simulation engine are summarized below for the prime-ordered chain versus the shuffled-gap null ensemble.

| Metric | True prime order | Shuffled-gap null mean | Signal |
|---|---:|---:|---:|
| Circular phase variance | 0.6476 | 1.3203 | Z = -2.0777 |
| Global fidelity | 0.5401 | 0.3262 | Z = 2.5707 |
| RH-stability stress test at \(\beta = 0.05\) | N/A | N/A | 450% variance-growth increase |

Interpretation: the ordered prime-gap structure behaves as a measurable dynamical stabilizer, lowering phase variance and improving coherence relative to randomized orderings while exhibiting strong instability under envelope perturbation.

## Architecture

The system is organized through an Architecture Decision Record suite:

- **ADR-001:** Hamiltonian v2.0 specification, \(H = H_{\text{prime}} + \lambda H_{\text{gap}}\).
- **ADR-002:** DOP853 integration and standard observables, including circular phase variance, localization, and fidelity.
- **ADR-003:** Shuffled-gap null ensemble for significance testing.
- **ADR-004:** Multiplicative integrity monitoring via \(E_{\text{mult}}\).
- **ADR-005:** RH-stability protocol via exponential-envelope stress testing.

If deeper mathematical detail is needed, start with the ADR index and then the Hamiltonian and observables records before reading the validation protocol.

## Installation

Use Python 3.10 or later and install the baseline dependencies:

```bash
pip install numpy scipy matplotlib
```

## Research CLI

The project is exposed through a unified command-line interface:

```bash
# Run a single pilot simulation
python3 src/cli.py simulate --primes 20 --zeros 10

# Run a null-ensemble validation study
python3 src/cli.py validate --runs 50 --primes 20

# Run a multiplicative integrity check
python3 src/cli.py multiplicity --primes 10 --composites 5

# Run an RH-stability envelope sweep
python3 src/cli.py stability --betas 0.0 0.02 0.05
```

## Project structure

```text
Prime-Gap-Dynamics/
├── docs/
│   └── adrs/             # Architecture Decision Records (001-005)
├── src/
│   ├── cli.py            # Unified research interface
│   ├── simulator.py      # Core Hamiltonian engine (v2.0)
│   ├── validation.py     # Statistical validation harness
│   ├── multiplicity.py   # Integrity monitoring logic
│   └── rh_stability.py   # Stability stress testing
├── Prime-Gap-Dynamics.md # Original theoretical scaffold
└── *.png                 # Baseline and validation plots
```

## What this project contributes

- A finite-dimensional prime-basis Hamiltonian for studying zeta-driven control dynamics.
- A null-model methodology that isolates prime-gap ordering from marginal gap statistics.
- A multiplicative integrity monitor linking recursive number-theoretic structure to dynamical preservation.
- A practical RH-stability protocol built around envelope perturbation and measurable decoherence signatures.

## Roadmap

- **Phase 5.1:** Integrate Lindblad master-equation support for open-system noise analysis.
- **Phase 5.2:** Expand the basis to composites up to \(P_{\max}\) for fuller multiplicative identity mapping.
- **Phase 6.0:** Explore cryptographic bit extraction from transistor switching events and phase-threshold crossings.

## Positioning

This repository is best understood as a research test harness rather than a proof engine. Its purpose is to make number-theoretic dynamical claims operational, reproducible, and statistically testable under explicit finite-resource assumptions.[web:183][web:185]
