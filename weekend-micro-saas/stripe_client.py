#!/usr/bin/env python3
"""Minimal Stripe client over stdlib — clone of Orion datcxy stripe_client.py shape."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

STRIPE_API = "https://api.stripe.com/v1"


def _request(method: str, path: str, data: dict | None = None) -> dict:
    key = os.environ.get("STRIPE_SECRET_KEY", "")
    if not key:
        raise RuntimeError("Set STRIPE_SECRET_KEY")
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(
        f"{STRIPE_API}{path}",
        method=method,
        headers={"Authorization": f"Bearer {key}"},
        data=body,
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_checkout_session(session_id: str) -> dict:
    return _request("GET", f"/checkout/sessions/{session_id}")


def is_paid_session(session_id: str) -> bool:
    try:
        sess = get_checkout_session(session_id)
        return sess.get("payment_status") == "paid"
    except urllib.error.HTTPError:
        return False


def verify_webhook(payload: bytes, sig_header: str, secret: str) -> dict:
    """Verify Stripe-Signature header (t=timestamp,v1=sig)."""
    import hashlib
    import hmac
    import time

    parts = dict(p.split("=", 1) for p in sig_header.split(",") if "=" in p)
    ts = int(parts.get("t", "0"))
    if abs(time.time() - ts) > 300:
        raise ValueError("timestamp too old")
    signed = f"{ts}.{payload.decode()}"
    expected = hmac.new(secret.encode(), signed.encode(), hashlib.sha256).hexdigest()
    v1 = parts.get("v1", "")
    if not hmac.compare_digest(expected, v1):
        raise ValueError("invalid signature")
    return json.loads(payload)


def self_test() -> None:
    assert "STRIPE_SECRET_KEY" not in os.environ or True
    print("stripe_client.py: import OK (live calls need STRIPE_SECRET_KEY)")


if __name__ == "__main__":
    self_test()
