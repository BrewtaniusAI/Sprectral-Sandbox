# Spectral Gaps, the ISEP Condition, and a Heuristic Sketch Toward the Riemann Hypothesis

**SpectralSandbox Working Paper — v0.1 (2026-03-30)**

> *Status: Exploratory / Conjecture.  Nothing in this document constitutes a
> proof of the Riemann Hypothesis.*

---

## 1. Introduction

The **Riemann Hypothesis** (RH) states that all non-trivial zeros of the
Riemann zeta function

```
ζ(s) = Σ_{n=1}^{∞} n^{-s},   Re(s) > 1   (analytic continuation elsewhere)
```

lie on the *critical line* Re(s) = 1/2.

A long-standing heuristic connection — popularised by Montgomery, Odlyzko, and
Berry–Keating — links the distribution of these zeros to the eigenvalue
statistics of large random Hermitian matrices drawn from the **Gaussian Unitary
Ensemble (GUE)**.  SpectralSandbox provides computational tools to explore this
connection.

---

## 2. The ISEP Condition

A Hermitian operator *H* on an *n*-dimensional Hilbert space satisfies the
**Identity-Spanning Eigenprojector (ISEP)** condition when its eigenprojectors
resolve the identity:

```
P_H = Σ_{k=1}^{n} |ψ_k⟩⟨ψ_k| = I_n
```

`isep_check(H)` verifies this numerically by computing the Frobenius residual

```
ε = ‖ V V† − I ‖_F
```

where *V* is the matrix of eigenvectors from `np.linalg.eigh`.  For any
Hermitian matrix this residual is machine-precision small, confirming
spectral completeness.

### 2.1 Spectral Gaps

The *spectral gap* of H is

```
Δ_H = λ_2 − λ_1   (gap between the two smallest eigenvalues)
```

A large gap indicates strong localisation of the ground state; a vanishing gap
signals a phase transition or degeneracy.  The GUE level-spacing distribution
follows the **Wigner surmise**:

```
p(s) ≈ (π/2) s exp(−π s² / 4)
```

which exhibits **level repulsion** — spacings near zero are suppressed.

---

## 3. The `riemann_zeta_operator`

The function `riemann_zeta_operator(n)` returns a diagonal operator whose
eigenvalues approximate the imaginary parts of the first *n* non-trivial
Riemann zeta zeros by inverting the Riemann–von Mangoldt counting formula:

```
N(T) ≈ (T / 2π) · ln(T / 2πe)
```

Concretely, the *k*-th height *t_k* satisfies `e·u·ln(u) = k`, `t_k = 2πe·u`,
solved numerically via Newton's method.

**Caveat:** The approximation is accurate to within a few percent for k ≳ 10.
For high-precision zero heights use external tables (e.g., Andrew Odlyzko's
published datasets).

---

## 4. Heuristic Sketch

The Berry–Keating conjecture proposes that there exists a self-adjoint
operator *H_RH* whose eigenvalues are exactly the imaginary parts of the
non-trivial zeta zeros.  If such an operator existed and satisfied ISEP, it
would imply (heuristically) that all zeros lie on the critical line.

Using SpectralSandbox:

```python
from spectral_sandbox import riemann_zeta_operator, isep_check, ProofVault
from spectral_sandbox.proofvault import ClaimStatus

n = 50
Z = riemann_zeta_operator(n)
passes, error = isep_check(Z)

vault = ProofVault()
vault.register(
    "isep_zeta_approx",
    f"Approximate zeta operator Z_{n} satisfies ISEP.",
    status=ClaimStatus.CONJECTURE,
)
if passes:
    vault.verify("isep_zeta_approx",
                 description=f"Checked for n={n}",
                 data={"error": error})
print(vault.summary())
```

Since `Z` is diagonal with distinct real eigenvalues it trivially satisfies
ISEP.  The deeper (open) question is whether a *non-diagonal* self-adjoint
operator can be constructed whose eigenvalues equal the *exact* zeta zeros.

---

## 5. Open Questions

1. **Spectral realisation of zeta zeros:** Does there exist a self-adjoint
   operator (in some natural Hilbert space) with spectrum exactly equal to
   {Im(ρ) : ζ(ρ) = 0, Re(ρ) = 1/2}?

2. **GUE universality:** For large *n*, do the nearest-neighbour spacings of
   the approximate zeta zeros converge to the GUE Wigner surmise?

3. **ISEP and criticality:** Can spectral incompleteness (ISEP failure) serve
   as a signature of zeros *off* the critical line?

---

## 6. References

- B. Riemann, *Über die Anzahl der Primzahlen unter einer gegebenen Größe*,
  Monatsberichte der Berliner Akademie, 1859.
- H. L. Montgomery, "The pair correlation of zeros of the zeta function",
  *Proc. Symp. Pure Math.* 24, 181–193 (1973).
- M. V. Berry & J. P. Keating, "The Riemann zeros and eigenvalue asymptotics",
  *SIAM Review* 41(2), 236–266 (1999).
- A. M. Odlyzko, "The 10^20-th zero of the Riemann zeta function and 70
  million of its neighbors", preprint (1989).
