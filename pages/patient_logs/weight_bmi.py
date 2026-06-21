import random
import time
from playwright.sync_api import Page, expect

class BodyShapePage:
    def __init__(self, page: Page):
        self.page = page

    def add_weight_bmi(self):
        # Click edit button
        edit_button = self.page.locator("//div[@data-target='#add-bodyshape']//img")
        edit_button.click()

        # Add value
        self.page.get_by_role("button", name="Add value").click()
        time.sleep(2)

        # Select Weight tab
        self.page.locator("#add-bodyshape").get_by_text("Weight").click()

        # Enter weight
        weight_value = str(random.randint(40, 85))
        weight_input = self.page.get_by_role("textbox", name="Weight kg")
        weight_input.type(weight_value)
        time.sleep(2)

        # Focus BMI input (triggers calculation or validation)
        self.page.get_by_role("textbox", name="BMI").click()

        # Save
        self.page.get_by_role("button", name="Save").click()
        self.page.get_by_role("button", name="Dismiss").click()
        time.sleep(3)

    def edit_weight_bmi(self):
        # Reopen edit
        time.sleep(2)
        self.page.locator("#add-bodyshape img").nth(1).click()

        # Edit weight
        new_value = str(random.randint(40, 85))
        weight_input = self.page.get_by_role("textbox", name="Weight kg")
        weight_input.clear()
        time.sleep(1)
        weight_input.type(new_value, delay=10)

        # Focus BMI input
        self.page.get_by_role("textbox", name="BMI").click()

        # Save
        self.page.get_by_role("button", name="Save").click()
        self.page.get_by_role("button", name="Dismiss").click()
        time.sleep(1)

        # Close modal
        self.page.locator("app-list-bodyshape > div > .add-patient-container > .header-wrap > .close-btn > img").click()
        time.sleep(3)
