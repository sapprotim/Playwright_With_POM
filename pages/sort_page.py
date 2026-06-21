from playwright.sync_api import Page, expect
from datetime import datetime
import time

class SortPage:
    def __init__(self, page: Page):
        self.page = page

    def sort_by_name_az_and_assert(self):
        self.page.get_by_role("button", name="Sort").click()
        self.page.get_by_text("Name (A-Z)").click()
        time.sleep(2)

        elements = self.page.locator("//tbody/tr/td[1]")
        count = elements.count()

        for i in range(count):
            text = elements.nth(i).inner_text().strip()
            assert text, f"Row {i + 1} is empty"
            assert text[0].isalpha(), f"Row {i + 1} does not start with a letter: '{text}'"

    def sort_by_last_sign_in_and_assert(self):
        self.page.get_by_role("button", name="Name").click()
        self.page.get_by_text("Last Sign In (Most Recent)").click()
        time.sleep(1)
        elements = self.page.locator("//tbody/tr/td[3]").all()
        datetimes = []
        for el in elements:
            text = el.inner_text().strip()
            if ', ' not in text:
                continue  # skip invalid entries
            try:
                time_part, date_part = text.split(', ')
                day, month, year = date_part.split(' ')
                day = day.zfill(2)
                formatted = f"{time_part}, {day} {month} {year}"
                dt = datetime.strptime(formatted, "%I:%M %p, %d %b %Y")
                datetimes.append(dt)
            except ValueError:
                continue
        assert datetimes == sorted(datetimes, reverse=True), "Last Sign In column is not sorted from newest to oldest"


    def sort_by_name_az_and_last_sign_in(self):
        self.sort_by_name_az_and_assert()
        self.sort_by_last_sign_in_and_assert()


