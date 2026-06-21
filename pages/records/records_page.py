import time
from playwright.sync_api import Page, expect

class RecordsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_records_files(self):
        records_link = self.page.get_by_role("link", name="Records")
        expect(records_link).to_be_visible()
        records_link.click()
        time.sleep(2)

    def click_files(self):
        files_tab = self.page.get_by_role("button", name="Files")
        expect(files_tab).to_be_enabled()
        files_tab.click()
        time.sleep(2)
        files_section = self.page.locator("#Files")
        expect(files_section).to_be_enabled()
        files_section.click()
        time.sleep(2)
