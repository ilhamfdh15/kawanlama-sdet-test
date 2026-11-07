import pytest
import os
from datetime import datetime, timedelta
from playwright.sync_api import expect
from dotenv import load_dotenv
from pages.login_page import LoginPage
from pages.appointment_page import AppointmentPage

load_dotenv()

# Fetch credentials securely from .env
USERNAME = os.getenv("CURA_USERNAME", "John Doe")
PASSWORD = os.getenv("CURA_PASSWORD", "ThisIsNotAPassword")
BASE_URL = os.getenv("CURA_BASE_URL", "https://katalon-demo-cura.herokuapp.com")

@pytest.fixture
def auth_page(page):
    """
    Setup fixture to provide a pre-authenticated browser state.
    Eliminates repetitive login code and conditional state checks in tests.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(USERNAME, PASSWORD)

    # Ensure login was successful before yielding to the test
    expect(page).to_have_url(f"{BASE_URL}/#appointment")
    return page


# ==========================================
# TC 1 & TC 2: Login Scenarios
# ==========================================
LOGIN_DATA = [
    (USERNAME, PASSWORD, True),               # TC 1: Valid Login
    ("InvalidUser", "WrongPassword", False)   # TC 2: Invalid Login
]

@pytest.mark.parametrize("username, password, is_valid", LOGIN_DATA)
def test_login_variants(page, username, password, is_valid):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)

    if is_valid:
        expect(page, "Login failed").to_have_url(f"{BASE_URL}/#appointment")
        login_page.logout()
    else:
        expect(page).to_have_url(f"{BASE_URL}/profile.php#login")
        expect(page.locator(".text-danger"), "Login validation failed").to_be_visible()


# ==========================================
# TC 3: Successful Logout
# ==========================================
def test_successful_logout(auth_page):
    """Uses auth_page to start in a logged-in state, skipping manual setup."""
    login_page = LoginPage(auth_page)
    login_page.logout()

    expect(auth_page, "Logout failed: User session was not terminated.").to_have_url(f"{BASE_URL}/")


# ==========================================
# TC 4: Make Appointment with all valid data
# ==========================================
APPOINTMENT_DATA = [
    ("Hongkong CURA Healthcare Center", "30/11/2026", "Routine checkup"),
    ("Tokyo CURA Healthcare Center", "25/12/2026", "Follow-up consultation"),
    ("Seoul CURA Healthcare Center", "15/01/2027", "Annual medical checkup")
]

@pytest.mark.parametrize("facility, date, comment", APPOINTMENT_DATA)
def test_make_appointment_data_driven(auth_page, facility, date, comment):
    appointment_page = AppointmentPage(auth_page)
    appointment_page.book_appointment(facility, date, comment)

    expect(appointment_page.confirmation_header, "Appointment booking failed.").to_be_visible()


def test_appointment_history_redirection(auth_page):
    auth_page.locator("#menu-toggle").click()
    auth_page.locator("text=History").click()

    expect(auth_page, "Navigation error: User was not redirected.").to_have_url(f"{BASE_URL}/history.php#history")


# ==========================================
# TC 5: Make Appointment without mandatory Visit Date
# ==========================================
def test_make_appointment_empty_date(auth_page):
    appointment_page = AppointmentPage(auth_page)

    # Fill all fields except Visit Date
    appointment_page.facility_dropdown.select_option("Seoul CURA Healthcare Center")
    appointment_page.medicaid_radio.check()
    appointment_page.comment_input.fill("Testing empty date validation")
    appointment_page.book_btn.click()

    # HTML5 validation blocks the submission
    expect(appointment_page.confirmation_header, "HTML5 Validation Bypass.").not_to_be_visible()

    # Verify the element is strictly required by the DOM
    is_required = auth_page.locator("#txt_visit_date").evaluate("el => el.required")
    assert is_required is True, "DOM Validation Error: Missing 'required' HTML attribute."


# ==========================================
# TC 6: Attempting to book an appointment with a past date
# ==========================================
def test_make_appointment_past_date(auth_page):
    appointment_page = AppointmentPage(auth_page)

    # Dynamically calculate yesterday's date
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")

    # Input the dynamic past date
    appointment_page.book_appointment("Hongkong CURA Healthcare Center", yesterday, "Past date test")

    # The expected result is that the appointment should be invalid as it is outdated.
    custom_error_msg = f"APPLICATION BUG: System successfully booked using past date ({yesterday}). Past dates should be blocked by business rules."

    expect(appointment_page.confirmation_header, custom_error_msg).not_to_be_visible()