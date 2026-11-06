from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#txt-username")
        self.password_input = page.locator("#txt-password")
        self.login_btn = page.locator("#btn-login")
        self.menu_toggle = page.locator("#menu-toggle")
        self.logout_link = page.locator("text=Logout")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()

    def logout(self):
        self.menu_toggle.click()
        self.logout_link.click()