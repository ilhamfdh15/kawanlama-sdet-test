import pytest
import base64

@pytest.fixture(scope="session")
def api_context(playwright):
    request_context = playwright.request.new_context(base_url="https://petstore.swagger.io/v2/")
    yield request_context
    request_context.dispose()

@pytest.fixture
def page(context):
    page = context.new_page()
    page.goto("https://katalon-demo-cura.herokuapp.com/profile.php#login")
    yield page
    page.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    # We only want to take a screenshot at the end of the actual test execution (not setup/teardown)
    if report.when == "call":
        # Check if this is a UI test that uses the 'page' fixture
        if "page" in item.funcargs:
            page = item.funcargs["page"]

            # Capture the screenshot as raw bytes
            screenshot_bytes = page.screenshot()

            # Encode it to Base64 so it can be safely embedded entirely within the single HTML file
            encoded_img = base64.b64encode(screenshot_bytes).decode("utf-8")

            # Create a clickable HTML image element
            html_content = (
                f'<div>'
                f'<img src="data:image/png;base64,{encoded_img}" alt="screenshot" '
                f'style="width:400px; height:auto; border:1px solid #ccc; cursor:pointer;" '
                f'onclick="window.open(this.src)" />'
                f'</div>'
            )

            # Retrieve the pytest-html plugin and attach the HTML block to the report extra section
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html is not None:
                extras.append(pytest_html.extras.html(html_content))

    report.extras = extras