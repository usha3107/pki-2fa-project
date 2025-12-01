#!/usr/bin/env python3

import sys
from datetime import datetime, timezone
from pathlib import Path

from app.totp_utils import generate_totp_code

# Persistent volume paths (inside Docker)
SEED_PATH = Path("/data/seed.txt")
LOG_PATH = Path("/cron/last_code.txt")

def main():
    try:
        # 1. Check seed exists
        if not SEED_PATH.exists():
            print("Seed not found", file=sys.stderr)
            return

        # 2. Read hex seed
        hex_seed = SEED_PATH.read_text().strip()

        # 3. Generate TOTP
        code = generate_totp_code(hex_seed)

        # 4. Get UTC timestamp
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # 5. Append log message
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a") as f:
            f.write(f"{timestamp} - 2FA Code: {code}\n")

    except Exception as e:
        print("Error in cron script:", e, file=sys.stderr)


if __name__ == "__main__":
    main()
