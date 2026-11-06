# Kawan Lama Group SDET Technical Test

This repository contains a professional UI and API automation framework built using Python, Playwright, and Pytest, implementing the Page Object Model (POM) design pattern.

## Framework Architecture

- UI Automation: CURA Healthcare demo application (pytest + Playwright + POM).
- API Automation: Swagger Petstore REST API (APIRequestContext with dynamic UUID user management).
- Data-Driven Testing: Parametrized test execution using pytest.mark.parametrize.
- Reporting: Automated HTML test report generation.

## Setup Instructions

1. Clone the Repository:
   git clone <your-repository-url>
   cd katalon-sdet-test

2. Create and Activate a Virtual Environment:
   python3 -m venv .venv
   source .venv/bin/activate

3. Upgrade Pip & Install Dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt

4. Install Playwright Browsers:
   playwright install chromium

## Running the Test Suite

Make sure your virtual environment is active (source .venv/bin/activate), then run the tests using the following commands:

- Run All Tests (UI & API):
  pytest -v tests/

- Run Only API Tests:
  pytest -v tests/api/test_petstore_api.py

- Run Only UI Tests:
  pytest -v tests/ui/test_cura_healthcare.py

## Generating Test Reports

To execute the test suite and automatically generate a shareable, interactive HTML test summary report:
pytest --html=report.html --self-contained-html

Once completed, open the generated report.html file in any web browser to view detailed execution statuses for every test case variant.