import pytest
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="session")
def api_context(playwright):
    base_url = os.getenv("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2/")
    request_context = playwright.request.new_context(base_url=base_url)
    yield request_context
    request_context.dispose()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    # Check if the test is in the 'call' phase AND it failed
    if report.when == "call" and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                # Capture screenshot on failure
                screenshot_bytes = page.screenshot()
                encoded_img = base64.b64encode(screenshot_bytes).decode("utf-8")
                html_content = (
                    f'<div>'
                    f'<img src="data:image/png;base64,{encoded_img}" alt="screenshot" '
                    f'style="width:400px; height:auto; border:1px solid #ccc; cursor:pointer;" '
                    f'onclick="window.open(this.src)" />'
                    f'</div>'
                )
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html is not None:
                    extras.append(pytest_html.extras.html(html_content))
            except Exception as e:
                print(f"Failed to capture screenshot on failure: {e}")

    report.extras = extras