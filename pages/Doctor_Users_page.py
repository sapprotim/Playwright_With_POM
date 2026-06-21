import time
from playwright.sync_api import Page, expect


class Doctoruserpage:
    def __init__(self, page: Page):
        self.page = page

    def select_doctor_users_page(self):
        self.page.locator("//tbody/tr[1]/td[1]/a[1]").click()
        time.sleep(7)

    def select_clinic_users_page(self, item_name):
        self.page.locator("//tbody/tr[1]/td[1]/img[1]").click()
        self.page.get_by_text("XYZ-clinic").click()




