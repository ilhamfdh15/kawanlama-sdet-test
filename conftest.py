import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AUTH_FILE = ".auth/state.json"

# ==========================================
# UI AUTOMATION FIXTURES (Storage State)
# ==========================================
@pytest.fixture(scope="session")
def authenticated_session(playwright):
    """
    Creates the storage_state JSON file once per test session.
    Uses the native 'playwright' fixture to avoid event loop crashes.
    """
    os.makedirs(".auth", exist_ok=True)

    # Launch an isolated browser just for creating the auth state
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    base_url = os.getenv("CURA_BASE_URL", "https://katalon-demo-cura.herokuapp.com/")

    page.goto(base_url)
    page.locator("#btn-make-appointment").click()
    page.locator("#txt-username").fill(os.getenv("CURA_USERNAME", "John Doe"))
    page.locator("#txt-password").fill(os.getenv("CURA_PASSWORD", "ThisIsNotAPassword"))
    page.locator("#btn-login").click()

    page.wait_for_url("**/#appointment")

    # Save the session cookies and close the setup browser
    context.storage_state(path=AUTH_FILE)
    browser.close()

    return AUTH_FILE

@pytest.fixture
def auth_page(browser, authenticated_session):
    """
    Yields an authenticated page using the storage_state.
    Bypasses the UI login entirely.
    """
    context = browser.new_context(storage_state=authenticated_session)
    page = context.new_page()

    base_url = os.getenv("CURA_BASE_URL", "https://katalon-demo-cura.herokuapp.com/")
    page.goto(f"{base_url}#appointment")

    yield page
    context.close()

# ==========================================
# API AUTOMATION FIXTURES
# ==========================================
@pytest.fixture(scope="session")
def api_context(playwright):
    """Provides a pristine Playwright APIRequestContext for API testing."""
    request_context = playwright.request.new_context(
        base_url="https://petstore.swagger.io/v2/"
    )
    yield request_context
    request_context.dispose()

# ==========================================
# REPORTING HOOKS
# ==========================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures screenshots on UI test failures and embeds them in the HTML report."""
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        if report.failed:
            page = item.funcargs.get("page") or item.funcargs.get("auth_page")
            if page:
                screenshot = page.screenshot()
                import base64
                encoded = base64.b64encode(screenshot).decode()
                html = f'<div><img src="data:image/png;base64,{encoded}" style="width:600px;height:auto;" onclick="window.open(this.src)" align="right"/></div>'
                extras.append(pytest_html.extras.html(html))
        report.extras = extras