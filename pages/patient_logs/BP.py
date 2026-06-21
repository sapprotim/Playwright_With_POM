import random
import time
from playwright.sync_api import Page, expect

class BloodPressurePage:
    def __init__(self, page: Page):
        self.page = page

    def add_blood_pressure(self):
        # Open blood pressure edit
        bp_edit = self.page.locator("#blood-pressure-overview-dashboard img").nth(1)
        expect(bp_edit).to_be_visible()
        bp_edit.click()

        # Click Add value
        add_value = self.page.locator("#add-blood-pressure").get_by_text("Add value")
        expect(add_value).to_be_visible()
        add_value.click()
        time.sleep(2)

        # Fill systolic
        systolic = str(random.randint(100, 130))
        systolic_input = self.page.get_by_role("textbox", name="Systolic mmHg")
        expect(systolic_input).to_be_visible()
        expect(systolic_input).to_be_enabled()
        systolic_input.click()
        systolic_input.type(systolic)

        # Fill diastolic
        diastolic = str(random.randint(60, 90))
        diastolic_input = self.page.get_by_role("textbox", name="Diastolic mmHg")
        expect(diastolic_input).to_be_visible()
        expect(diastolic_input).to_be_enabled()
        diastolic_input.click()
        diastolic_input.type(diastolic)

        # Save
        save_btn = self.page.get_by_role("button", name="Save")
        expect(save_btn).to_be_visible()
        save_btn.click()

        # Dismiss popup
        self.page.get_by_role("button", name="Dismiss").click()
        self.page.locator("#add-blood-pressure img").first.click()
        time.sleep(2)
