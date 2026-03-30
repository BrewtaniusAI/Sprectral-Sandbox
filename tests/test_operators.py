"""Tests for spectral_sandbox.operators"""
import numpy as np
import pytest
from spectral_sandbox import (
    diagonal_operator,
    random_hermitian,
    laplacian_operator,
    riemann_zeta_operator,
)
from spectral_sandbox import isep_check


def test_diagonal_operator_shape():
    D = diagonal_operator([1, 2, 3, 4])
    assert D.shape == (4, 4)
    assert np.allclose(np.diag(D), [1, 2, 3, 4])


def test_diagonal_operator_isep():
    D = diagonal_operator([0.5, 1.5, 2.5])
    passes, _ = isep_check(D)
    assert passes


def test_random_hermitian_shape():
    H = random_hermitian(6, seed=1)
    assert H.shape == (6, 6)


def test_random_hermitian_is_hermitian():
    H = random_hermitian(8, seed=99)
    assert np.allclose(H, H.conj().T, atol=1e-14)


def test_random_hermitian_isep():
    H = random_hermitian(10, seed=7)
    passes, _ = isep_check(H)
    assert passes


def test_random_hermitian_reproducible():
    H1 = random_hermitian(5, seed=42)
    H2 = random_hermitian(5, seed=42)
    assert np.allclose(H1, H2)


def test_laplacian_shape():
    L = laplacian_operator(5)
    assert L.shape == (5, 5)


def test_laplacian_tridiagonal():
    L = laplacian_operator(4)
    expected = np.array([
        [-2, 1, 0, 0],
        [1, -2, 1, 0],
        [0, 1, -2, 1],
        [0, 0, 1, -2],
    ], dtype=float)
    assert np.allclose(L, expected)


def test_laplacian_periodic():
    L = laplacian_operator(4, periodic=True)
    assert L[0, 3] == 1.0
    assert L[3, 0] == 1.0
    assert np.allclose(L, L.T)


def test_laplacian_isep():
    L = laplacian_operator(6)
    passes, _ = isep_check(L)
    assert passes


@pytest.mark.parametrize("n", [5, 10, 20])
def test_riemann_zeta_operator_shape(n):
    Z = riemann_zeta_operator(n)
    assert Z.shape == (n, n)


def test_riemann_zeta_operator_diagonal():
    Z = riemann_zeta_operator(4)
    # Only diagonal entries should be nonzero
    assert np.allclose(Z - np.diag(np.diag(Z)), 0)


def test_riemann_zeta_operator_ascending():
    Z = riemann_zeta_operator(10)
    eigs = np.diag(Z)
    assert np.all(np.diff(eigs) > 0), "Approximate zeta zeros should be ascending"
