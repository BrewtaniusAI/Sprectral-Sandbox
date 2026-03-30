"""
spectral_sandbox
================
A lightweight Python toolkit for spectral methods in linear algebra,
exploring operator self-completeness (ISEP), spectral decompositions,
and connections to analytic number theory (Riemann Hypothesis sketch).

Submodules
----------
isep        : Identity-Spanning Eigenprojector (ISEP) checks
operators   : Spectral operator construction utilities
proofvault  : Lightweight claim-and-verify ledger for mathematical results
"""

from .isep import isep_check, isep_basis
from .operators import (
    diagonal_operator,
    random_hermitian,
    laplacian_operator,
    riemann_zeta_operator,
)
from .proofvault import ProofVault

__all__ = [
    "isep_check",
    "isep_basis",
    "diagonal_operator",
    "random_hermitian",
    "laplacian_operator",
    "riemann_zeta_operator",
    "ProofVault",
]

__version__ = "0.1.0"
__author__ = "BrewtaniusAI"
