# Kawan Lama Group SDET Technical Test
This repository contains the UI and API automation solutions using Python and Playwright.

## Framework Architecture
- **Page Object Model (POM)** for UI maintainability.
- **Data-Driven Testing** utilizing `pytest.mark.parametrize`.
- **Unified Request Context** for API testing via Playwright.

## Setup Instructions
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium