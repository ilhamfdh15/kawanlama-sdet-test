Markdown
# Kawan Lama Group SDET Technical Test

This repository contains UI and API automation framework built using **Python**, **Playwright**, and **Pytest**, implementing the **Page Object Model (POM)** design pattern.

## Enterprise-Grade Enhancements

- **CI/CD Integrated:** Automated test execution via GitHub Actions on every push/PR, with HTML reports uploaded as build artifacts.
- **Secure Configuration:** Environment variables (`.env` & `python-dotenv`) used to abstract hardcoded credentials and base URLs.
- **Robust Assertions:** Utilizes Playwright's built-in `expect` for auto-waiting to prevent race conditions.
- **Visual Reporting:** Automatically captures and embeds Base64 screenshots for all UI tests directly into the HTML report upon failure/success.
- **Cross-Browser Ready:** Natively supports execution across Chromium, Firefox, and WebKit.

## Test Coverage (UI Scenarios)

The UI automation suite covers all critical positive and boundary test cases for the CURA Healthcare portal:
1. **TC 1:** Successful Login with valid credentials.
2. **TC 2:** Unsuccessful Login with invalid credentials (asserting error messages).
3. **TC 3:** Successful Logout and session termination.
4. **TC 4:** Make Appointment with valid data (parameterized for multiple facilities).
5. **TC 5:** Make Appointment without mandatory Visit Date (HTML5 validation check).
6. **TC 6:** Attempting to book an appointment with a past date (dynamic boundary test).

## Setup Instructions

### 1. Clone the Repository
git clone [https://github.com/ilhamfdh15/kawanlama-sdet-test.git](https://github.com/ilhamfdh15/kawanlama-sdet-test.git)
cd kawanlama-sdet-test

### 2. Create and Activate a Virtual Environment:
   python3 -m venv .venv
   source .venv/bin/activate

### 3. Upgrade Pip & Install Dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt

### 4. Install Playwright Browsers:
   playwright install --with-deps

## Running the Test Suite

Make sure your virtual environment is active (source .venv/bin/activate), then run the tests using the following commands:

- Run All Tests (UI & API):
  pytest -v tests/

- Run Only API Tests:
  pytest -v tests/api/test_petstore_api.py

- Run Only UI Tests:
  pytest -v tests/ui/test_cura_healthcare.py
  
- Run Cross-Browser Tests
pytest --browser chromium --browser webkit tests/ui/

## Generating Test Reports with Embedded Screenshots

To execute the test suite and automatically generate a shareable HTML test summary report (with UI screenshots attached to every test result):
pytest --html=report.html --self-contained-html

Once completed, open the generated report.html file in any web browser. You can click on the image thumbnails attached to each test case to view the full high-resolution screenshot.
