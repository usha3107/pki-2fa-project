import requests
from pathlib import Path

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

STUDENT_ID = "YOUR_STUDENT_ID"
GITHUB_REPO_URL = "https://github.com/yourusername/pki-2fa-project"  # exact URL

def request_seed(student_id: str, github_repo_url: str, api_url: str = API_URL):
    public_pem = Path("student_public.pem").read_text()

    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_pem
    }

    resp = requests.post(api_url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "success":
        raise RuntimeError(f"API error: {data}")

    encrypted_seed = data["encrypted_seed"]
    Path("encrypted_seed.txt").write_text(encrypted_seed)
    print("Saved encrypted_seed.txt")

if __name__ == "__main__":
    request_seed(STUDENT_ID, GITHUB_REPO_URL)
