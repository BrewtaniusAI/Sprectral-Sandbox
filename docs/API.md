# API Reference — SpectralSandbox 0.1.0

---

## `spectral_sandbox.isep`

### `isep_check(operator, tol=1e-8)`

Check whether `operator` satisfies the ISEP condition P_O = I.

| Parameter | Type | Description |
|---|---|---|
| `operator` | `np.ndarray` | Square Hermitian (or real symmetric) matrix |
| `tol` | `float` | Frobenius-norm tolerance (default `1e-8`) |

**Returns** `(passes: bool, error: float)`

---

### `isep_basis(operator)`

Return the sorted eigenvalues and orthonormal eigenbasis of `operator`.

| Parameter | Type | Description |
|---|---|---|
| `operator` | `np.ndarray` | Square Hermitian matrix |

**Returns** `(eigenvalues: np.ndarray, eigenbasis: np.ndarray)`

---

## `spectral_sandbox.operators`

### `diagonal_operator(eigenvalues)`

Construct a real diagonal operator.

| Parameter | Type | Description |
|---|---|---|
| `eigenvalues` | `array_like` | 1-D sequence of real eigenvalues |

**Returns** `np.ndarray` of shape `(n, n)`.

---

### `random_hermitian(n, seed=None)`

Generate an `n × n` GUE (Gaussian Unitary Ensemble) sample.

| Parameter | Type | Description |
|---|---|---|
| `n` | `int` | Matrix dimension |
| `seed` | `int \| None` | RNG seed for reproducibility |

**Returns** `np.ndarray` of shape `(n, n)`, dtype `complex128`.

---

### `laplacian_operator(n, periodic=False)`

Build the 1-D discrete Laplacian (finite-difference) operator.

| Parameter | Type | Description |
|---|---|---|
| `n` | `int` | Number of lattice sites |
| `periodic` | `bool` | Use periodic boundary conditions (default `False`) |

**Returns** `np.ndarray` of shape `(n, n)`.

---

### `riemann_zeta_operator(n, sigma=0.5)`

Diagonal operator whose entries approximate the imaginary parts of the first
`n` non-trivial Riemann zeta zeros (heuristic).

| Parameter | Type | Description |
|---|---|---|
| `n` | `int` | Number of approximate zeta zeros |
| `sigma` | `float` | Real part of s (default `0.5`, reserved for future use) |

**Returns** `np.ndarray` of shape `(n, n)`.

---

## `spectral_sandbox.proofvault`

### `class ProofVault`

A registry for mathematical claims.

#### Methods

| Method | Description |
|---|---|
| `register(name, statement, status)` | Register a new claim; raises `ValueError` on duplicate |
| `verify(name, description, data)` | Mark claim as VERIFIED and record evidence |
| `refute(name, description, data)` | Mark claim as REFUTED and record counter-example |
| `summary()` | Return `{status: count}` dictionary |
| `list_claims(status=None)` | List all (or filtered) `Claim` objects |
| `to_json(indent=2)` | Serialise vault to JSON string |
| `ProofVault.from_json(data)` | Deserialise from JSON string |
| `vault[name]` | Direct `Claim` access by name |
| `name in vault` | Membership test |
| `len(vault)` | Number of registered claims |

---

### `class Claim`

A single registered claim (dataclass).

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | Unique identifier |
| `statement` | `str` | Mathematical statement |
| `status` | `ClaimStatus` | Current verification status |
| `evidence` | `list[dict]` | Accumulated evidence records |
| `created_at` | `float` | Unix timestamp of creation |
| `updated_at` | `float` | Unix timestamp of last update |

---

### `class ClaimStatus` (Enum)

| Value | Meaning |
|---|---|
| `CONJECTURE` | Unverified claim |
| `VERIFIED` | Numerically or formally verified |
| `REFUTED` | Counter-example found |
| `OPEN` | Known open problem |
