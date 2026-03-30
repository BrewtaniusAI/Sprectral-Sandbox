"""
proofvault.py – Lightweight claim-and-verify ledger
====================================================

The ``ProofVault`` class provides a simple in-memory (and optionally
JSON-serialisable) registry for mathematical claims and their verification
status.  It is designed for exploratory research workflows where you want to
track which assertions have been numerically checked, which are conjectures,
and which have counter-examples.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ClaimStatus(str, Enum):
    """Verification status of a registered claim."""

    CONJECTURE = "conjecture"   # Unverified
    VERIFIED = "verified"       # Numerically or formally verified
    REFUTED = "refuted"         # Counter-example found
    OPEN = "open"               # Known open problem


@dataclass
class Claim:
    """A single mathematical claim entry."""

    name: str
    statement: str
    status: ClaimStatus = ClaimStatus.CONJECTURE
    evidence: list[dict[str, Any]] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def add_evidence(self, description: str, data: Any = None) -> None:
        """Append an evidence record to this claim.

        Parameters
        ----------
        description : str
            Human-readable description of the evidence.
        data : any, optional
            Serialisable supporting data (e.g. numerical residual, dict).
        """
        self.evidence.append({"description": description, "data": data})
        self.updated_at = time.time()

    def verify(self, description: str = "Numerically verified", data: Any = None) -> None:
        """Mark the claim as verified and record evidence."""
        self.status = ClaimStatus.VERIFIED
        self.add_evidence(description, data)

    def refute(self, description: str = "Counter-example found", data: Any = None) -> None:
        """Mark the claim as refuted and record the counter-example."""
        self.status = ClaimStatus.REFUTED
        self.add_evidence(description, data)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        return d


class ProofVault:
    """A registry for mathematical claims.

    Examples
    --------
    >>> from spectral_sandbox import ProofVault
    >>> vault = ProofVault()
    >>> vault.register("isep_identity", "The eigenprojectors of H span I.")
    >>> vault.verify("isep_identity", description="Checked on 4×4 GUE sample", data={"error": 1e-15})
    >>> vault["isep_identity"].status
    <ClaimStatus.VERIFIED: 'verified'>
    """

    def __init__(self) -> None:
        self._claims: dict[str, Claim] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        name: str,
        statement: str,
        status: ClaimStatus | str = ClaimStatus.CONJECTURE,
    ) -> Claim:
        """Register a new claim.

        Parameters
        ----------
        name : str
            Unique identifier for the claim.
        statement : str
            Human-readable mathematical statement.
        status : ClaimStatus or str, optional
            Initial status.  Defaults to ``CONJECTURE``.

        Returns
        -------
        Claim
            The newly registered claim.

        Raises
        ------
        ValueError
            If *name* is already registered.
        """
        if name in self._claims:
            raise ValueError(f"Claim '{name}' is already registered.")
        claim = Claim(name=name, statement=statement, status=ClaimStatus(status))
        self._claims[name] = claim
        return claim

    def __getitem__(self, name: str) -> Claim:
        return self._claims[name]

    def __contains__(self, name: str) -> bool:
        return name in self._claims

    def __len__(self) -> int:
        return len(self._claims)

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def verify(self, name: str, description: str = "Numerically verified", data: Any = None) -> None:
        """Verify an existing claim by name."""
        self._claims[name].verify(description, data)

    def refute(self, name: str, description: str = "Counter-example found", data: Any = None) -> None:
        """Refute an existing claim by name."""
        self._claims[name].refute(description, data)

    def summary(self) -> dict[str, int]:
        """Return a status-count summary.

        Returns
        -------
        dict
            Mapping of status string → count.
        """
        counts: dict[str, int] = {s.value: 0 for s in ClaimStatus}
        for claim in self._claims.values():
            counts[claim.status.value] += 1
        return counts

    def list_claims(self, status: ClaimStatus | str | None = None) -> list[Claim]:
        """Return all claims, optionally filtered by *status*."""
        claims = list(self._claims.values())
        if status is not None:
            target = ClaimStatus(status)
            claims = [c for c in claims if c.status == target]
        return claims

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_json(self, indent: int = 2) -> str:
        """Serialise the vault to a JSON string."""
        return json.dumps([c.to_dict() for c in self._claims.values()], indent=indent)

    @classmethod
    def from_json(cls, data: str) -> "ProofVault":
        """Deserialise a vault from a JSON string produced by :meth:`to_json`."""
        vault = cls()
        for entry in json.loads(data):
            claim = Claim(
                name=entry["name"],
                statement=entry["statement"],
                status=ClaimStatus(entry["status"]),
                evidence=entry.get("evidence", []),
                created_at=entry.get("created_at", time.time()),
                updated_at=entry.get("updated_at", time.time()),
            )
            vault._claims[claim.name] = claim
        return vault
