import pytest

@pytest.fixture(scope="session")
def api_context(playwright):
    # Notice the trailing slash here
    request_context = playwright.request.new_context(base_url="https://petstore.swagger.io/v2/")
    yield request_context
    request_context.dispose()

@pytest.fixture
def page(context):
    page = context.new_page()
    page.goto("https://katalon-demo-cura.herokuapp.com/profile.php#login")
    yield page
    page.close()