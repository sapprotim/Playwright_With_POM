import re
from playwright.sync_api import Page

class DataValidation:
    def __init__(self, page: Page):
        self.page = page

    def validate_blood_pressure(self):
        self.page.reload()
        sbp_text = self.page.locator("//*[@id='blood-pressure-overview-dashboard']/div[1]/div[1]/div[2]/span[1]").text_content()
        dbp_text = self.page.locator("//*[@id='blood-pressure-overview-dashboard']/div[1]/div[2]/div[2]/span[1]").text_content()
        sbp = int(sbp_text.strip())
        dbp = int(dbp_text.strip())
        expected_bp_string = f"{sbp}/{dbp} mmHg"
        displayed_bp = self.page.locator("//p[@id='user-anteriorPosterior']").text_content().strip()
        print(sbp_text, dbp_text, sbp, dbp)
        assert expected_bp_string == displayed_bp, f"Expected {expected_bp_string}, but got {displayed_bp}"

    def validate_weight(self):
        raw_text = self.page.locator("//p[@id='user-weight']").inner_text()  # e.g., "47 kg"'
        assert "kg" in raw_text.lower(), f"Expected unit 'kg' in '{raw_text}'"

    def validate_bmi(self):
        raw_text = self.page.locator("//p[@id='user-bmi']").inner_text()  # e.g., "15 kg/m2"
        assert "kg/m2" in raw_text.lower(), f"Expected unit 'kg/m2' in '{raw_text}'"

    def validate_waist_circumference(self):
        raw_text = self.page.locator("//p[@id='user-waist']").inner_text()  # e.g., "85 cm"
        assert "cm" in raw_text.lower(), f"Expected unit 'cm' in '{raw_text}'"