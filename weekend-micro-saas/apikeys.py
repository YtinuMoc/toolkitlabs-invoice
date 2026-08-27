#!/usr/bin/env python3
"""Signed, database-free API keys — clone of Orion datcxy apikeys.py shape."""
import base64
import hashlib
import hmac
import json
import os
import sys
import time

DEFAULT_SECRET = "change-me-in-production-use-os-environ"


def _secret() -> bytes:
    return os.environ.get("API_KEY_SECRET", DEFAULT_SECRET).encode()


def mint_key(customer_id: str, plan: str = "default", ttl_days: int = 365) -> str:
    payload = {
        "sub": customer_id,
        "plan": plan,
        "exp": int(time.time()) + ttl_days * 86400,
    }
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(_secret(), body.encode(), hashlib.sha256).hexdigest()[:32]
    return f"tlk_{body}.{sig}"


def verify_key(key: str) -> dict | None:
    if not key.startswith("tlk_") or "." not in key:
        return None
    body, sig = key[4:].split(".", 1)
    expected = hmac.new(_secret(), body.encode(), hashlib.sha256).hexdigest()[:32]
    if not hmac.compare_digest(sig, expected):
        return None
    pad = "=" * (-len(body) % 4)
    payload = json.loads(base64.urlsafe_b64decode(body + pad))
    if payload.get("exp", 0) < time.time():
        return None
    return payload


def self_test() -> None:
    key = mint_key("test-customer", plan="pro")
    assert verify_key(key) is not None, "minted key must verify"
    assert verify_key("tlk_bad.sig") is None, "bad sig must fail"
    assert verify_key("not-a-key") is None, "malformed must fail"
    print("apikeys.py self-test OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "mint":
        print(mint_key(sys.argv[2] if len(sys.argv) > 2 else "demo"))
    else:
        self_test()
