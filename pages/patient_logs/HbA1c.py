import random
import time
from playwright.sync_api import Page, expect

class HbA1cPage:
    def __init__(self, page: Page):
        self.page = page

    def add_or_edit_hba1c(self):
        # Click the HbA1c section icon
        hba1c_icon = self.page.locator("div:nth-child(2) > .custom-card > .content-wrap > .footer > .right > span > .new-dot-toggle1 > img")
        expect(hba1c_icon).to_be_visible()
        hba1c_icon.click()
        time.sleep(2)

        # Check if "Add value" button is available
        add_value_btn = self.page.get_by_role("button", name="Add value")
        if add_value_btn.count() > 0 and add_value_btn.is_visible():
            add_value_btn.click()
            textbox = self.page.get_by_role("textbox", name="%")
            expect(textbox).to_be_enabled()
            textbox.click()
            value = str(random.randint(3, 15))
            textbox.type(value)
            time.sleep(1)
            self.page.get_by_role("button", name="Save").click()
            self.page.get_by_role("button", name="Dismiss").click()
            self.page.locator("#add-hba1c img").click()
            time.sleep(2)
        else:
            # Edit existing value
            self.page.locator("#add-hba1c img").nth(1).click()
            textbox = self.page.get_by_role("textbox", name="%")
            textbox.click()
            time.sleep(2)
            textbox.clear()
            value = str(random.randint(3, 15))
            textbox.type(value)
            time.sleep(1)
            self.page.get_by_role("button", name="Save").click()
            self.page.get_by_role("button", name="Dismiss").click()
            self.page.locator("#add-hba1c img").first.click()
            time.sleep(2)
