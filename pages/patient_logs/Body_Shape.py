from datetime import datetime
import random
import time
from playwright.sync_api import Page, expect


class BodyShapeTests:
    def __init__(self, page: Page):
        self.page = page


    def test_add_weight_bmi(self, page: Page):
        self.page.locator("//div[@data-target='#add-bodyshape']//img").click()
        self.page.get_by_role("button", name="Add value").click()
        time.sleep(2)

        self.page.locator("#add-bodyshape").get_by_text("Weight").click()
        weight = str(random.randint(40, 85))
        weight_input = self.page.get_by_role("textbox", name="Weight kg")
        weight_input.type(weight)
        time.sleep(2)
        self.page.get_by_role("textbox", name="BMI").click()
        self.page.get_by_role("button", name="Save").click()
        time.sleep(3)

    def test_edit_weight_bmi(self, page: Page):
        self.page.locator("#add-bodyshape img").nth(1).click()
        new_val = str(random.randint(40, 85))
        input_field = page.get_by_role("textbox", name="Weight kg")
        input_field.clear()
        time.sleep(1)
        input_field.type(new_val, delay=10)
        self.page.get_by_role("textbox", name="BMI").click()
        self.page.get_by_role("button", name="Save").click()
        time.sleep(1)
        self.page.locator("app-list-bodyshape > div > .add-patient-container > .header-wrap > .close-btn > img").click()
        time.sleep(3)