from playwright.sync_api import Page, expect
import time
from data import user_name


class UserProfileSearch:
    def __init__(self, page: Page):
        self.page = page

    def search_user_profile(self):
        self.page.fill("input[placeholder='Search']", user_name)
        self.page.locator("//tbody/tr[1]/td[1]/div[1]/div[1]/div[1]/span[1]").click()
        time.sleep(5)