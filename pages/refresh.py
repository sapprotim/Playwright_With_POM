from playwright.sync_api import Page, expect

class RefreshablePage:
    def __init__(self, page: Page):
        self.page = page
        self.refresh_icon = page.locator("//img[@title='Refresh']")

    def refresh(self):
        expect(self.refresh_icon).to_be_visible()
        self.refresh_icon.click()
