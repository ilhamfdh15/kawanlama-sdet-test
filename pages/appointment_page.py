from pages.base_page import BasePage

class AppointmentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Locators
        self.facility_dropdown = page.locator("#combo_facility")
        self.readmission_checkbox = page.locator("#chk_hospotal_readmission")

        # Radio buttons for all healthcare programs
        self.medicare_radio = page.locator("#radio_program_medicare")
        self.medicaid_radio = page.locator("#radio_program_medicaid")
        self.none_radio = page.locator("#radio_program_none")

        self.visit_date_input = page.locator("#txt_visit_date")
        self.comment_input = page.locator("#txt_comment")
        self.book_btn = page.locator("#btn-book-appointment")
        self.confirmation_header = page.locator("h2:has-text('Appointment Confirmation')")

    def book_appointment(self, facility, date, comment, readmission=True, program="Medicaid"):
        """
        Books an appointment with flexible parameters.
        Defaults to Medicaid and readmission=True to remain backward-compatible with existing tests.
        """
        self.facility_dropdown.select_option(facility)

        # Let Playwright handle the state internally (auto-checks current state)
        if readmission:
            self.readmission_checkbox.check()
        else:
            self.readmission_checkbox.uncheck()

        # Dynamically handle program selection
        program_lower = program.lower()
        if program_lower == "medicare":
            self.medicare_radio.check()
        elif program_lower == "medicaid":
            self.medicaid_radio.check()
        else:
            self.none_radio.check()

        # NATIVE UI INTERACTION:
        self.visit_date_input.fill(date)
        self.visit_date_input.press("Enter")
        self.page.locator("body").click()
        self.comment_input.fill(comment)
        self.book_btn.click()