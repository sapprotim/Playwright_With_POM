import time
import random
from playwright.sync_api import Page, expect


class LipidsPage:
    def __init__(self, page: Page):
        self.page = page

    def open_lipids_panel(self):
        lipids_edit_button = self.page.locator("div[data-target='#add-lipids'] img")
        lipids_edit_button.click()
        time.sleep(2)

    def is_third_lipid_visible(self) -> bool:
        lipid_locator = self.page.locator(
            "//body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[2]/div[1]/app-overview[1]/div[3]/app-lipids-widget[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-list-lipids[1]/div[1]/div[1]/div[2]/div[1]/div[3]"
        )
        try:
            return lipid_locator.is_visible(timeout=3000)
        except Exception:
            return False

    def add_lipid_values(self):
        add_button = self.page.get_by_role("button", name="Add value")
        expect(add_button).to_be_visible()
        add_button.click()
        time.sleep(2)

        self._fill_lipid_fields()

        save_button = self.page.get_by_role("button", name="Save")
        expect(save_button).to_be_visible()
        save_button.click()

        self.page.get_by_role("button", name="Dismiss").click()
        time.sleep(5)

        self.page.keyboard.press("Tab")
        time.sleep(2)

        self._click_edit_icon()
        time.sleep(2)

        self._fill_lipid_fields(clear_fields=True)

        save_button = self.page.get_by_role("button", name="Save")
        expect(save_button).to_be_enabled()
        save_button.click()
        time.sleep(2)

        self._close_lipid_panel()

    def edit_lipid_values(self):
        self._click_edit_icon()
        time.sleep(2)

        self._fill_lipid_fields(clear_fields=True)

        save_button = self.page.get_by_role("button", name="Save")
        expect(save_button).to_be_enabled()
        save_button.click()
        time.sleep(5)

        self._close_lipid_panel()

    def _click_edit_icon(self):
        edit_icon = self.page.locator(".content-body > div > .row > div:nth-child(5) > .form-wrap > .inp1 > img").first
        edit_icon.click()

    def _close_lipid_panel(self):
        close_icon = self.page.locator(
            "//body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[2]/div[1]/app-overview[1]/div[3]/app-lipids-widget[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-list-lipids[1]/div[1]/div[1]/div[1]/div[1]/img[1]"
        )
        close_icon.click()
        time.sleep(3)

    def _fill_lipid_fields(self, clear_fields=False):
        fields = [
            ("Total Cholesterol", "Total Cholesterol mmol/L"),
            ("Triglycerides", "Triglycerides mmol/L"),
            ("HDL Cholesterol", "HDL Cholesterol mmol/L"),
            ("LDL Cholesterol", "LDL Cholesterol mmol/L"),
        ]
        for label_text, field_name in fields:
            value = f"{random.uniform(0.1, 5):.1f}"
            self.page.locator(f"//label[@class='inp']//span[normalize-space()='{label_text}']").click()
            field = self.page.get_by_role("textbox", name=field_name)
            expect(field).to_be_visible()
            if clear_fields:
                field.clear()
                time.sleep(1)
            field.type(value)
            time.sleep(1)
