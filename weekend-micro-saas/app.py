#!/usr/bin/env python3
"""
FastAPI micro-SaaS loop — clone of Orion datcxy app.py shape.
Requires: pip install fastapi uvicorn
Edit CONFIG dict, set env vars, run: uvicorn app:app --reload
"""
import os
from typing import Optional

try:
    from fastapi import FastAPI, Header, HTTPException, Request
    from fastapi.responses import HTMLResponse, JSONResponse
except ImportError:
    print("Install: pip install fastapi uvicorn")
    raise

from apikeys import mint_key, verify_key
from stripe_client import is_paid_session

CONFIG = {
    "product_name": "My Micro-SaaS",
    "tagline": "One sentence outcome for your audience.",
    "stripe_checkout_url": os.environ.get("STRIPE_CHECKOUT_URL", "https://buy.stripe.com/YOUR_PLINK"),
    "price_label": "EUR 9 / month",
}

app = FastAPI(title=CONFIG["product_name"])


@app.get("/", response_class=HTMLResponse)
def landing():
    return f"""<!doctype html><html><head><title>{CONFIG['product_name']}</title></head>
<body><h1>{CONFIG['product_name']}</h1><p>{CONFIG['tagline']}</p>
<p><a href="{CONFIG['stripe_checkout_url']}">Subscribe — {CONFIG['price_label']}</a></p></body></html>"""


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/mint")
def api_mint(session_id: str):
    if not is_paid_session(session_id):
        raise HTTPException(402, "payment required")
    return {"api_key": mint_key(session_id)}


@app.get("/api/gated")
def gated(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing key")
    payload = verify_key(authorization[7:])
    if not payload:
        raise HTTPException(403, "invalid key")
    return JSONResponse({"access": "granted", "plan": payload.get("plan")})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
