import os
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.appointment_page import AppointmentPage

BASE_URL = os.getenv("CURA_BASE_URL", "https://katalon-demo-cura.herokuapp.com").rstrip('/')
USERNAME = os.getenv("CURA_USERNAME", "John Doe")
PASSWORD = os.getenv("CURA_PASSWORD", "ThisIsNotAPassword")

LOGIN_DATA = [
    (USERNAME, PASSWORD, True),
    ("InvalidUser", "WrongPassword", False)
]

@pytest.mark.parametrize("username, password, is_valid", LOGIN_DATA)
def test_login_variants(page, username, password, is_valid):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)

    if is_valid:
        expect(page).to_have_url(f"{BASE_URL}/#appointment")
    else:
        expect(page).to_have_url(f"{BASE_URL}/profile.php#login")
        expect(page.locator(".text-danger")).to_have_text("Login failed! Please ensure the username and password are valid.")

def test_successful_logout(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(USERNAME, PASSWORD)
    login_page.logout()
    expect(page).to_have_url(f"{BASE_URL}/")


APPOINTMENT_DATA = [
    ("Tokyo CURA Healthcare Center", "25/12/2026", "Follow-up consultation"),
    ("Hongkong CURA Healthcare Center", "30/11/2026", "Routine checkup"),
]

@pytest.mark.parametrize("facility, visit_date, comment", APPOINTMENT_DATA)
def test_make_appointment_data_driven(auth_page, facility, visit_date, comment):
    appointment_page = AppointmentPage(auth_page)

    appointment_page.book_appointment(
        facility=facility,
        visit_date=visit_date,
        comment=comment
    )

    expect(auth_page).to_have_url(f"{BASE_URL}/appointment.php#summary")
    appointment_page.verify_appointment_summary(
        facility=facility,
        visit_date=visit_date,
        comment=comment
    )

def test_appointment_history_redirection(auth_page):
    auth_page.locator("#menu-toggle").click()
    auth_page.locator("a[href='history.php#history']").click()
    expect(auth_page).to_have_url(f"{BASE_URL}/history.php#history")

def test_make_appointment_empty_date(auth_page):
    appointment_page = AppointmentPage(auth_page)

    appointment_page.book_appointment(
        facility="Tokyo CURA Healthcare Center",
        visit_date="",
        comment="Missing date test"
    )

    expect(auth_page.locator("#txt_visit_date")).to_have_js_property("validationMessage", "Please fill out this field.")

@pytest.mark.xfail(strict=True, reason="pending clarification: demo app currently accepts past dates")
def test_make_appointment_past_date(auth_page):
    appointment_page = AppointmentPage(auth_page)
    appointment_page.book_appointment(
        facility="Tokyo CURA Healthcare Center",
        visit_date="01/01/2020",
        comment="Past date test"
    )
    expect(auth_page).to_have_url(f"{BASE_URL}/#appointment")