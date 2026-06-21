import time
from playwright.sync_api import Page, expect

class assign:
    def __init__(self, page: Page):
        self.page = page

    def assign_users(self):
        self.page.get_by_text("+ Assign Users").click()
        self.page.get_by_role("button", name="Confirm").click()
        self.page.get_by_role("button", name="Dismiss").click()

    def assign_doctor(self):
        self.page.get_by_text("+ Assign Doctor").click()
        self.page.get_by_role("button", name="Confirm").click()
        self.page.get_by_role("button", name="Dismiss").click()

    def assign_Clinic_Admin(self):
        self.page.get_by_text("+ Assign Clinic Admin").click()
        self.page.get_by_role("button", name="Confirm").click()
        self.page.get_by_role("button", name="Dismiss").click()

    def assign_fh_Admin(self):
        self.page.get_by_text("+ Assign Fullerton Health Admin").click()
        self.page.get_by_role("button", name="Confirm").click()
        self.page.get_by_role("button", name="Dismiss").click()
