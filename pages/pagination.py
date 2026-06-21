from playwright.sync_api import Page, expect

class PaginationPage:
    def __init__(self, page: Page):
        self.page = page

    def select_page_size_10(self):
        self.page.locator("//img[@title='Refresh']").click()
        self.page.get_by_role("button", name="10").click()
        self.page.locator("[id=\"\\31 0\"]").click()

    def select_page_size_20(self):
        self.page.get_by_role("button", name="10").click()
        self.page.locator("[id='\\32 0']").click()

    def select_page_size_30(self):
        self.page.get_by_role("button", name="20").click()
        self.page.locator("[id='\\33 0']").click()

    def select_page_size_40(self):
        self.page.get_by_role("button", name="30").click()
        self.page.locator("[id='\\34 0']").click()

    def select_page_size_50(self):
        self.page.get_by_role("button", name="40").click()
        self.page.locator("[id='\\35 0']").click()

    def pagination(self):
        self.select_page_size_10()
        self.select_page_size_20()
        self.select_page_size_30()
        self.select_page_size_40()
        self.select_page_size_50()

