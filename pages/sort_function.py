from playwright.sync_api import Page, expect

class UserTableSort:
    def __init__(self, page: Page):
        self.page = page       


    def sort_user_table(self):
        cell = ["NAME", "CLINIC"]
        for name in cell:
            sort_button = self.page.get_by_role("cell", name=name).locator("img")
            expect(sort_button).to_be_visible()
            sort_button.click()