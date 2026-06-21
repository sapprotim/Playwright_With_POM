import time
import re
from playwright.sync_api import Page, expect

class RoleManagerPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_role_manager(self):
        role_manager_button = self.page.locator("div").filter(has_text=re.compile(r"^Role Manager$"))
        expect(role_manager_button).to_be_visible()
        role_manager_button.click()
        time.sleep(2)