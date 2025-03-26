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
    parts = version_str.strip().split(".")
    while len(parts) < 4:
        parts.append("0")
    return tuple(map(int, parts[:4]))  # shopware, major, minor, patch

def compare_versions(prod, test, strategy):
    _, prod_major, prod_minor, prod_patch = prod
    _, test_major, test_minor, test_patch = test

    if strategy == "exact":
        if (prod_major, prod_minor, prod_patch) != (test_major, test_minor, test_patch):
            print(f"::error ::Version mismatch (exact): Prod={prod_major}.{prod_minor}.{prod_patch}, Test={test_major}.{test_minor}.{test_patch}")
            sys.exit(1)

    elif strategy == "minor":
        if (prod_major != test_major) or (prod_minor != test_minor):
            print(f"::error ::Version mismatch (minor): Prod={prod_major}.{prod_minor}, Test={test_major}.{test_minor}")
            sys.exit(1)
        if prod_patch != test_patch:
            print(f"::warning ::Patch version differs: Prod={prod_patch}, Test={test_patch}")

    elif strategy == "major":
        if prod_major != test_major:
            print(f"::error ::Version mismatch (major): Prod={prod_major}, Test={test_major}")
            sys.exit(1)
        if prod_minor != test_minor:
            print(f"::notice ::Minor version differs: Prod={prod_minor}, Test={test_minor}")
        if prod_patch != test_patch:
            print(f"::notice ::Patch version differs: Prod={prod_patch}, Test={test_patch}")

    else:  # default
        if (prod_major != test_major) or (prod_minor != test_minor):
            print(f"::error ::Incompatible Shopware versions: Prod={prod_major}.{prod_minor}, Test={test_major}.{test_minor}")
            sys.exit(1)
        if prod_patch != test_patch:
            print(f"::warning ::Patch version differs: Prod={prod_patch}, Test={test_patch}")
        else:
            print("::notice ::Versions match exactly.")

    print("Versions are compatible.")

def main():
    prod_url = os.getenv("PROD_URL")
    test_url = os.getenv("TEST_URL")
    prod_id = os.getenv("PROD_CLIENT_ID")
    prod_secret = os.getenv("PROD_CLIENT_SECRET")
    test_id = os.getenv("TEST_CLIENT_ID")
    test_secret = os.getenv("TEST_CLIENT_SECRET")
    fail_on = os.getenv("FAIL_ON", "default").lower()

    if fail_on not in {"default", "exact", "minor", "major"}:
        print(f"::error ::Invalid FAIL_ON value: {fail_on}")
        sys.exit(1)

    if not all([prod_url, test_url, prod_id, prod_secret, test_id, test_secret]):
        print("::error ::Missing one or more required environment variables.")
        sys.exit(1)

    prod_token = get_token(prod_url, prod_id, prod_secret)
    test_token = get_token(test_url, test_id, test_secret)

    prod_version = parse_version(get_version(prod_url, prod_token))
    test_version = parse_version(get_version(test_url, test_token))

    print(f"Production version: {'.'.join(map(str, prod_version[:4]))}")
    print(f"Test version: {'.'.join(map(str, test_version[:4]))}")

    compare_versions(prod_version, test_version, fail_on)

if __name__ == "__main__":
    main()
