import time
import re
from playwright.sync_api import Page, expect

class PatientLogsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_patient_logs(self):
        patient_logs_button = self.page.locator("div").filter(has_text=re.compile(r"^Patient Logs$")).nth(1)
        expect(patient_logs_button).to_be_visible()
        patient_logs_button.click()
        time.sleep(2)
