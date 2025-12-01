from pathlib import Path
from app.crypto_utils import load_private_key, decrypt_seed, STUDENT_PRIVATE_KEY_PATH

if __name__ == "__main__":
    enc = Path("encrypted_seed.txt").read_text().strip()
    priv = load_private_key(STUDENT_PRIVATE_KEY_PATH)
    seed = decrypt_seed(enc, priv)
    print("Decrypted seed:", seed)
    print("Length:", len(seed))
