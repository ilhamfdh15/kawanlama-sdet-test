import os
import pytest
import allure
from dotenv import load_dotenv

load_dotenv()

AUTH_FILE = ".auth/state.json"
BASE_URL = os.getenv("CURA_BASE_URL", "https://katalon-demo-cura.herokuapp.com").rstrip('/')

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Menyematkan screenshot ke Allure dan HTML saat UI test gagal."""
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("auth_page")
        if page:
            screenshot_bytes = page.screenshot()
            allure.attach(screenshot_bytes, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            if pytest_html:
                import base64
                encoded = base64.b64encode(screenshot_bytes).decode()
                html = f'<div><img src="data:image/png;base64,{encoded}" style="width:600px;height:auto;" align="right"/></div>'
                extras.append(pytest_html.extras.html(html))
    report.extras = extras

@pytest.fixture(scope="session")
def authenticated_session(playwright):
    """Membangun session cookies HANYA sekali dan menyimpannya ke state.json."""
    os.makedirs(".auth", exist_ok=True)
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto(BASE_URL)
    page.locator("#btn-make-appointment").click()
    page.locator("#txt-username").fill(os.getenv("CURA_USERNAME", "John Doe"))
    page.locator("#txt-password").fill(os.getenv("CURA_PASSWORD", "ThisIsNotAPassword"))
    page.locator("#btn-login").click()
    page.wait_for_url("**/#appointment")

    context.storage_state(path=AUTH_FILE)
    browser.close()
    return AUTH_FILE

@pytest.fixture
def auth_page(browser, authenticated_session):
    """Fixture khusus untuk test booking/read-only agar tidak crash dengan test logout."""
    context = browser.new_context(storage_state=authenticated_session)
    page = context.new_page()
    page.goto(f"{BASE_URL}/#appointment")
    yield page
    context.close()

@pytest.fixture(scope="session")
def api_context(playwright):
    """Context terpisah untuk API Testing."""
    request_context = playwright.request.new_context(base_url="https://petstore.swagger.io/v2/")
    yield request_context
    request_context.dispose()