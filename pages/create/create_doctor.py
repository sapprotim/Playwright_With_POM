import re
import time
import random
from playwright.sync_api import Page, expect
from faker import Faker
from pages.phone_number import generate_fake_sg_phone

fake = Faker()

class DoctorCreationPage:
    def __init__(self, page: Page):
        self.page = page

    def create_doctor(self):
        try:
            self.page.get_by_text("+ Add A New Doctor").click()
            expect(self.page.get_by_role("textbox", name="Email ID")).to_be_visible()

            self.page.get_by_role("textbox", name="Email ID").fill(fake.email())
            self.page.get_by_text("Next").first.click()

            first_name = fake.first_name()
            last_name = fake.last_name()
            self.page.get_by_role("textbox", name="First Name").fill(first_name)
            self.page.get_by_role("textbox", name="Last Name").fill(last_name)
            self.page.get_by_role("textbox", name="Specialization").fill("General Medicine")

            self.page.locator(".ng-arrow-wrapper").click()
            time.sleep(1)
            self.page.get_by_role("option", name="Singapore").click()
            time.sleep(1)

            self.page.locator("(//input[@id='phone'])[1]").fill(generate_fake_sg_phone())
            time.sleep(1)
            self.page.get_by_text("Next").click()

            # self.page.get_by_text("Next").nth(1).click()
            # expect(self.page.get_by_text("Enabled")).to_be_visible()
            # self.page.get_by_text("Enabled").click()
            # self.page.locator("label").filter(has_text="Disabled").locator("span").click()
            # self.page.locator("label").filter(has_text="Enabled").locator("span").click()
            # self.page.get_by_text("Next").nth(1).click()

            self.page.locator("//div[@class='schedule-custom-dropdown-single']//img").click()
            self.page.locator("//div[@class='dropdown open']//ul[@class='dropdown-menu']/li[2]").click()

            self.page.locator("label").filter(has_text=re.compile(r"^Clinic$")).locator("img").click()
            options = self.page.locator("//div[@class='dropdown open']//ul[@class='dropdown-menu']/li")
            count = options.count()

            for i in range(count):
                option = options.nth(i)
                expect(option).to_be_visible()
                option.click()
                self.page.wait_for_timeout(500)

            self.page.get_by_text("Create Account").click()
            self.page.get_by_role("button", name="Dismiss").click()
            time.sleep(2)

            full_name = f"{first_name} {last_name}"
            return full_name

        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"