from playwright.sync_api import Page, expect
import time

class UserHeader:
    def __init__(self, page: Page):
        self.page = page

    def verify_roleFHA_user_prospects_headers(self):
        headers = [
            "EMAIL ID", "FORM SUBMISSION", "USER TYPE", "ELIGIBLE",
            "COMPATIBLE FITBIT", "DISCOUNT CODE REDEEMED", "INVITED TO ONBOARD"
        ]
        for text in headers:
            element = self.page.get_by_text(text, exact=True)
            expect(element).to_be_visible()


    def verify_roleFHA_user_lists_headers(self):
        headers = ["NAME", "CLINIC", "APP SETUP", "LAST DEVICE SYNC", "BP LOGGED", "LAST CONSULT"]
        for text in headers:
            element = self.page.get_by_text(text, exact=True)
            expect(element).to_be_visible()


    def verify_roleCA_user_list_headers(self):
        headers = ["NAME", "CLINIC", "APP SETUP"]
        for text in headers:
            element = self.page.get_by_text(text, exact=True)
            expect(element).to_be_visible()


    def verify_roledoc_my_users_headers(self):
        headers = [
            "NAME", "CLINIC", "APP SETUP", "LAST DEVICE SYNC", "LAST CONSULT",
            "MEDICAL CONDITION", "FOLLOW-UP (PCC)", "PROGRAMME DURATION", "ACTION"
        ]
        for text in headers:
            element = self.page.get_by_text(text, exact=True)
            expect(element).to_be_visible()
