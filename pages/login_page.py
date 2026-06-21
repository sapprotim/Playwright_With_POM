import re
import time
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://hpb-uat.connectedlife.io/#/login"

    def login(self, username, password, otp):
        self.page.goto(self.url)
        self.page.fill("input[name='username']", username)
        self.page.fill("input[name='password']", password)
        self.page.click("input[value='Sign In']")
        self.page.wait_for_timeout(3000)  # 3 seconds
        self.page.fill("input[id='inp']", str(otp))
        self.page.click("input[value='Submit']")
        time.sleep(10)
