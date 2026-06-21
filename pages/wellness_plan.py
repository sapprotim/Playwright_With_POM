from playwright.sync_api import Page, expect
from datetime import datetime, timedelta
import time
import re

class Wellnessplan:
    def __init__(self, page: Page):
        self.page = page

    def Wellness_plan_page(self):
        wellness_plan_page = self.page.locator("//a[@id='Wellness Plan']")
        assert wellness_plan_page.is_visible() and wellness_plan_page.is_enabled()
        wellness_plan_page.click()

    # Test conditional logic for old or new wellness plan paths
    def genarate_plan(self):
        try:
            self.page.wait_for_selector("//strong[normalize-space()='NRIC:']", timeout=5000)
            count = self.page.locator("//strong[normalize-space()='NRIC:']").count()

        except:
            count = 0

        if count > 0:
            self.old_plan()
            self.old_plan_calendar()
            self.old_sign_off_share()
        else:

            self.specify_patient_condition()
            self.specify_clinical_conditions()
            self.forth_question()
            self.lifestyle_patient_conditions()
            self.lifestyle_patient_conditions()  # appears duplicated — is that intended?
            self.assessment_calender()
            self.sign_off_share()

    # Test interactions for old wellness plan workflow
    def old_plan(self):
        # Generate Wellness Plan
        generate_plan_btn = self.page.get_by_role("button", name="Generate Wellness Plan")
        assert generate_plan_btn.is_visible() and generate_plan_btn.is_enabled()
        generate_plan_btn.click()

        # High-Normal Blood Pressure
        high_normal_bp = self.page.get_by_text("High-Normal Blood Pressure").first
        assert high_normal_bp.is_visible() and high_normal_bp.is_enabled()
        high_normal_bp.click()

        # Checkbox selections
        checkbox_1 = self.page.locator("div:nth-child(3) > .checkbox-container > div > .custom-checkbox > .checkmark").first
        assert checkbox_1.is_visible() and checkbox_1.is_enabled()
        checkbox_1.click()

        checkbox_2 = self.page.locator("div:nth-child(4) > .checkbox-container > .checkbox-item > .custom-checkbox > .checkmark")
        assert checkbox_2.is_visible() and checkbox_2.is_enabled()
        checkbox_2.click()

        checkbox_3 = self.page.locator("div:nth-child(2) > .custom-checkbox > .checkmark").first
        assert checkbox_3.is_visible() and checkbox_3.is_enabled()
        checkbox_3.click()

        checkbox_4 = self.page.locator("div:nth-child(3) > .checkbox-container > div:nth-child(2) > .custom-checkbox > .checkmark").first
        assert checkbox_4.is_visible() and checkbox_4.is_enabled()
        checkbox_4.click()

        # Adequately Controlled BP, Lipid, and Diabetes
        self.page.get_by_text("Adequately Controlled BP").click()
        self.page.get_by_text("Adequately Controlled Lipid").click()
        self.page.get_by_text("Adequately Controlled Diabetes").click()

        # Diabetic conditions
        self.page.get_by_text("Diabetic Retinopathy").click()
        self.page.get_by_text("Type 2 DM at Greater Risk of").click()

        # Poorly Controlled BP, Lipid, and Diabetes
        self.page.get_by_text("Poorly Controlled BP").click()
        self.page.get_by_text("Poorly Controlled Lipid").click()
        self.page.get_by_text("Poorly Controlled Diabetes").click()

        # Diabetic Neuropathy and Not relevant
        self.page.get_by_text("Diabetic Neuropathy").click()
        self.page.get_by_text("Not relevant").click()

        # Additional conditions
        time.sleep(1)
        self.page.locator("span").filter(has_text="High-Normal Blood Pressure").click()
        self.page.locator("span").filter(has_text="Pre-Diabetes").click()
        self.page.locator("span").filter(has_text=re.compile(r"^Lipid Disorders$")).click()
        self.page.locator("span").filter(has_text="Hypertension").click()
        self.page.locator("span").filter(has_text="Type 2 Diabetes Mellitus").click()
        self.page.locator("span").filter(has_text="High-Normal Blood Pressure").click()

        # Nutrition & Healthy Eating
        nutrition_btn = self.page.get_by_role("listitem").filter(has_text=re.compile(r"^Nutrition & Healthy Eating$")).get_by_role("button")
        assert nutrition_btn.is_visible() and nutrition_btn.is_enabled()
        nutrition_btn.click()

        # Choose fresh produce and limit sodium intake
        produce_checkbox = self.page.locator("label").filter(has_text="Choose fresh produce,").locator("span").nth(2)
        assert produce_checkbox.is_visible() and produce_checkbox.is_enabled()
        produce_checkbox.click()

        sodium_checkbox = self.page.locator("label").filter(has_text="Limit sodium intake to 2000mg").locator("span").nth(2)
        assert sodium_checkbox.is_visible() and sodium_checkbox.is_enabled()
        sodium_checkbox.click()

    # Test old plan calendar date selection
    def old_plan_calendar(self):
        self.page.get_by_role("textbox", name="Select date").click()
        time.sleep(1)
        self.page.locator("//button[@title='Choose a month']").click()
        time.sleep(2)
        # Calculate target month and day
        target_date = datetime.today() + timedelta(days=5)
        target_month = (datetime.today().month + 2 - 1) % 12 + 1  # month + 2, wrap around to 1–12
        target_day = target_date.day
        month_name = target_date.replace(month=target_month).strftime("%b")
        self.page.locator(f"//td[@title='{month_name}']").click()
        time.sleep(2)
        self.page.locator(f"//div[normalize-space()='{target_day}']").click()


    # Test sign off and share action
    def old_sign_off_share(self):
        sign_off_button = self.page.locator("//button[normalize-space()='Sign Off & Share']")
        assert sign_off_button.is_visible() and sign_off_button.is_enabled()
        sign_off_button.click()
        time.sleep(2)
        Confirm_button = self.page.locator("//button[normalize-space()='Confirm']")
        assert Confirm_button.is_visible() and Confirm_button.is_enabled()
        time.sleep(5)

    """New User plan"""
    # Test specifying patient condition in new plan flow
    def specify_patient_condition(self):
        self.page.locator("//button[normalize-space()='Generate Wellness Plan']").click()
        locator1 = self.page.locator("label").filter(has_text="High-Normal Blood Pressure").locator("span")
        assert locator1.is_visible() and locator1.is_enabled()
        locator1.click()

        # First checkbox
        locator2 = self.page.locator("div:nth-child(3) > .checkbox-container > div > .custom-checkbox > .checkmark").first
        assert locator2.is_visible() and locator2.is_enabled()
        locator2.click()

        # Second checkbox
        locator3 = self.page.locator(
            "div:nth-child(4) > .checkbox-container > .checkbox-item > .custom-checkbox > .checkmark")
        assert locator3.is_visible() and locator3.is_enabled()
        locator3.click()

        # Third checkbox
        locator4 = self.page.locator("div:nth-child(2) > .custom-checkbox > .checkmark").first
        assert locator4.is_visible() and locator4.is_enabled()
        locator4.click()

        # Fourth checkbox
        locator5 = self.page.locator(
            "div:nth-child(3) > .checkbox-container > div:nth-child(2) > .custom-checkbox > .checkmark").first
        assert locator5.is_visible() and locator5.is_enabled()
        locator5.click()

    # Test specifying clinical conditions by verifying visibility, enablement, and clicking each condition
    def specify_clinical_conditions(self):
        conditions = [
            "Adequately Controlled BP",
            "Adequately Controlled Lipid",
            "Adequately Controlled Diabetes",
            "Diabetic Retinopathy",
            "Type 2 DM at Greater Risk of",
            "Poorly Controlled BP",
            "Poorly Controlled Lipid",
            "Poorly Controlled Diabetes",
            "Diabetic Neuropathy"
        ]

        for text in conditions:
            locator = self.page.locator("label").filter(has_text=text).locator("span").nth(1)
            assert locator.is_visible(), f"'{text}' not visible"
            assert locator.is_enabled(), f"'{text}' not enabled"
            locator.click()

        combo_text = "Adequately Controlled BPPoorly Controlled BPAdequately Controlled Lipid"
        combo_locator = self.page.get_by_text(combo_text)
        assert combo_locator.is_visible(), f"'{combo_text}' not visible"
        assert combo_locator.is_enabled(), f"'{combo_text}' not enabled"
        combo_locator.click()

    # Test interaction with multiple buttons related to blood pressure, nutrition, diabetes, and lifestyle categories
    def forth_question(self):
        btn1 = self.page.get_by_role("listitem").filter(has_text="High-Normal Blood Pressure,").get_by_role("button").first
        assert btn1.is_visible() and btn1.is_enabled()
        btn1.click()

        btn2 = self.page.get_by_role("listitem").filter(has_text="High-Normal Blood Pressure,").get_by_role("button").nth(1)
        assert btn2.is_visible() and btn2.is_enabled()
        btn2.click()

        btn3 = self.page.get_by_role("listitem").filter(has_text="High-Normal Blood Pressure,").get_by_role("button").nth(2)
        assert btn3.is_visible() and btn3.is_enabled()
        btn3.click()

        btn4 = self.page.get_by_role("listitem").filter(has_text="High-Normal Blood Pressure,").get_by_role("button").nth(3)
        assert btn4.is_visible() and btn4.is_enabled()
        btn4.click()

        nutrition_div = self.page.locator("div").filter(has_text=re.compile(r"^Nutrition & Healthy Eating$")).nth(1)
        assert nutrition_div.is_visible() and nutrition_div.is_enabled()
        nutrition_div.click()

        btn5 = self.page.get_by_role("listitem").filter(has_text="Pre-Diabetes, Type 2 Diabetes").get_by_role("button").nth(1)
        assert btn5.is_visible() and btn5.is_enabled()
        btn5.click()

        btn6 = self.page.get_by_role("listitem").filter(has_text="Pre-Diabetes, Type 2 Diabetes").get_by_role("button").nth(2)
        assert btn6.is_visible() and btn6.is_enabled()
        btn6.click()

        btn7 = self.page.get_by_role("listitem").filter(has_text="Pre-Diabetes, Type 2 Diabetes").get_by_role("button").nth(3)
        assert btn7.is_visible() and btn7.is_enabled()
        btn7.click()

        cat1 = self.page.get_by_role("listitem").filter(has_text=re.compile(r"^Nutrition & Healthy Eating$")).get_by_role("button")
        assert cat1.is_visible() and cat1.is_enabled()
        cat1.click()

        cat2 = self.page.get_by_role("listitem").filter(has_text=re.compile(r"^Physical Activity & Weight Management$")).get_by_role("button")
        assert cat2.is_visible() and cat2.is_enabled()
        cat2.click()

        cat3 = self.page.get_by_role("listitem").filter(has_text=re.compile(r"^Smoking & Alcohol$")).get_by_role("button")
        assert cat3.is_visible() and cat3.is_enabled()
        cat3.click()

        cat4 = self.page.get_by_role("listitem").filter(has_text=re.compile(r"^Mental Well-being$")).get_by_role("button")
        assert cat4.is_visible() and cat4.is_enabled()
        cat4.click()

    # Test selecting lifestyle patient conditions by verifying visibility, enablement, and clicking
    def lifestyle_patient_conditions(self):
        conditions = [
            "High-Normal Blood Pressure",
            "Pre-Diabetes",
            "Lipid Disorders",
            "Hypertension",
            "Type 2 Diabetes Mellitus"
        ]

        for condition in conditions:
            locator = self.page.locator("label").filter(has_text=re.compile(rf"^{condition}$")).locator("span").first
            assert locator.is_visible(), f"'{condition}' is not visible"
            assert locator.is_enabled(), f"'{condition}' is not enabled"
            locator.click()

    # Test Nutrition & Healthy Eating sub-question by clicking the relevant button and option
    def forth_question_sub(self):
        nutrition_button = self.page.get_by_role("listitem").filter(has_text="Nutrition & Healthy Eating").get_by_role("button")
        nutrition_button.click()
        aim_substitute_button = self.page.locator("label").filter(has_text="Aim to substitute ≥50% of").locator("span").nth(2)
        assert aim_substitute_button.is_visible() and aim_substitute_button.is_enabled()
        aim_substitute_button.click()

    # Test interaction with assessment calendar widget including navigation and date selection
    def assessment_calender(self):
        self.page.get_by_role("textbox", name="Select date").click()
        time.sleep(1)
        self.page.locator("//button[@title='Choose a month']").click()
        time.sleep(2)
        # Calculate target month and day
        target_date = datetime.today() + timedelta(days=5)
        target_month = (datetime.today().month + 2 - 1) % 12 + 1  # month + 2, wrap around to 1–12
        target_day = target_date.day
        month_name = target_date.replace(month=target_month).strftime("%b")
        self.page.locator(f"//td[@title='{month_name}']").click()
        time.sleep(2)
        self.page.locator(f"//div[normalize-space()='{target_day}']").click()

    # Test sign off and share functionality including confirmation
    def sign_off_share(self):
        warning_locator = self.page.locator("//small[@id='warning-message']")

        if warning_locator.is_visible():
            warning_text = warning_locator.inner_text().strip()
            if warning_text == "Select at least 1 option!":
                # Click on the SVG icon
                self.page.locator("//li[1]//div[1]//button[1]//span[1]//*[name()='svg']").click()
                time.sleep(2)

                # Click on the second span inside the label
                self.page.locator(
                    "//body//app-root[@class='app-main']//div[@class='card-bordered']"
                    "//div[@class='ng-star-inserted']//div[@class='ng-star-inserted']"
                    "//div[1]//div[1]//label[1]//span[2]"
                ).click()
                time.sleep(2)

        sign_off_button = self.page.locator("//button[normalize-space()='Sign Off & Share']")
        assert sign_off_button.is_visible() and sign_off_button.is_enabled()
        sign_off_button.click()
        time.sleep(2)
        Confirm_button = self.page.locator("//button[normalize-space()='Confirm']")
        Confirm_button.click()
        assert Confirm_button.is_visible() and Confirm_button.is_enabled()
        time.sleep(5)