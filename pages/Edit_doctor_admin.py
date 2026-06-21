from fontTools.merge.util import first
from playwright.sync_api import Page, expect
from faker import Faker
import random
import time
from .phone_number import generate_fake_sg_phone





class Editdector:
    def __init__(self, page: Page):
        self.page = page
        self.fake = Faker()

    def edit_dector(self):
        try:
            self.page.locator("//img[@title='Refresh']").click()
            self.page.locator("//img[@src='./assets/images/edit.png']").first.click(timeout=5000)
            self.page.get_by_role("textbox", name="First Name").click()
            self.page.get_by_role("textbox", name="Last Name").click()
            self.page.get_by_role("textbox", name="Email ID").click()

            if self.page.locator("//div[@class='iti__arrow']").is_visible():
                self.page.locator("//div[@class='iti__arrow']").click()
            else:
                self.page.locator("//div[@class='selected-dial-code'] | //div[@class='iti__selected-flag dropdown-toggle']").click()

            self.page.locator("//input[@id='country-search-box']").fill("Singapore")
            self.page.locator("//span[@class='iti__country-name'][normalize-space()='Singapore']").click()

            # Generate Singapore-style phone number
            self.page.fill("//input[@id='phone']", generate_fake_sg_phone())

            time.sleep(1)
            self.page.locator("//div[normalize-space()='Country']").first.click()
            self.page.get_by_role("textbox", name="search country").click()
            self.page.get_by_role("textbox", name="search country").fill("Singapore")
            self.page.get_by_role("textbox", name="search country").press("Enter")
            time.sleep(3)


            # self.page.get_by_text("Unit Preferences").click()
            # self.page.get_by_text("Fahrenheit (°F)").click()
            # self.page.get_by_text("Celsius (°C)").click()
            # self.page.get_by_text("Pound (lb)").click()
            # self.page.get_by_text("Kilogram (kg)").click()
            # self.page.get_by_text("Feets & inches").click()
            # self.page.get_by_text("Centimeter (cm)").first.click()
            # self.page.get_by_text("Inch (in)").click()
            # self.page.get_by_text("Centimeter (cm)").nth(1).click()
            # self.page.get_by_text("Milligrams per decilitre (mg/").first.click()
            # self.page.get_by_text("Millimoles per litre (mmol/L)").first.click()
            # self.page.get_by_text("Milligrams per decilitre (mg/").nth(1).click()
            # self.page.get_by_text("Millimoles per litre (mmol/L)").nth(1).click()
            # self.page.get_by_text("Millimoles per mol (mmol/mol)").click()
            # self.page.get_by_text("Percentage (%)").click()
            #
            # self.page.get_by_text("Notification Preference").click()
            # self.page.locator("label:nth-child(3) > .checkmark").first.click()
            # self.page.get_by_text("Enabled").first.click()
            self.page.get_by_text("Affiliation").click()
            #
            # self.page.locator(".schedule-drop-value > img").first.click()
            # list_items = self.page.locator("//div[@class='dropdown open']//ul[@class='dropdown-menu']//li")
            # count = list_items.count()
            # list_items.nth(random.randint(0, count - 1)).click()
            #
            # self.page.locator(".schedule-custom-dropdown > .dropdown > .schedule-drop-value > img").first.click()
            # time.sleep(1)
            # list_items = self.page.locator("//div[@class='dropdown open']//ul[@class='dropdown-menu']/li")
            # count = list_items.count()
            # list_items.nth(random.randint(0, count - 1)).click()
            #
            # if self.page.locator("//div[contains(text(),'Clinic cannot be empty')]").is_visible():
            #     self.page.locator(".schedule-custom-dropdown > .dropdown > .schedule-drop-value > img").first.click()
            #     time.sleep(1)
            #     list_items = self.page.locator("//div[@class='dropdown open']//ul[@class='dropdown-menu']/li")
            #     count = list_items.count()
            #     list_items.nth(random.randint(0, count - 1)).click()

            self.page.locator("//app-assign-care-team-facility-dept//div[@class='next-btn'][normalize-space()='Save Changes']").click()
            self.page.get_by_role("button", name="Dismiss").click()
            time.sleep(6)

        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"







