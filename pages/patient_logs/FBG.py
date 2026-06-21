import random
import time
from playwright.sync_api import Page, expect

class GlucosePage:
    def __init__(self, page: Page):
        self.page = page

    def add_fasting_blood_glucose(self):
        # Open glucose section
        glucose_section = self.page.get_by_role("heading", name="Fasting Blood Glucose").locator("div")
        glucose_section.click()

        # Click edit
        edit_btn = self.page.query_selector("div[data-target='#add-blood-glucose'] img")
        edit_btn.click()

        # Click Add value
        add_value = self.page.locator("#add-blood-glucose").get_by_text("Add value")
        expect(add_value).to_be_visible()
        add_value.click()

        # Enter glucose value
        glucose_value = str(random.randint(2, 30))
        glucose_input = self.page.get_by_role("textbox", name="mmol/L")
        expect(glucose_input).to_be_visible()
        glucose_input.click()
        glucose_input.type(glucose_value)
        time.sleep(2)

        # Save
        save_btn = self.page.get_by_role("button", name="Save")
        expect(save_btn).to_be_visible()
        save_btn.click()
        self.page.get_by_role("button", name="Dismiss").click()
        time.sleep(2)

    def edit_fasting_blood_glucose(self):
        # Open edit
        self.page.locator("#add-blood-glucose img").nth(1).click()
        glucose_input = self.page.get_by_role("textbox", name="mmol/L")
        new_value = str(random.randint(2, 30))
        time.sleep(2)
        glucose_input.clear()
        time.sleep(2)
        glucose_input.type(new_value)

        # Save
        save_btn = self.page.get_by_role("button", name="Save")
        save_btn.click()
        self.page.get_by_role("button", name="Dismiss").click()
        self.page.locator("#add-blood-glucose img").first.click()
        time.sleep(2)
