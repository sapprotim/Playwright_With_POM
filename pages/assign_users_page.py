from playwright.sync_api import Page, expect

class AssignUsersPage:
    def __init__(self, page: Page):
        self.page = page

    def click_assign_users(self):
        self.page.get_by_text("+ Assign Users").click()

    def click_confirm(self):
        self.page.get_by_role("button", name="Confirm").click()

    def click_dismiss(self):
        self.page.get_by_role("button", name="Dismiss").click()

    def assign_and_confirm(self):
        self.click_assign_users()
        self.click_confirm()
        self.click_dismiss()