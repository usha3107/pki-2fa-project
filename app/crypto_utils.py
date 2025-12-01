import base64
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Paths to keys (in Docker these will be under /app/)
STUDENT_PRIVATE_KEY_PATH = Path("student_private.pem")
STUDENT_PUBLIC_KEY_PATH = Path("student_public.pem")
INSTRUCTOR_PUBLIC_KEY_PATH = Path("instructor_public.pem")


def load_private_key(path: Path):
    key_data = path.read_bytes()
    return serialization.load_pem_private_key(key_data, password=None)


def load_public_key(path: Path):
    key_data = path.read_bytes()
    return serialization.load_pem_public_key(key_data)


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64 seed using RSA/OAEP + SHA256.
    Returns 64-character hex seed.
    """

    ciphertext = base64.b64decode(encrypted_seed_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    seed = plaintext.decode("utf-8").strip()

    # Validate it is 64-char lowercase hex
    if len(seed) != 64:
        raise ValueError("Seed must be exactly 64 chars")

    if not all(c in "0123456789abcdef" for c in seed):
        raise ValueError("Seed must be lowercase hex")

    return seed
