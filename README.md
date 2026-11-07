# Kawan Lama Group SDET Technical Test

This repository contains an enterprise-grade UI and API automation framework built using **Python**, **Playwright**, and **Pytest**, implementing the **Page Object Model (POM)** design pattern.

## Enterprise-Grade Enhancements

- **CI/CD Integrated:** Automated test execution via GitHub Actions on every push/PR, with HTML reports, Allure results uploaded as build artifacts, and Playwright binaries cached for speed.
- **Session State Management:** Utilizes Playwright's `storageState` to cache authentication cookies, bypassing repetitive UI logins for massive execution speed gains.
- **Dual Executive Reporting:** Generates both `pytest-html` self-contained summaries and interactive **Allure Reports** complete with step-by-step traces and attached failure screenshots.
- **Secure Configuration:** Environment variables (`.env` & `python-dotenv`) used to abstract hardcoded credentials and base URLs.
- **Atomic API Design:** API tests utilize dynamic UUID generation and `yield` teardowns to ensure zero test interdependency and prevent database bloat.
- **Visual Reporting:** Automatically captures and embeds Base64 screenshots for all UI tests directly into both HTML and Allure reports upon failure/success.
- **Robust Assertions:** Utilizes Playwright's built-in `expect` for auto-waiting to prevent race conditions.
- **Cross-Browser Ready:** Natively supports execution across Chromium, Firefox, and WebKit.

## Test Coverage

### UI Automation (CURA Healthcare)
1. **TC 1:** Successful Login with valid credentials.
2. **TC 2:** Unsuccessful Login with invalid credentials (asserting error messages).
3. **TC 3:** Successful Logout and session termination.
4. **TC 4:** Make Appointment with valid data (parameterized for multiple facilities).
5. **TC 5:** Make Appointment without mandatory Visit Date (HTML5 validation check).
6. **TC 6:** Attempting to book an appointment with a past date (dynamic boundary test evaluating business rules).

### API Automation (Swagger Petstore)
1. **Create User:** Validates payload ingestion and 200 OK response.
2. **Get User:** Validates data retrieval matching injected state.
3. **Update User:** Validates PUT operations with dynamic payload modification.
4. **Delete User:** Validates explicit resource removal.
5. **Authentication:** Validates stateless login and logout token generation endpoints.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ilhamfdh15/kawanlama-sdet-test.git
cd kawanlama-sdet-test
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Upgrade Pip & Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```bash
playwright install --with-deps
```

## Running the Test Suite
Make sure your virtual environment is active (`source .venv/bin/activate`), then run the tests using the following commands:

- **Run All Tests (UI & API):**
  ```bash
  pytest -v tests/
  ```

- **Run Only API Tests:**
  ```bash
  pytest -v tests/api/test_petstore_api.py
  ```

- **Run Only UI Tests:**
  ```bash
  pytest -v tests/ui/test_cura_healthcare.py
  ```

- **Run Cross-Browser Tests:**
  ```bash
  pytest --browser chromium --browser webkit tests/ui/
  ```

## Generating Test Reports with Embedded Screenshots
To execute the test suite and automatically generate a shareable HTML test summary report alongside raw metrics for Allure:
```bash
pytest --html=report.html --self-contained-html --alluredir=allure-results
```

## 📊 Test Execution Metrics & Reporting

The framework generates a rich, self-contained HTML report using `pytest-html` alongside raw metrics for the **Allure Framework**, capturing failure screenshots in both formats.

### Suite Breakdown

| Module | Total Tests | Passed | Expected Failures | Core Coverage Areas |
| :--- | :---: | :---: | :---: | :--- |
| **UI Automation (Cura)** | 9 | 8 | 1 | Data-driven login variants, Appointment CRUD, History routing, Negative date validation |
| **API Automation (Petstore)** | 7 | 7 | 0 | Atomic user generation, Authentication state, Data updates, Isolated teardown |
| **Total Pipeline** | **16** | **15** | **1** | |

> **Note on Expected Failure:** The single UI failure (`test_make_appointment_past_date`) is a deliberately engineered negative test. It validates application boundaries and successfully catches a business logic bug where the system improperly accepts historical dates for future appointments.

## Viewing Test Reports

### Pytest-HTML Report:
Open the standalone HTML file in any web browser to view your test results with embedded Base64 failure screenshots:
```bash
open report.html
```

### Allure Interactive Dashboard:
Compile and serve the rich Allure results dashboard locally (requires Allure command-line tool / `brew install allure`):
```bash
allure serve allure-results
```