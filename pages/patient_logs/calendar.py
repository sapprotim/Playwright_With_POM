from datetime import datetime
import random
import time
from playwright.sync_api import Page, expect


class CalendarPage:
    def __init__(self, page: Page):
        self.page = page

    def calendar_click(self):
        self.page.locator(".date-picker-wrap").click()
        try:
            today_date = datetime.today().strftime("%-m/%-d/")
        except ValueError:
            today_date = datetime.today().strftime("%#m/%#d/")

        calendar_date_select = self.page.get_by_title(today_date).locator("div")
        calendar_date_select.click()
        time.sleep(2)