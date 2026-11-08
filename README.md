# SDET Automation Pipeline

Testing suite for UI (CURA Healthcare) and API (Swagger Petstore) using Python, Playwright, and Pytest.

## 🚀 Key Features & Architectural Highlights

This repository implements testing patterns to ensure reliability, speed, and strict validation:

* **CI/CD Pipeline:** The GitHub Actions workflow enforces true pass/fail reporting. Tests are never masked (`|| true` is intentionally omitted) to ensure pipeline integrity. Manual triggers (`workflow_dispatch`) are also supported.
* **Smart Session Management:**
    * **Isolated Sessions:** Tests that mutate authentication state (like login/logout) use a fresh browser context (`page`) to prevent flaky test interactions.
    * **Shared Sessions:** Read-only and booking tests share a cached session (`storageState` via the `auth_page` fixture) to dramatically reduce execution time.
* **Safe API Teardown:** API tests utilize a `yield`-based cleanup pipeline. Test data (like created users) is reliably deleted during teardown, even if the primary test assertions fail.
* **Strong Assertions:** Validates native DOM properties (e.g., HTML5 `validationMessage`), specific CSS locators, and strict URL paths. Known demo app limitations (like accepting past dates) are actively tracked using `@pytest.mark.xfail(strict=True)`.
* **Dual Reporting:** Automatically generates Pytest-HTML reports (attached as CI artifacts) and interactive Allure reports (published to GitHub Pages) with automatic failure screenshots.

## 🛠️ Tech Stack

* **Language:** Python 3.11
* **Framework:** Pytest
* **Automation Tool:** Playwright (Sync API)
* **Reporting:** Allure Report, Pytest-HTML
* **CI/CD:** GitHub Actions

## 📦 Project Structure

```text
├── .github/workflows/
│   └── sdt-automation.yml    # CI/CD Pipeline configuration
├── pages/
│   ├── base_page.py          # Base POM class
│   ├── login_page.py         # CURA Login POM
│   └── appointment_page.py   # CURA Appointment POM (with datepicker handling)
├── tests/
│   ├── api/
│   │   └── test_petstore_api.py   # API test scenarios with yield teardown
│   └── ui/
│       └── test_cura_healthcare.py # UI test scenarios (isolated vs shared sessions)
├── .env.example              # Template for environment variables
├── conftest.py               # Global fixtures (auth, API context, reporting hooks)
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## ⚙️ Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ilhamfdh15/kawanlama-sdet-test.git
   cd kawanlama-sdet-test
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies and Playwright browsers:**
   ```bash
   pip install -r requirements.txt
   playwright install --with-deps
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add the following:
   ```env
   CURA_BASE_URL=https://katalon-demo-cura.herokuapp.com
   CURA_USERNAME=John Doe
   CURA_PASSWORD=ThisIsNotAPassword
   ```

## ▶️ Running Tests

**Run all tests (API & UI) with Allure reporting:**
```bash
pytest --alluredir=allure-results
```

**Run only UI tests:**
```bash
pytest tests/ui/
```

**Run only API tests:**
```bash
pytest tests/api/
```

**View Allure Report Locally:**
```bash
allure serve allure-results
```

## 📊 CI/CD and Reporting

Every push or pull request to the `main` or `master` branch triggers the GitHub Actions pipeline.
* **HTML Artifacts:** A standalone HTML report is available for download in the Artifacts section of each GitHub Actions run.