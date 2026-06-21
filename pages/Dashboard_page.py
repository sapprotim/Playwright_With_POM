import time
from playwright.sync_api import Page, expect

class Dashboardpage:
    def __init__(self, page: Page):
        self.page = page
        self.user_list_title = "//div[@class='user-list-title']"
        self.total_users = "text=Total"

    def verify_my_users_visible(self):
        title = self.page.locator(self.user_list_title)
        expect(title).to_be_visible()
        expect(title).to_have_text("My Users")
        time.sleep(3)

    def click_total_users(self):
        total = self.page.get_by_text("Total")
        expect(total).to_be_visible()
        total.click()