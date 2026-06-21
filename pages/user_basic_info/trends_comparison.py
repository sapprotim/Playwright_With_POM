import time
from playwright.sync_api import Page

class UserComparisonPage:
    def __init__(self, page: Page):
        self.page = page

    def verify_clinical_comparison_selection(self):
        watch_btn = self.page.get_by_role("button", name="Comparison watch-img")
        assert watch_btn.is_visible() and watch_btn.is_enabled()
        watch_btn.click()
        time.sleep(2)

        dropdown_img = self.page.locator(".dropdown-option > img").first
        assert dropdown_img.is_visible() and dropdown_img.is_enabled()
        dropdown_img.click()

        clinical_checkboxes = [
            "Waist Circumference", "HbA1c", "Fasting Blood Glucose", "Total Cholesterol",
            "HDL Cholesterol", "LDL Cholesterol", "Triglycerides", "Resting Heart Rate",
            "Heart Rate Variability", "Select / Deselect All"
        ]

        for name in clinical_checkboxes:
            checkbox = self.page.get_by_role("checkbox", name=name)
            assert checkbox.is_visible() and checkbox.is_enabled()
            checkbox.check()

        self.page.get_by_role("button", name="Close").click()

    def verify_lifestyle_comparison_selection(self):
        time.sleep(3)
        watch_btn = self.page.get_by_role("button", name="Comparison watch-img")
        watch_btn.click()

        time.sleep(2)
        dropdown_img = self.page.locator(".dropdown-main > div:nth-child(2) > img")
        assert dropdown_img.is_enabled()
        dropdown_img.scroll_into_view_if_needed()
        dropdown_img.click(force=True)

        lifestyle_checkboxes = [
            "Processed Food", "Fruit & Vegetables", "Wholegrains",
            "Unhealthy Oil & Fat", "Limit Sugar", "Stress", "Select / Deselect All"
        ]

        for name in lifestyle_checkboxes:
            checkbox = self.page.get_by_role("checkbox", name=name)
            assert checkbox.is_visible() and checkbox.is_enabled()
            checkbox.check()

        self.page.get_by_role("button", name="Close").click()

    def verify_dashboard_sections_visibility(self):
        time.sleep(10)
        assert self.page.get_by_text("Wellness Score (Clinical)").is_visible()
        assert self.page.get_by_text("Wellness Score (Lifestyle)").is_visible()
        assert self.page.locator("#blood-pressure-analysis-dashboard").get_by_text("Blood Pressure").is_visible()
        assert self.page.get_by_text("Steps", exact=True).first.is_visible()
        assert self.page.get_by_text("Moderate Vigorous Physical").is_visible()
        assert self.page.get_by_text("Sleep", exact=True).is_visible()

        lifestyle_tags = [
            "Smoking", "Alcohol", "Processed Food", "Wholegrains",
            "Limit Sugar", "Stress", "Unhealthy Oil & Fat", "Fruit & Vegetables"
        ]
        for tag in lifestyle_tags:
            locator = self.page.locator("span").filter(has_text=tag)
            assert locator.is_enabled(timeout=5000) if tag == "Processed Food" else locator.is_visible()

        clinical_metrics = {
            "hpb-hba1c": "HbA1c",
            "hpb-hdl-cholestrol": "HDL Cholesterol",
            "app-total-cholestrol": "Total Cholesterol",
            "hpb-ldl-cholestrol": "LDL Cholesterol",
            "hpb-triglycerides": "Triglycerides",
            "hpb-fasting-blood-glucose": "Fasting Blood Glucose",
            "hpb-waist-circumference": "Waist Circumference",
            "hpb-bmi": "Body Mass Index",
            "hpb-resting-heart-rate": "Resting Heart Rate"
        }

        for key, label in clinical_metrics.items():
            assert self.page.locator(key).get_by_text(label).is_visible()

        assert self.page.get_by_text("Heart Rate Variabilty").is_visible()
