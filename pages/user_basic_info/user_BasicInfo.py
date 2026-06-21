import re
from playwright.sync_api import Page, expect
import time

class UserBasicInfoPage:
    def __init__(self, page: Page):
        self.page = page

    def verify_basic_info(self):
        assert self.page.locator("//p[@id='user-fullname']").text_content().strip() != ""
        assert self.page.locator("//div[@id='profile-gender']/p[1]").text_content().strip() == "NRIC"
        assert re.match(r"^[STFG]\d{7}[A-Z]$", self.page.locator("//div[@id='profile-gender']/p[2]").text_content().strip())
        assert self.page.locator("//p[normalize-space()='Sex']").text_content().strip() == "Sex"
        assert self.page.locator("//div[@class='ant-row ng-star-inserted']//p[@id='user-age']").text_content().strip() in ["Male", "Female"]
        assert self.page.locator("//p[normalize-space()='Age']").text_content().strip() == "Age"
        age = int(self.page.locator("//div[@class='profile-detailes-grid']//div[2]//p[2]").text_content().strip())
        assert 25 <= age <= 75
        assert self.page.locator("//p[normalize-space()='Race']").text_content().strip() == "Race"
        assert self.page.locator("//div[@class='profile-detailes-grid']//div[3]//p[2]").text_content().strip() != ""

    def verify_body_info(self):
        assert self.page.locator("//p[normalize-space()='Weight']").text_content().strip() == "Weight"
        assert re.match(r"^\d+(\.\d+)? kg$", self.page.locator("//p[@id='user-weight']").text_content().strip())
        assert self.page.locator("//p[normalize-space()='Height']").text_content().strip() == "Height"
        assert re.match(r"^\d+(\.\d+)?\s+cm$", self.page.locator("//p[@id='user-height']").text_content().strip().replace("\xa0", " "))
        assert self.page.locator("//p[normalize-space()='BMI']").text_content().strip() == "BMI"
        assert re.match(r"^\d+(\.\d+)? kg/m2$", self.page.locator("//p[@id='user-bmi']").text_content().strip())
        assert self.page.locator("//p[normalize-space()='Waist Circumference']").text_content().strip() == "Waist Circumference"
        assert re.match(r"^\d+(\.\d+)? cm$", self.page.locator("//p[@id='user-waist']").text_content().strip())

    def verify_vital_info(self):
        assert self.page.locator("//p[normalize-space()='Blood Pressure']").text_content().strip() == "Blood Pressure"
        expect(self.page.locator("//p[@id='user-anteriorPosterior']")).to_be_visible()
        time.sleep(5)

    def verify_last_updated(self):
        text = self.page.locator("//*[contains(text(), 'Last Updated:')]").text_content().strip()
        assert re.match(r"^Last Updated: \d{1,2} [A-Za-z]{3,9} \d{4}$", text)

    def verify_onboarding_date(self):
        text = self.page.locator("//body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[1]/div[2]/div[1]/h3[1]").text_content().strip()
        assert re.match(r"^Onboarding Date: \d{1,2} [A-Za-z]+ \d{4}$", text)
