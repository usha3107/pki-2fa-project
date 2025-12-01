# scripts/test_totp.py
from pathlib import Path
from app.totp_utils import generate_totp_code, verify_totp_code, seconds_remaining_in_period

if __name__ == "__main__":
    # Example valid seed (only for testing) — replace with your decrypted hex from test_decrypt.py
    hex_seed = "4f2a1c9b3e6d7a8b9c0d1e2f3a4b5c6d"
    code = generate_totp_code(hex_seed)
    print("Code:", code, "valid_for:", seconds_remaining_in_period())
    print("Verify:", verify_totp_code(hex_seed, code))
