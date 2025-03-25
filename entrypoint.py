import os
import sys
import requests

def get_token(base_url, client_id, client_secret):
    response = requests.post(
        f"{base_url}/api/oauth/token",
        json={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
    )
    if response.status_code != 200:
        print(f"::error ::Auth failed at {base_url}: {response.status_code} {response.text}")
        sys.exit(1)
    return response.json().get("access_token")

def get_version(base_url, token):
    response = requests.get(
        f"{base_url}/api/_info/config",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        print(f"::error ::Failed to get version from {base_url}: {response.status_code} {response.text}")
        sys.exit(1)
    return response.json().get("version")

def parse_version(version_str):
    # Normalize version string to at least 3 parts
    parts = version_str.strip().split(".")
    while len(parts) < 4:
        parts.append("0")
    return tuple(map(int, parts[:4]))  # (major, minor, patch, optional)

def main():
    prod_url = os.getenv("PROD_URL")
    test_url = os.getenv("TEST_URL")
    prod_id = os.getenv("PROD_CLIENT_ID")
    prod_secret = os.getenv("PROD_CLIENT_SECRET")
    test_id = os.getenv("TEST_CLIENT_ID")
    test_secret = os.getenv("TEST_CLIENT_SECRET")

    if not all([prod_url, test_url, prod_id, prod_secret, test_id, test_secret]):
        print("::error ::Missing one or more required environment variables.")
        sys.exit(1)

    prod_token = get_token(prod_url, prod_id, prod_secret)
    test_token = get_token(test_url, test_id, test_secret)

    prod_version_str = get_version(prod_url, prod_token)
    test_version_str = get_version(test_url, test_token)

    print(f"Production version: {prod_version_str}")
    print(f"Test version: {test_version_str}")

    *_, prod_major, prod_minor, prod_patch = parse_version(prod_version_str)
    *_, test_major, test_minor, test_patch = parse_version(test_version_str)

    if (prod_major != test_major) or (prod_minor != test_minor):
        print(f"::error ::Incompatible Shopware versions. Major/minor mismatch: Prod={prod_major}.{prod_minor}, Test={test_major}.{test_minor}. Aborting.")
        sys.exit(1)

    if prod_patch != test_patch:
        print(f"::warning ::Patch version differs. Prod={prod_patch}, Test={test_patch}. Proceed with caution.")
    else:
        print("::notice ::Versions match exactly.")

    print("Versions are compatible. Safe to continue.")

if __name__ == "__main__":
    main()
