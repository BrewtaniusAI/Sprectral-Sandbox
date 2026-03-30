"""
operators.py – Spectral operator construction utilities
=======================================================

Factory functions for building Hermitian matrices (operators) that are
commonly used in spectral analysis and in sketches connecting random-matrix
theory to analytic number theory.
"""

import numpy as np


def diagonal_operator(eigenvalues: np.ndarray) -> np.ndarray:
    """Construct a real diagonal operator from a sequence of eigenvalues.

    Parameters
    ----------
    eigenvalues : array_like
        1-D sequence of real eigenvalues.

    Returns
    -------
    numpy.ndarray
        Diagonal matrix of shape (n, n).

    Examples
    --------
    >>> import numpy as np
    >>> from spectral_sandbox import diagonal_operator
    >>> diagonal_operator([1, 2, 3])
    array([[1., 0., 0.],
           [0., 2., 0.],
           [0., 0., 3.]])
    """
    vals = np.asarray(eigenvalues, dtype=float)
    return np.diag(vals)


def random_hermitian(n: int, seed: int | None = None) -> np.ndarray:
    """Generate a random *n × n* Hermitian matrix from the GUE.

    The Gaussian Unitary Ensemble (GUE) is defined by drawing an n×n matrix
    of i.i.d. complex Gaussians G and returning (G + G†) / (2√n).

    Parameters
    ----------
    n : int
        Matrix dimension.
    seed : int or None, optional
        Random seed for reproducibility.

    Returns
    -------
    numpy.ndarray, shape (n, n), dtype complex128
        A Hermitian GUE sample.

    Examples
    --------
    >>> from spectral_sandbox import random_hermitian
    >>> H = random_hermitian(4, seed=0)
    >>> H.shape
    (4, 4)
    """
    rng = np.random.default_rng(seed)
    real_part = rng.standard_normal((n, n))
    imag_part = rng.standard_normal((n, n))
    G = real_part + 1j * imag_part
    H = (G + G.conj().T) / (2 * np.sqrt(n))
    return H


def laplacian_operator(n: int, periodic: bool = False) -> np.ndarray:
    """Build the 1-D discrete Laplacian (finite-difference) operator.

    Parameters
    ----------
    n : int
        Number of lattice sites.
    periodic : bool, optional
        If ``True``, use periodic (circulant) boundary conditions.
        Defaults to ``False`` (Dirichlet / open boundaries).

    Returns
    -------
    numpy.ndarray, shape (n, n)
        Real symmetric tridiagonal Laplacian matrix with −2 on the diagonal
        and +1 on the super- and sub-diagonals.

    Examples
    --------
    >>> from spectral_sandbox import laplacian_operator
    >>> laplacian_operator(4)
    array([[-2.,  1.,  0.,  0.],
           [ 1., -2.,  1.,  0.],
           [ 0.,  1., -2.,  1.],
           [ 0.,  0.,  1., -2.]])
    """
    L = -2.0 * np.eye(n) + np.diag(np.ones(n - 1), 1) + np.diag(np.ones(n - 1), -1)
    if periodic and n > 2:
        L[0, n - 1] = 1.0
        L[n - 1, 0] = 1.0
    return L


def riemann_zeta_operator(n: int, sigma: float = 0.5) -> np.ndarray:
    """Construct an *n × n* diagonal operator whose eigenvalues approximate
    the imaginary parts of Riemann zeta zeros on the critical line.

    .. note::
        This is a *heuristic sketch*, not a rigorous construction.  The
        non-trivial zeros of ζ(s) on the critical line Re(s) = ½ are
        approximated by inverting the Riemann–von Mangoldt counting formula

            N(T)  ≈  (T / 2π) · ln(T / 2πe)

        That is, the *k*-th zero height *t_k* satisfies

            e · u · ln(u)  =  k,   t_k  =  2πe · u

        which is solved numerically via Newton's method.  The approximation
        is accurate to within a few percent for k ≳ 10; for small k the
        values are order-of-magnitude estimates only.

    Parameters
    ----------
    n : int
        Number of approximate zeta zeros to include.
    sigma : float, optional
        Real part of s (default 0.5, the critical line).  Not currently used
        in the approximation formula but retained for future extensions.

    Returns
    -------
    numpy.ndarray, shape (n, n)
        Real diagonal matrix with approximate zeta-zero imaginary parts,
        in ascending order.

    Examples
    --------
    >>> from spectral_sandbox import riemann_zeta_operator
    >>> Z = riemann_zeta_operator(5)
    >>> Z.shape
    (5, 5)
    """
    k = np.arange(1, n + 1, dtype=float)
    # Solve  e·u·ln(u) = k  ⟺  u·ln(u) = k/e
    # via Newton's method.  t_k = 2πe·u.
    # 60 iterations is ample for double-precision convergence; Newton's method
    # converges quadratically once near the root, so < 10 iterations suffice
    # in practice.  The higher limit guards against edge cases near u → 0⁺.
    _MAX_NEWTON_ITER = 60
    rhs = k / np.e
    u = np.log(k + np.e)  # positive initial guess (log(k+e) ≥ 1 for k ≥ 1)
    for _ in range(_MAX_NEWTON_ITER):
        u = np.maximum(u, 1e-12)
        f = u * np.log(u) - rhs
        fp = np.log(u) + 1.0
        # Avoid division by near-zero derivative
        fp = np.where(np.abs(fp) < 1e-14, np.sign(fp + 1e-30) * 1e-14, fp)
        u = u - f / fp
        u = np.maximum(u, 1e-12)
    t_k = 2 * np.pi * np.e * u
    return np.diag(t_k)
