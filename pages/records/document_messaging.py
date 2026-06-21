import time
from playwright.sync_api import Page, expect


class DocumentMessaging:
    def __init__(self, page: Page):
        self.page = page

    def select_document_checkbox(self):
        record_checkbox = self.page.get_by_role("cell").filter(has_text="No data").locator("span").nth(1)
        expect(record_checkbox).to_be_enabled()
        record_checkbox.click()

    def send_message_to_user(self):
        self.page.locator(".broadcast-img > .ng-star-inserted").click()
        send_message = self.page.locator("div[id='one-to-one-message-documents'] textarea[placeholder='Type message here']")
        send_message.click()
        send_message.clear()
        time.sleep(2)
        send_message.type("Have a good day.", delay=100)
        time.sleep(2)
        self.page.locator("#one-to-one-message-documents").get_by_text("Send", exact=True).click()
        self.page.get_by_role("button", name="Dismiss").click()
        time.sleep(3)



