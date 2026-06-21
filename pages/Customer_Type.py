import time
from playwright.sync_api import Page, expect

class CustomerType:
    def __init__(self, page: Page):
        self.page = page

    def customtype(self):
        self.page.get_by_role("button", name="All ▾").click()
        self.page.get_by_text("Corporate").click()
        self.page.get_by_role("button", name="Corporate ▾").click()
        self.page.get_by_text("Clinic Walk-In").click()
        self.page.get_by_role("button", name="Clinic Walk-In ▾").click()
        self.page.get_by_text("Public").click()