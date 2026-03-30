"""Tests for spectral_sandbox.isep"""
import numpy as np
import pytest
from spectral_sandbox import isep_check, isep_basis


def _random_hermitian(n, seed=0):
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    return A + A.conj().T


@pytest.mark.parametrize("n", [2, 4, 10, 50])
def test_isep_check_passes_for_hermitian(n):
    H = _random_hermitian(n)
    passes, error = isep_check(H)
    assert passes, f"ISEP should pass for Hermitian matrix; error={error}"
    assert error < 1e-8


def test_isep_check_passes_for_real_symmetric():
    A = np.array([[4.0, 2.0], [2.0, 3.0]])
    passes, error = isep_check(A)
    assert passes
    assert error < 1e-12


def test_isep_check_custom_tolerance():
    A = np.eye(3)
    passes_tight, _ = isep_check(A, tol=1e-15)
    passes_loose, _ = isep_check(A, tol=1.0)
    assert passes_tight
    assert passes_loose


def test_isep_basis_sorted():
    A = np.diag([3.0, 1.0, 2.0])
    vals, vecs = isep_basis(A)
    assert np.allclose(vals, [1.0, 2.0, 3.0])
    assert vecs.shape == (3, 3)


def test_isep_basis_orthonormal():
    rng = np.random.default_rng(42)
    B = rng.standard_normal((5, 5))
    H = B + B.T
    vals, vecs = isep_basis(H)
    assert np.allclose(vecs.T @ vecs, np.eye(5), atol=1e-12)
