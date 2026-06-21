import time
from playwright.sync_api import Page

class Delete:
    def __init__(self, page: Page):
        self.page = page

    def delete_click(self):
        try:
            self.page.locator("//tbody/tr[1]/td[5]/div[1]/img[2]").first.click()
        except Exception:
            self.page.locator("//img[@src='./assets/images/delete.png']").first.click()

    def delete_confirm(self):
        # self.page.locator("//button[normalize-space()='Delete Blake Ball']").click()
        # self.page.locator("//button[normalize-space()='Delete Fullerton Health Admin']").click()
        # self.page.locator("//div[@class='ng-star-inserted']//div[@class='ack-dismiss']/button[2]").click()
        self.page.locator(".btn.btn-primary.delete-medi-btn", has_text="Delete").click()


    def delete_cancel(self):
        self.page.get_by_role("button", name="Cancel").click()

    def delete_clinic(self):
        self.page.locator("//tbody/tr[1]/td[1]/img[1]").click()
        self.page.locator("//tr[2]//img[@src='./assets/images/delete.png']").click()
        self.page.locator("//button[normalize-space()='Delete Clinic']").click()
        self.page.locator("#department-success-message").get_by_text("Dismiss").click()


    def delete_FH(self):
        self.page.locator("//img[@src='./assets/images/delete.png']").click()
        self.page.locator("//div[@class='modal-content']//div[@class='modal-body']//div//button[@class='btn btn-primary delete-medi-btn'][normalize-space()='Delete Fullerton Health']").click()
        self.page.locator("//div[@id='success-message']//button[@class='btn btn-primary ack-dismiss-btn-custom'][normalize-space()='Dismiss']").click()











