# 🛡️ shopware-version-guard

**Ensure your Shopware test environment matches the production version before importing anonymized data.**

This GitHub Action compares the Shopware version between a production and test environment using integration credentials.  
It is intended to run before importing a production database into a test instance, to prevent version mismatch issues.

---

## ✅ What It Does

- Authenticates to both Shopware instances using **integration credentials**
- Fetches `/api/_info/config` to determine version
- Compares `major.minor.patch` components
- Enforces compatibility based on **major + minor**
- Allows patch version mismatch but with a warning

---

## 🔍 Behavior

| Version Comparison            | Result                                     |
|------------------------------|--------------------------------------------|
| `major` or `minor` mismatch  | ❌ **Fails** the workflow (`exit 1`)        |
| `patch` mismatch only        | ⚠️ **Warning**, but continues               |
| Exact match                  | ✅ **Passes** silently                      |

---

## 🚀 Usage

```yaml
- name: Check Shopware Versions
  uses: sanikapanika/shopware-version-guard@v1
  env:
    PROD_URL: ${{ secrets.SHOPWARE_PROD_URL }}
    PROD_CLIENT_ID: ${{ secrets.SHOPWARE_PROD_CLIENT_ID }}
    PROD_CLIENT_SECRET: ${{ secrets.SHOPWARE_PROD_CLIENT_SECRET }}
    TEST_URL: ${{ secrets.SHOPWARE_TEST_URL }}
    TEST_CLIENT_ID: ${{ secrets.SHOPWARE_TEST_CLIENT_ID }}
    TEST_CLIENT_SECRET: ${{ secrets.SHOPWARE_TEST_CLIENT_SECRET }}
```

---

## 🔐 Required Secrets

| Variable                | Description                                        |
|------------------------|----------------------------------------------------|
| `SHOPWARE_PROD_URL`    | Base URL of your production Shopware instance     |
| `SHOPWARE_PROD_CLIENT_ID` | Integration client ID for production             |
| `SHOPWARE_PROD_CLIENT_SECRET` | Integration client secret for production     |
| `SHOPWARE_TEST_URL`    | Base URL of your test Shopware instance           |
| `SHOPWARE_TEST_CLIENT_ID` | Integration client ID for test                  |
| `SHOPWARE_TEST_CLIENT_SECRET` | Integration client secret for test         |

---

## 🧪 Example Workflow

```yaml
name: Ensure Shopware Versions Match

on:
  workflow_dispatch:

jobs:
  check-versions:
    runs-on: ubuntu-latest
    steps:
      - name: Run Shopware Version Guard
        uses: sanikapanika/shopware-version-guard@v1
        env:
          PROD_URL: ${{ secrets.SHOPWARE_PROD_URL }}
          PROD_CLIENT_ID: ${{ secrets.SHOPWARE_PROD_CLIENT_ID }}
          PROD_CLIENT_SECRET: ${{ secrets.SHOPWARE_PROD_CLIENT_SECRET }}
          TEST_URL: ${{ secrets.SHOPWARE_TEST_URL }}
          TEST_CLIENT_ID: ${{ secrets.SHOPWARE_TEST_CLIENT_ID }}
          TEST_CLIENT_SECRET: ${{ secrets.SHOPWARE_TEST_CLIENT_SECRET }}
```

---

## 📦 Development

This action is implemented in Python and runs via Docker.

```bash
# Run locally for testing
docker build -t shopware-version-guard .
docker run \
  -e PROD_URL=... \
  -e TEST_URL=... \
  -e PROD_CLIENT_ID=... \
  -e PROD_CLIENT_SECRET=... \
  -e TEST_CLIENT_ID=... \
  -e TEST_CLIENT_SECRET=... \
  shopware-version-guard
```

---

## 📄 License

MIT – free to use, improve, or contribute.
