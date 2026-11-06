import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.appointment_page import AppointmentPage

LOGIN_DATA = [
    ("John Doe", "ThisIsNotAPassword", True),
    ("InvalidUser", "WrongPassword", False)
]

# Expanded appointment data including different facilities and comments
APPOINTMENT_DATA = [
    ("Hongkong CURA Healthcare Center", "30/11/2026", "Routine checkup"),
    ("Tokyo CURA Healthcare Center", "25/12/2026", "Follow-up consultation"),
    ("Seoul CURA Healthcare Center", "15/01/2027", "Annual medical checkup")
]

@pytest.mark.parametrize("username, password, is_valid", LOGIN_DATA)
def test_login_variants(page, username, password, is_valid):
    login_page = LoginPage(page)
    login_page.login(username, password)

    if is_valid:
        assert page.url == "https://katalon-demo-cura.herokuapp.com/#appointment"
        page.locator("#menu-toggle").click()
        page.locator("text=Logout").click()
    else:
        assert page.url == "https://katalon-demo-cura.herokuapp.com/profile.php#login"
        assert page.locator(".text-danger").is_visible()

@pytest.mark.parametrize("facility, date, comment", APPOINTMENT_DATA)
def test_make_appointment_data_driven(page, facility, date, comment):
    login_page = LoginPage(page)
    appointment_page = AppointmentPage(page)

    if "profile.php#login" in page.url or page.locator("#txt-username").is_visible():
        login_page.login("John Doe", "ThisIsNotAPassword")

    appointment_page.book_appointment(facility, date, comment)
    expect(appointment_page.confirmation_header).to_be_visible()

def test_appointment_history_redirection(page):
    login_page = LoginPage(page)
    login_page.login("John Doe", "ThisIsNotAPassword")

    # Navigate to History via sidebar menu
    page.locator("#menu-toggle").click()
    page.locator("text=History").click()

    assert "history.php#history" in page.url