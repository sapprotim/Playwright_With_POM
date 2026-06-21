from playwright.sync_api import Page, expect
import time

class SearchPage:
    def __init__(self, page: Page):
        self.page = page

    def verify_roleFHA_user_prospects_headers(self):
        self.page.fill("input[placeholder='Search']","Partho")
        self.page.locator("//tbody/tr/td[1]").click()
