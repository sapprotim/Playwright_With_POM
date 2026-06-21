import re

class UserMetricsPage:
    def __init__(self, page):
        self.page = page

    def navigate_to_user_metrics(self):
        self.page.get_by_text("Fullerton Health Organization").click()
        self.page.locator("a").filter(has_text=re.compile(r"^Users$")).click()
        self.page.get_by_role("link", name="User Metrics").click()
        self.page.locator("//img[@title='Refresh']").click()