from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.crypto_utils import load_private_key, decrypt_seed, STUDENT_PRIVATE_KEY_PATH
from app.totp_utils import generate_totp_code, verify_totp_code, seconds_remaining_in_period

app = FastAPI()
SEED_PATH = Path("data/seed.txt")  # local path; Docker will override to /data

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(body: DecryptSeedRequest):
    try:
        priv = load_private_key(STUDENT_PRIVATE_KEY_PATH)
        hex_seed = decrypt_seed(body.encrypted_seed, priv)
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

    try:
        SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
        SEED_PATH.write_text(hex_seed)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to store seed")

    return {"status": "ok"}

@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    try:
        hex_seed = SEED_PATH.read_text().strip()
        code = generate_totp_code(hex_seed)
        valid_for = seconds_remaining_in_period()
        return {"code": code, "valid_for": valid_for}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate TOTP")

@app.post("/verify-2fa")
def verify_2fa(body: Verify2FARequest):
    if not body.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not SEED_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    try:
        hex_seed = SEED_PATH.read_text().strip()
        valid = verify_totp_code(hex_seed, body.code.strip(), valid_window=1)
        return {"valid": bool(valid)}
    except Exception:
        raise HTTPException(status_code=500, detail="Verification failed")
