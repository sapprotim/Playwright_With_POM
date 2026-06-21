import time
import re
from playwright.sync_api import Page, expect
from faker import Faker
fake = Faker()


class CustomRolePage:
    def __init__(self, page: Page):
        self.page = page

    def CustomRoles_function(self):
        self.page.get_by_role("button", name="Custom Roles ").click()
        self.page.get_by_role("button", name="Custom Roles ").click()

    def customRole_Create(self):
        fake = Faker()
        global roleName
        roleName = fake.name()
        self.CustomRoles_function()
        create = self.page.get_by_role("button", name="Add a New Role")
        expect(create).to_be_visible()
        create.click()
        self.page.get_by_role("textbox", name="Role Name").click()
        self.page.get_by_role("textbox", name="Role Name").type(roleName)
        self.page.get_by_role("button", name="Add Role").click()


    async def customRole_Edit(self):
        self.page.locator("//div[13]//div[1]//div[1]//i").last.click()
        self.page.get_by_role("menuitem", name="Edit").click()
        time.sleep(2)
        text = self.page.get_by_role("textbox")
        expect(text).to_be_editable()
        await text.click(timeout=1000)
        text.clear()
        text.type(roleName, timeout=60)
        text.press("Enter", expect=True)
        time.sleep(2)
        self.page.get_by_role("button", name="YES").click()
        self.page.get_by_role("button", name="Dismiss").click()


    def customRole_CheckboxIn(self):
        self.page.get_by_text(roleName).click()
        checkbox = self.page.locator("tr:nth-child(2) > td:nth-child(4) > .custom-checkbox > .checkmark")
        expect(checkbox).to_be_visible()
        checkbox.click()
        self.page.get_by_role("button", name="Save Changes").click()
        self.page.get_by_role("button", name="Dismiss").click()

    def customRole_CheckboxOut(self):
        self.page.get_by_text(roleName).click()
        self.page.locator("tr:nth-child(2) > td:nth-child(4) > .custom-checkbox > .checkmark").click()
        self.page.get_by_role("button", name="Save Changes").click()
        self.page.get_by_role("button", name="Dismiss").click()


    def customrole_Delete(self):
        self.page.get_by_text(roleName).click()
        self.page.locator("//div[13]//div[1]//div[1]//i").last.click()
        self.page.get_by_role("menuitem", name="Delete").click()
        self.page.get_by_role("button", name="YES").click()
        self.page.get_by_role("button", name="Dismiss").click()
