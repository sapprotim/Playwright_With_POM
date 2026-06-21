import time

from playwright.sync_api import Page, expect

class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator("input[placeholder='Search']")

    def perform_search(self, search_term: str):
        expect(self.search_input).to_be_visible()
        expect(self.search_input).to_be_enabled()
        self.search_input.clear()  # Clear previous input
        self.search_input.type(search_term)
        self.page.wait_for_timeout(2000)  # Wait for results to update

    def verify_search_results(self, search_term: str, column_xpath: str):
        rows = self.page.locator(column_xpath)

        # Wait for results to appear (basic wait logic, could be enhanced with Playwright wait)
        self.page.wait_for_timeout(2000)
        count = rows.count()
        assert count > 0, f"❌ No search results found for term: '{search_term}'"

        expected_parts = [part.strip().lower() for part in search_term.split(",")]
        row_elements = rows.all()

        print(f"\n🔍 Search term: '{search_term}'")
        print("📋 Search results:")
        matched = False

        for row in row_elements:
            text = row.inner_text().strip()
            print(f" - {text}")
            lower_text = text.lower()
            if all(part in lower_text for part in expected_parts):
                matched = True

        if not matched:
            raise AssertionError(f"❌ None of the rows matched all parts of the search term: '{search_term}' {text}")

    def search_function(self, search_term: str):
        self.perform_search(search_term)
        time.sleep(1)
        self.verify_search_results(search_term, "//tbody/tr/td[1]")

    def search_function_FH(self, search_term: str):
        self.perform_search(search_term)
        time.sleep(1)
        self.verify_search_results(search_term, "//tbody/tr[1]/td[1]/span")

    def search_function_Invited_Users(self, search_term: str):
        self.perform_search(search_term)
        self.verify_search_results(search_term, "//tbody/tr/td[3]")

    def search_function_clinic(self, search_term: str):
        self.perform_search(search_term)
        self.verify_search_results(search_term, "//div[@class='d-flex-center-start']//div")