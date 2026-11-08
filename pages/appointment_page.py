from playwright.sync_api import Page, expect

class AppointmentPage:
    def __init__(self, page: Page):
        self.page = page

        # Form Locators
        self.facility_dropdown = page.locator("#combo_facility")
        self.readmission_checkbox = page.locator("#chk_hospotal_readmission")
        self.medicare_radio = page.locator("#radio_program_medicare")
        self.medicaid_radio = page.locator("#radio_program_medicaid")
        self.none_radio = page.locator("#radio_program_none")
        self.visit_date_input = page.locator("#txt_visit_date")
        self.calendar_icon = page.locator(".input-group-addon")
        self.comment_input = page.locator("#txt_comment")
        self.book_button = page.locator("#btn-book-appointment")

        # Summary Locators
        self.summary_facility = page.locator("#facility")
        self.summary_readmission = page.locator("#hospital_readmission")
        self.summary_program = page.locator("#program")
        self.summary_visit_date = page.locator("#visit_date")
        self.summary_comment = page.locator("#comment")

    def book_appointment(self, facility: str, visit_date: str, comment: str, readmission: bool = False, healthcare_program: str = "Medicare"):
        """Fills out and submits the appointment booking form by properly committing the datepicker."""
        self.facility_dropdown.select_option(facility)

        if readmission:
            self.readmission_checkbox.check()
        else:
            self.readmission_checkbox.uncheck()

        if healthcare_program == "Medicare":
            self.medicare_radio.check()
        elif healthcare_program == "Medicaid":
            self.medicaid_radio.check()
        elif healthcare_program == "None":
            self.none_radio.check()

        # 1. Clear and type the date naturally to trigger change events
        self.visit_date_input.click()
        self.visit_date_input.fill("")
        self.visit_date_input.press_sequentially(visit_date, delay=50)

        # 2. Click the calendar icon addon again to toggle/close the datepicker popup natively
        self.calendar_icon.click()

        # 3. Fill comment and click book safely
        self.comment_input.fill(comment)
        self.book_button.click()

    def verify_appointment_summary(self, facility: str, visit_date: str, comment: str, readmission: str = "No", healthcare_program: str = "Medicare"):
        """Validates the text of the appointment summary page."""
        expect(self.summary_facility).to_have_text(facility)
        expect(self.summary_readmission).to_have_text(readmission)
        expect(self.summary_program).to_have_text(healthcare_program)
        expect(self.summary_visit_date).to_have_text(visit_date)
        expect(self.summary_comment).to_have_text(comment)