import pytest
from datetime import datetime, timedelta
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.appointment_page import AppointmentPage

# ==========================================
# TC 1 & TC 2: Login Scenarios
# ==========================================
LOGIN_DATA = [
    ("John Doe", "ThisIsNotAPassword", True),   # TC 1: Valid Login
    ("InvalidUser", "WrongPassword", False)     # TC 2: Invalid Login
]

@pytest.mark.parametrize("username, password, is_valid", LOGIN_DATA)
def test_login_variants(page, username, password, is_valid):
    login_page = LoginPage(page)
    login_page.login(username, password)

    if is_valid:
        # TC 1 Assertion
        expect(page, "Login failed: User was not redirected to the appointment page after entering valid credentials.").to_have_url("https://katalon-demo-cura.herokuapp.com/#appointment")

        page.locator("#menu-toggle").click()
        page.locator("text=Logout").click()
    else:
        # TC 2 Assertion
        expect(page, "Security flow error: Invalid credentials bypassed the login screen.").to_have_url("https://katalon-demo-cura.herokuapp.com/profile.php#login")

        expect(page.locator(".text-danger"), "Login validation failed: The red 'Login failed!' error message was not displayed to the user.").to_be_visible()


# ==========================================
# TC 3: Successful Logout
# ==========================================
def test_successful_logout(page):
    login_page = LoginPage(page)

    if "profile.php#login" in page.url or page.locator("#txt-username").is_visible():
        login_page.login("John Doe", "ThisIsNotAPassword")

    # Click the menu toggle and click 'Logout'
    page.locator("#menu-toggle").click()
    page.locator("text=Logout").click()

    # Session is completely terminated and redirected to Home page
    expect(page, "Logout failed: User session was not terminated and redirected to the homepage.").to_have_url("https://katalon-demo-cura.herokuapp.com/")


# ==========================================
# TC 4: Make Appointment with all valid data (Data-Driven)
# ==========================================
APPOINTMENT_DATA = [
    ("Hongkong CURA Healthcare Center", "30/11/2026", "Routine checkup"),
    ("Tokyo CURA Healthcare Center", "25/12/2026", "Follow-up consultation"),
    ("Seoul CURA Healthcare Center", "15/01/2027", "Annual medical checkup")
]

@pytest.mark.parametrize("facility, date, comment", APPOINTMENT_DATA)
def test_make_appointment_data_driven(page, facility, date, comment):
    login_page = LoginPage(page)
    appointment_page = AppointmentPage(page)

    if "profile.php#login" in page.url or page.locator("#txt-username").is_visible():
        login_page.login("John Doe", "ThisIsNotAPassword")

    appointment_page.book_appointment(facility, date, comment)

    expect(appointment_page.confirmation_header, "Appointment booking failed: The appointment confirmation summary was not displayed after submitting valid data.").to_be_visible()

def test_appointment_history_redirection(page):
    login_page = LoginPage(page)

    if "profile.php#login" in page.url or page.locator("#txt-username").is_visible():
        login_page.login("John Doe", "ThisIsNotAPassword")

    page.locator("#menu-toggle").click()
    page.locator("text=History").click()

    expect(page, "Navigation error: User was not redirected to the History page.").to_have_url("https://katalon-demo-cura.herokuapp.com/history.php#history")


# ==========================================
# TC 5: Make Appointment without mandatory Visit Date
# ==========================================
def test_make_appointment_empty_date(page):
    login_page = LoginPage(page)
    appointment_page = AppointmentPage(page)

    if "profile.php#login" in page.url or page.locator("#txt-username").is_visible():
        login_page.login("John Doe", "ThisIsNotAPassword")

    # Fill all fields except Visit Date
    appointment_page.facility_dropdown.select_option("Seoul CURA Healthcare Center")
    appointment_page.medicaid_radio.check()
    appointment_page.comment_input.fill("Testing empty date validation")
    appointment_page.book_btn.click()

    # HTML5 validation blocks the submission
    expect(appointment_page.confirmation_header, "HTML5 Validation Bypass: The system allowed booking an appointment without a mandatory visit date.").not_to_be_visible()

    # Verify the element is strictly required by the DOM
    is_required = page.locator("#txt_visit_date").evaluate("el => el.required")
    assert is_required is True, "DOM Validation Error: The visit date input field is missing the strict 'required' HTML attribute."


# ==========================================
# TC 6: Attempting to book an appointment with a past date
# ==========================================
def test_make_appointment_past_date(page):
    login_page = LoginPage(page)
    appointment_page = AppointmentPage(page)

    if "profile.php#login" in page.url or page.locator("#txt-username").is_visible():
        login_page.login("John Doe", "ThisIsNotAPassword")

    # Dynamically calculate yesterday's date in DD/MM/YYYY format
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")

    # Input the dynamic past date
    appointment_page.book_appointment("Hongkong CURA Healthcare Center", yesterday, "Past date test")

    # The expected result is that the appointment should be invalid as it is outdated.
    custom_error_msg = f"APPLICATION BUG: The system successfully booked an appointment using a past date ({yesterday}). Past dates should be blocked."

    expect(appointment_page.confirmation_header, custom_error_msg).not_to_be_visible()