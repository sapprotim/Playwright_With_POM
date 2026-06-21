import re
import time
import random
from faker import Faker
from playwright.sync_api import Page, expect
from fontTools.merge.util import first
from playwright.sync_api import Page, expect
from faker import Faker
import random

from pages.phone_number import generate_fake_sg_phone

fake = Faker()

class create_clinic_page:
    def __init__(self, page: Page):
        self.page = page

    def create_clinic_admin(self) -> str:
        try:
            add_admin_button = self.page.get_by_text("+ Add A New Clinic Admin")
            expect(add_admin_button).to_be_visible()
            add_admin_button.click()

            username = fake.name()
            username_input = self.page.get_by_role("textbox", name="User name")
            expect(username_input).to_be_visible()
            time.sleep(2)
            username_input.type(username)

            next_button = self.page.get_by_text("Next").first
            expect(next_button).to_be_visible()
            next_button.click()

            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            self.page.get_by_role("textbox", name="First Name").fill(first_name)
            self.page.get_by_role("textbox", name="Last Name").fill(last_name)
            self.page.get_by_role("textbox", name="Email ID").fill(email)

            self.page.locator(".ng-arrow-wrapper").click()
            time.sleep(2)
            self.page.get_by_role("option", name="Singapore").click()

            self.page.locator("//div[@class='iti__arrow']").click()
            self.page.get_by_role("textbox", name="Search Country").click()
            self.page.get_by_role("textbox", name="Search Country").type("singapore")
            self.page.locator("#iti-0__item-sg").get_by_text("Singapore").click()


            phone_input = self.page.get_by_role("textbox", name="4567")
            expect(phone_input).to_be_visible()
            time.sleep(1)
            phone_input.fill(generate_fake_sg_phone())

            self.page.get_by_text("Next").click()

            self.page.locator("//div[@class='schedule-custom-dropdown-single']//img").click()
            facility_option = self.page.locator("//div[@class='dropdown open']//ul[@class='dropdown-menu']/li[1]")
            expect(facility_option).to_be_visible()
            facility_option.click()

            clinic_label_img = self.page.locator("label").filter(has_text=re.compile(r"^Clinic$")).locator("img")
            expect(clinic_label_img).to_be_visible()
            clinic_label_img.click()

            department_option = self.page.locator("//div[@class='schedule-custom-dropdown']//li[1]")
            expect(department_option).to_be_visible()
            department_option.click()

            create_button = self.page.get_by_text("Create Account")
            expect(create_button).to_be_visible()
            create_button.click()

            time.sleep(2)
            expect(self.page.get_by_role("button", name="Dismiss")).to_be_visible(timeout=5000)
            self.page.get_by_role("button", name="Dismiss").click()

            full_name = f"{first_name} {last_name}"
            return full_name

        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"
