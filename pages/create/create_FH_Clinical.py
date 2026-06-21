import re
from playwright.sync_api import Page, expect
from pages.phone_number import generate_fake_sg_phone

class Create_FA_clinica:
    def __init__(self, page: Page):
        self.page = page

    def add_fullerton_health(self, name, address):
        try:
            expect(self.page.get_by_role("button", name="+ Add New Fullerton Health")).to_be_visible()
            self.page.get_by_role("button", name="+ Add New Fullerton Health").click()
            self.page.get_by_role("textbox", name=re.compile("Fullerton Health Name")).fill(name)
            self.page.get_by_role("textbox", name=re.compile("Fullerton Health Address")).fill(address)
            self.page.get_by_text("Add Fullerton Health").click()
            expect(self.page.get_by_role("button", name="Dismiss")).to_be_visible()
            self.page.get_by_role("button", name="Dismiss").click()

        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"

    def add_clinic(self, name, address, facility_name):
        try:
            self.page.get_by_role("button", name="+ Add New Clinic").click()
            self.page.get_by_role("textbox", name="Clinic Name").fill(name)
            self.page.get_by_role("textbox", name="Clinic Address").fill(address)
            self.page.locator("span", has_text="Parent Facility").click()
            self.page.locator(f"//li[normalize-space()='{facility_name}']").click()
            self.page.get_by_text("Add Clinic").click()
            self.page.get_by_role("button", name="Dismiss").click()

        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"