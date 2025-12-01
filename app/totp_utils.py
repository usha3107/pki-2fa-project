# app/totp_utils.py
import re
import base64
import pyotp
import time

HEX_RE = re.compile(r'^[0-9a-fA-F]+$')

def hex_to_base32(hex_seed: str) -> str:
    if not isinstance(hex_seed, str):
        raise TypeError("hex_seed must be a string")
    # strip whitespace/newlines, remove optional 0x prefix
    s = hex_seed.strip()
    if s.startswith("0x") or s.startswith("0X"):
        s = s[2:]
    # ensure only hex chars and even length
    if not s:
        raise ValueError("empty hex seed")
    if not HEX_RE.fullmatch(s):
        raise ValueError("hex_seed contains non-hex characters")
    if len(s) % 2 != 0:
        raise ValueError("hex_seed must have an even number of hex characters")
    b = bytes.fromhex(s)
    # base32 encode and decode to ascii, remove padding (pyotp tolerates without '=' too)
    b32 = base64.b32encode(b).decode('ascii').rstrip('=')
    return b32

def generate_totp_code(hex_seed: str, digits: int = 6, period: int = 30) -> str:
    secret_b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(secret_b32, digits=digits, interval=period)
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, digits: int = 6, period: int = 30) -> bool:
    secret_b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(secret_b32, digits=digits, interval=period)
    # allow small window if required: window=1 means ±1 interval
    return totp.verify(code, valid_window=1)

def seconds_remaining_in_period(period: int = 30) -> int:
    now = int(time.time())
    return period - (now % period)
