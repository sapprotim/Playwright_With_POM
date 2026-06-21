import time
import re
from playwright.sync_api import Page, expect

class WellnessScoreTab:
    def __init__(self, page: Page):
        self.page = page

    def verify_clinical_value_format(self):
        time.sleep(5)
        raw_text = self.page.locator("//span[@class='highcharts-title']//div").text_content().strip()
        cleaned = raw_text.replace("\n", "").replace("\r", "").replace(" ", "").strip()
        formatted = cleaned.replace("Clinical", "Clinical:")
        assert re.match(r"^Clinical:\d+$", formatted), f"Unexpected format: {formatted}"

    def verify_all_clinical_elements(self):
        elements = self.page.locator('//*[@id="wellness-score-dashboard"]/div[2]/div/div/div/ul/span/li/div')
        count = elements.count()
        assert count == 11, f"Expected 11 elements, found {count}"
        for i in range(count):
            el = elements.nth(i)
            assert el.is_visible()
            assert el.is_enabled()
            el.click(timeout=3000)

    def navigate_to_lifestyle_tab(self):
        self.page.locator("//span[@class='mdc-tab__text-label'][normalize-space()='Lifestyle']").click()
        time.sleep(5)

    def verify_lifestyle_value_format(self):
        time.sleep(10)
        raw_text = self.page.locator("//span[@class='highcharts-title']//div").text_content().strip()
        cleaned = raw_text.replace("\n", "").replace("\r", "").replace(" ", "").strip()
        formatted = cleaned.replace("Lifestyle", "Lifestyle:")
        assert re.match(r"^Lifestyle:\d+$", formatted), f"Unexpected format: {formatted}"

    def verify_all_lifestyle_elements(self):
        elements = self.page.locator('//*[@id="wellness-score-dashboard"]/div[2]/div/div/div/ul/span/li/div')
        count = elements.count()
        assert count == 12, f"Expected 12 elements, found {count}"
        for i in range(count):
            el = elements.nth(i)
            assert el.is_visible(), f"Element {i+1} not visible"
            assert el.is_enabled(), f"Element {i+1} not enabled"
            el.click(timeout=3000)

    def calendar_filter_dropdown(self):
        img1 = self.page.locator("#wellness-score-dashboard label img")
        img2 = self.page.locator("//img[@src='./assets/images/calendar.png']")

        if img1.is_visible():
            img1.click()
        else:
            img2.click()

        options = [
            "Today", "Yesterday", "Last 7 Days", "Last 15 Days",
            "Last 30 Days", "Last 60 Days", "Last 90 Days", "Custom range"
        ]
        for option in options:
            btn = self.page.get_by_role("button", name=option)
            assert btn.is_visible(), f"{option} button not visible"
            btn.click()

        update_btn = self.page.get_by_role("button", name="Update")
        assert update_btn.is_visible(), "Update button not visible"
        update_btn.click()

    def view_filter_buttons(self):
        for option in ["Year", "Day", "Month", "Week"]:
            btn = self.page.get_by_role("button", name=option)
            assert btn.is_visible(), f"{option} button not visible"
            assert btn.is_enabled(), f"{option} button not enabled"
            btn.click()

    def calendar_parameter_images(self):
        time.sleep(2)
        container = self.page.locator("app-blood-pressure-wheel-parameters div").filter(has_text="Day Week Month Year Today")
        first_img = container.locator("img").first
        third_img = container.locator("img").nth(2)

        assert first_img.is_visible() and first_img.is_enabled()
        first_img.click()

        assert third_img.is_visible() and third_img.is_enabled()
        third_img.click()

    def verify_generate_wellness_plan_button(self):
        btn = self.page.locator("//button[@class='generate-wellness-plan']")
        expect(btn).to_be_visible()
        expect(btn).to_be_enabled()
