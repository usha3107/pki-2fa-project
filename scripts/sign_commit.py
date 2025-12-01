import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json

# Load student private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Load instructor public key
with open("instructor_public.pem", "rb") as f:
    instructor_pub = serialization.load_pem_public_key(f.read())

# Ask for commit hash
commit_hash = input("Enter commit hash: ").strip()

# Step 1: Sign commit hash using student private key
signature = private_key.sign(
    commit_hash.encode(),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Step 2: Encrypt the signature using instructor public key
encrypted_signature = instructor_pub.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Convert to base64
encrypted_b64 = base64.b64encode(encrypted_signature).decode()

print("\nCommit Hash:", commit_hash)
print("Encrypted Signature (Base64):")
print(encrypted_b64)
