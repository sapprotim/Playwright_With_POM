from playwright.sync_api import Page, expect

class ResetSort:
    def __init__(self, page: Page):
        self.page = page

    def Reset_Sort(self):
        reset_sort = self.page.get_by_role("button", name="Reset Sort")
        expect(reset_sort).to_be_enabled()
        reset_sort.click()