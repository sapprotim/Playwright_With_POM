from faker import Faker
from playwright.sync_api import Page, expect
import time
import random
from playwright.sync_api import Page, expect
from pages.phone_number import generate_fake_sg_phone

fake = Faker()
class CreateFullertonHealthPage:
    def __init__(self, page: Page):
        self.page = page

    def create_fh_admin(self) -> str:
        try:
            self.page.get_by_text("+ Add A New Fullerton Health").click()

            user_name = "AT" + fake.user_name()

            # Fill user name and click Next
            self.page.get_by_role("textbox", name="User name").type(user_name)
            self.page.keyboard.press(" ")
            self.page.get_by_text("Next").first.click()

            # Generate and fill personal details
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            self.page.get_by_role("textbox", name="First Name").fill(first_name)
            self.page.get_by_role("textbox", name="Last Name").fill(last_name)
            self.page.get_by_role("textbox", name="Email ID").fill(email)

            # Select country from dropdown
            self.page.locator(".ng-arrow-wrapper").click()
            expect(self.page.get_by_role("option", name="Singapore")).to_be_visible()
            self.page.get_by_role("option", name="Singapore").click()

            # Select phone country code
            self.page.locator("//div[@class='iti__arrow']").click()
            self.page.get_by_role("textbox", name="Search Country").type("singapore")
            self.page.locator("#iti-0__item-sg").get_by_text("Singapore").click()

            # Generate and fill phone number
            phone_input = self.page.get_by_role("textbox", name="4567")
            expect(phone_input).to_be_visible()
            phone_input.fill(generate_fake_sg_phone())

            self.page.get_by_text("Next").click()

            # Select facility
            self.page.locator("//span[normalize-space()='Fullerton Health']").click()
            time.sleep(2)

            for i in range(1, 6):
                self.page.locator(
                    f"//*[@id='add-admin']/div/div/div/div/app-add-facility-admin/div[1]/div[2]/div[2]/form/div[2]/div[2]/app-assign-facility/form/div/div/div/div[1]/ul/li[{i}]").click()

            self.page.locator("//span[normalize-space()='Fullerton Health']").click()
            time.sleep(2)

            # Create account
            create_button = self.page.get_by_text("Create Account")
            expect(create_button).to_be_visible()
            create_button.click()

            # Dismiss confirmation
            expect(self.page.get_by_role("button", name="Dismiss")).to_be_visible(timeout=5000)
            self.page.get_by_role("button", name="Dismiss").click()

            full_name = f"{first_name} {last_name}"
            return full_name

        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"