import os
import time
from playwright.sync_api import Page, expect
from pytest_html.extras import image


class DocumentUploader:
    def __init__(self, page: Page):
        self.page = page

    def click_upload_button(self):
        try:
            upload_link = self.page.get_by_role("link", name="+ Upload Document")
            expect(upload_link).to_be_visible(timeout=3000)
            upload_link.click()
        except Exception:
            fallback_upload = self.page.get_by_role("link", name="Upload Files")
            expect(fallback_upload).to_be_visible(timeout=3000)
            fallback_upload.click()
        time.sleep(2)

    def upload_document_file(self):
        image_path = os.path.abspath('An_image_portraying_a_modern_professional_lifestyle.jpg')
        self.page.set_input_files("//input[@type='file']", image_path)
        time.sleep(2)

        upload_all_btn = self.page.get_by_role("button", name="Upload & Share")
        expect(upload_all_btn).to_be_enabled()
        upload_all_btn.click()
        time.sleep(2)

        self.page.get_by_placeholder("Type message here").click()
        self.page.get_by_placeholder("Type message here").type("Take Care of your health.", delay=100)
        self.page.get_by_text("Confirm & Send").click()
        time.sleep(2)
