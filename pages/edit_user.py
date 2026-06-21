from PIL.ImagePalette import random
from playwright.sync_api import Page, expect
import time
import random
from playwright.sync_api import TimeoutError
from .phone_number import generate_fake_sg_phone


class EditWorkflowPage:
    def __init__(self, page: Page):
        self.page = page


    def role_Org_doc_edit_user(self):
        edit_button = self.page.get_by_role("link", name="Edit").first
        expect(edit_button).to_be_visible()
        edit_button.click()

    def edit_myuser(self):
        # edit_button = self.page.locator("//a[normalize-space()='Edit']")
        edit_button = self.page.locator("//tbody/tr[1]/td[10]/div[1]/a[1]")
        expect(edit_button).to_be_visible()
        edit_button.click()

    def edit_user_functions(self):
        for section in [
            "Physical Measures", "Smoking / Drinking",
            "Stress", "Physical Activity", "Eating Practices", "Preferences"
        ]:

            tab = self.page.get_by_text(section, exact=True)
            expect(tab).to_be_visible()
            tab.click()

        chronic_conditions = self.page.get_by_text("Chronic Medical Conditions")
        expect(chronic_conditions).to_be_visible()
        chronic_conditions.click()

        clinic_option = self.page.get_by_text("Change Clinic")
        expect(clinic_option).to_be_visible()
        clinic_option.click()

        # clinic_dropdown = self.page.get_by_role("textbox", name="Clinic")
        # clinic_dropdown.click()
        # time.sleep(2)
        #
        # # Open the dropdown tray
        # options = self.page.locator("//div[@class='dropdown open']//ul[@class='dropdown-menu']/li")
        # option_count = options.count()
        #
        # # Pick a random index (1-based for XPath)
        # # Get all options and count them
        # random_index = random.randint(1, option_count)
        # # clinic_option = self.page.locator(f"//div[@id='add-patient']//li[{random_index}]")
        # clinic_option = self.page.locator(f"//div[@class='dropdown open']//ul[@class='dropdown-menu']/li[{random_index}]")
        # expect(clinic_option).to_be_visible()
        # clinic_option.click()

        try:
            # Try main Save + Dismiss sequence
            self.page.locator("//div[normalize-space()='Save Changes']").click(timeout=5000)
            self.page.get_by_role("button", name="Dismiss").click(timeout=5000)
            time.sleep(5)

        except Exception as e:

            clinic_dropdown = self.page.get_by_role("textbox", name="Clinic")
            clinic_dropdown.click()

            options = self.page.locator("//div[@class='dropdown open']//ul[@class='dropdown-menu']/li")
            option_count = options.count()
            # Pick a random index (1-based for XPath)
            random_index = random.randint(1, option_count)
            clinic_option = self.page.locator(f"//div[@class='dropdown open']//ul[@class='dropdown-menu']/li[{random_index}]")
            expect(clinic_option).to_be_visible()
            clinic_option.click()
            self.page.locator("//div[normalize-space()='Save Changes']").click()
            self.page.get_by_role("button", name="Dismiss").click()
            time.sleep(5)


    def edit_user(self):
        try:
            self.edit_myuser()
            self.edit_user_functions()
        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"

    def edit_roleOrg_doc_user(self):
        try:
            self.role_Org_doc_edit_user()
            self.edit_user_functions()
        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"

    def edit_userORG(self):
        try:
            self.page.locator("//img[@src='./assets/images/edit.png']").first.click()
            self.edit_user_functions()
        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"