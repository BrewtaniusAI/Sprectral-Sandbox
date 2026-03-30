"""Tests for spectral_sandbox.proofvault"""
import json
import pytest
from spectral_sandbox import ProofVault
from spectral_sandbox.proofvault import Claim, ClaimStatus


def test_register_and_retrieve():
    v = ProofVault()
    v.register("test_claim", "1 + 1 = 2")
    assert "test_claim" in v
    assert v["test_claim"].statement == "1 + 1 = 2"
    assert v["test_claim"].status == ClaimStatus.CONJECTURE


def test_register_duplicate_raises():
    v = ProofVault()
    v.register("dup", "statement A")
    with pytest.raises(ValueError, match="already registered"):
        v.register("dup", "statement B")


def test_verify_claim():
    v = ProofVault()
    v.register("claim_a", "Something is true")
    v.verify("claim_a", description="Checked numerically", data={"error": 1e-14})
    assert v["claim_a"].status == ClaimStatus.VERIFIED
    assert len(v["claim_a"].evidence) == 1


def test_refute_claim():
    v = ProofVault()
    v.register("claim_b", "Something is false")
    v.refute("claim_b", description="Counter-example: n=5")
    assert v["claim_b"].status == ClaimStatus.REFUTED


def test_summary():
    v = ProofVault()
    v.register("c1", "claim 1")
    v.register("c2", "claim 2", status=ClaimStatus.OPEN)
    v.register("c3", "claim 3")
    v.verify("c3")
    s = v.summary()
    assert s["conjecture"] == 1
    assert s["verified"] == 1
    assert s["open"] == 1
    assert s["refuted"] == 0


def test_list_claims_all():
    v = ProofVault()
    v.register("x", "X")
    v.register("y", "Y")
    assert len(v.list_claims()) == 2


def test_list_claims_filtered():
    v = ProofVault()
    v.register("p", "P")
    v.register("q", "Q")
    v.verify("p")
    verified = v.list_claims(status=ClaimStatus.VERIFIED)
    assert len(verified) == 1
    assert verified[0].name == "p"


def test_json_roundtrip():
    v = ProofVault()
    v.register("rh", "All non-trivial zeros of ζ(s) lie on Re(s) = 1/2.",
               status=ClaimStatus.OPEN)
    v.register("isep", "Eigenprojectors of H span I.", status=ClaimStatus.CONJECTURE)
    v.verify("isep", description="Verified on GUE(100)", data={"n": 100})
    payload = v.to_json()
    v2 = ProofVault.from_json(payload)
    assert len(v2) == 2
    assert v2["rh"].status == ClaimStatus.OPEN
    assert v2["isep"].status == ClaimStatus.VERIFIED
    assert v2["isep"].evidence[0]["data"]["n"] == 100


def test_len():
    v = ProofVault()
    assert len(v) == 0
    v.register("a", "A")
    assert len(v) == 1
