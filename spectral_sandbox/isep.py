"""
isep.py – Identity-Spanning Eigenprojector (ISEP) checks
=========================================================

The *ISEP condition* (also written  P_O = I) asserts that the eigenprojectors
of a Hermitian operator O span the full Hilbert space:

    P_O  =  Σ_k  |ψ_k⟩⟨ψ_k|  =  I

When P_O = I the operator is said to be *identity-spanning*.  This is
equivalent to the standard statement that a Hermitian matrix has a complete
orthonormal eigenbasis, and is used throughout the SpectralSandbox package as
a sanity-check after constructing or loading operators.
"""

import numpy as np


def isep_check(operator: np.ndarray, tol: float = 1e-8) -> tuple[bool, float]:
    """Check whether *operator* satisfies the ISEP condition P_O = I.

    Parameters
    ----------
    operator : numpy.ndarray
        A square, Hermitian (or real symmetric) matrix.
    tol : float, optional
        Absolute tolerance for the Frobenius-norm residual ||P_O - I||_F.
        Defaults to 1e-8.

    Returns
    -------
    passes : bool
        ``True`` if ||P_O - I||_F < *tol*.
    error : float
        The actual Frobenius-norm residual.

    Examples
    --------
    >>> import numpy as np
    >>> from spectral_sandbox import isep_check
    >>> A = np.array([[2, 1], [1, 3]], dtype=float)
    >>> passes, err = isep_check(A)
    >>> passes
    True
    """
    eigvals, eigvecs = np.linalg.eigh(operator)
    span = eigvecs @ eigvecs.conj().T
    identity = np.eye(operator.shape[0])
    error = float(np.linalg.norm(span - identity))
    return error < tol, error


def isep_basis(operator: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return the sorted (ascending) eigenvalues and orthonormal eigenbasis.

    Parameters
    ----------
    operator : numpy.ndarray
        A square, Hermitian (or real symmetric) matrix.

    Returns
    -------
    eigenvalues : numpy.ndarray, shape (n,)
        Real eigenvalues sorted in ascending order.
    eigenbasis : numpy.ndarray, shape (n, n)
        Columns are the corresponding unit eigenvectors.

    Examples
    --------
    >>> import numpy as np
    >>> from spectral_sandbox import isep_basis
    >>> A = np.diag([3.0, 1.0, 2.0])
    >>> vals, vecs = isep_basis(A)
    >>> vals
    array([1., 2., 3.])
    """
    eigenvalues, eigenbasis = np.linalg.eigh(operator)
    return eigenvalues, eigenbasis
