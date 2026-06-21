import time
import random
from playwright.sync_api import expect, Page

class WCPage:
    def __init__(self, page: Page):
        self.page = page

    def WC_Add(self):
        WC_editButton = self.page.locator("div:nth-child(4) > .custom-card > .content-wrap > .footer > .right > .ng-star-inserted > .new-dot-toggle1 > img")
        expect(WC_editButton).to_be_visible()
        WC_editButton.click()
        time.sleep(2)

        WC_AddButton = self.page.get_by_role("button", name="Add value")
        expect(WC_AddButton).to_be_visible()
        WC_AddButton.click()
        time.sleep(2)

        self.page.locator("label.inp span.label").click()
        value5 = str(random.randint(50, 100))
        WC_Add_Value = self.page.locator("label.inp span.label")
        expect(WC_Add_Value).to_be_visible()
        WC_Add_Value.click()
        WC_Add_Value.type(value5)
        time.sleep(2)

        WC_Save = self.page.get_by_role("button", name="Save")
        expect(WC_Save).to_be_visible()
        WC_Save.click()
        time.sleep(2)
        self.page.get_by_role("button", name="Dismiss").click()
        time.sleep(2)
        self.page.locator("#add-body img").nth(1).click()

    def WC_edit(self):
        WC_edit = self.page.locator("label.inp span.label")
        value5 = str(random.randint(50, 100))
        expect(WC_edit).to_be_visible()
        time.sleep(2)
        WC_edit.clear()
        time.sleep(2)
        WC_edit.type(value5)
        time.sleep(2)

        WC_Save1 = self.page.get_by_role("button", name="Save")
        expect(WC_Save1).to_be_visible()
        WC_Save1.click()
        time.sleep(2)
        self.page.get_by_role("button", name="Dismiss").click()
        time.sleep(1)
        self.page.locator("#add-body img").first.click()
        time.sleep(5)
