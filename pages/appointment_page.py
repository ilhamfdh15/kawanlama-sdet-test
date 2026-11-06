from pages.base_page import BasePage

class AppointmentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.facility_dropdown = page.locator("#combo_facility")
        self.readmission_checkbox = page.locator("#chk_hospotal_readmission")
        self.medicaid_radio = page.locator("#radio_program_medicaid")
        self.visit_date_input = page.locator("#txt_visit_date")
        self.comment_input = page.locator("#txt_comment")
        self.book_btn = page.locator("#btn-book-appointment")
        self.confirmation_header = page.locator("h2:has-text('Appointment Confirmation')")

    def book_appointment(self, facility, date, comment):
        self.facility_dropdown.select_option(facility)

        if not self.readmission_checkbox.is_checked():
            self.readmission_checkbox.check()

        self.medicaid_radio.check()

        # Bypass readonly restriction by setting value via JS and dispatching events
        self.visit_date_input.evaluate(
            "(element, val) => { element.value = val; element.dispatchEvent(new Event('input')); element.dispatchEvent(new Event('change')); }",
            date
        )

        # Dismiss calendar overlay
        self.page.keyboard.press("Escape")

        self.comment_input.fill(comment)
        self.book_btn.click()