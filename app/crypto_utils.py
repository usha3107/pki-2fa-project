import base64
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

STUDENT_PRIVATE_KEY_PATH = Path("student_private.pem")
STUDENT_PUBLIC_KEY_PATH = Path("student_public.pem")
INSTRUCTOR_PUBLIC_KEY_PATH = Path("instructor_public.pem")

def load_private_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_private_key(data, password=None)

def load_public_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_public_key(data)

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    try:
        ciphertext = base64.b64decode(encrypted_seed_b64)
    except Exception as e:
        raise ValueError("Invalid base64") from e

    try:
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise ValueError("RSA decryption failed") from e

    seed = plaintext.decode("utf-8").strip()
    if len(seed) != 64:
        raise ValueError("Seed must be 64 characters")
    if any(c not in "0123456789abcdef" for c in seed):
        raise ValueError("Seed must be lowercase hex")

    return seed
