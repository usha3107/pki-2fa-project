from app.totp_utils import generate_totp_code, verify_totp_code, seconds_remaining_in_period

if __name__ == "__main__":
    hex_seed = "PUT_YOUR_64_CHAR_DECRYPTED_SEED_HERE"
    code = generate_totp_code(hex_seed)
    print("Code:", code, "valid_for:", seconds_remaining_in_period())
    print("Verify:", verify_totp_code(hex_seed, code))
