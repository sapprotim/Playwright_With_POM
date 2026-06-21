import time
import re
from playwright.sync_api import Page, expect

class DefaultRolesPage:
    def __init__(self, page: Page):
        self.page = page

    def DefaultRoles_function(self):
        self.page.get_by_role("button", name="Default Roles ").click()
        self.page.get_by_role("button", name="Default Roles ").click()

    def Checkbox(self):
        checkbox = self.page.locator("//tbody/tr[2]/td[4]/label[1]/span[1]")
        expect(checkbox).to_be_visible()
        checkbox.click()
        self.page.get_by_role("button", name="Dismiss").click()

    def FHA_CheckboxText(self):
        self.page.get_by_text("Fullerton Health Admin", exact=True).nth(1).click()
    def CA_CheckboxText(self):
        self.page.get_by_text("Clinic Admin", exact=True).nth(1).click()
    def Doc_CheckboxText(self):
        self.page.get_by_text("Doctor", exact=True).nth(1).click()

    def CheckboxIn(self):
        self.DefaultRoles_function()
        self.FHA_CheckboxText()
        self.CA_CheckboxText()
        self.Doc_CheckboxText()
        self.Checkbox()

    def CheckboxOut(self):
        self.page.locator("//tbody/tr[2]/td[4]/label[1]/span[1]").click()
        self.page.get_by_role("button", name="Dismiss").click()
