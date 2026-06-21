from playwright.sync_api import Page, expect
import time

class re_invite:
    def __init__(self, page: Page):
        self.page = page
    def re_invite(self):
        self.page.get_by_role("row", name="Details available on").locator("span").nth(1).click()
        self.page.locator("div:nth-child(2) > img").click()
        self.page.get_by_text("Confirm resend").click()
        time.sleep(1)
        self.page.get_by_role("button", name="Dismiss").click()