import random
import re
import time
from datetime import datetime
from playwright.sync_api import Page, expect
from collections import Counter

class Filter:
    def __init__(self, page: Page):
        self.page = page

    def click_Filter(self):
        filter_icon = self.page.get_by_role("button", name="filter Filter")
        expect(filter_icon).to_be_visible()
        filter_icon.click()
        time.sleep(2)

    def select_clinic_normal(self):
        self.page.locator("//form//span[normalize-space()='Clinic']").click()
        time.sleep(1)
        global clinics_selected
        clinics_selected = []
        count = self.page.locator(f"//div[@class='open']//ul[@class='dropdown-menu']/li/label").count()
        for _ in range(count):
            line_number = random.randint(1, count)
            clinic_option = self.page.locator(f"//div[@class='open']//ul[@class='dropdown-menu']/li[{line_number}]/label")
            expect(clinic_option).to_be_visible()
            clinic_option.click()
            clinics_selected.append(clinic_option.text_content().strip())
        self.page.locator("//form//span[normalize-space()='Clinic']").click()

    def select_clinic_Myuser(self):
        self.page.locator("//span[normalize-space()='Clinic']").click()
        global clinics_selected
        clinics_selected = []
        count = self.page.locator(f"//div[@class='open']//ul[@class='dropdown-menu']/li/label").count()
        for _ in range(count):
            line_number = random.randint(1, count)
            clinic_option = self.page.locator(f"//div[@class='open']//ul[@class='dropdown-menu']/li[{line_number}]/label")
            expect(clinic_option).to_be_visible()
            clinic_option.click()
            clinics_selected.append(clinic_option.text_content().strip())
        self.page.locator("//span[normalize-space()='Clinic']").click()

    def select_medical(self):
        time.sleep(2)
        self.page.locator("//span[normalize-space()='Medical Conditions']").click()
        global medical_selected
        medical_selected = []
        options = self.page.locator("//div[@class='open']//li/label")
        total_options = options.count()
        for _ in range(total_options):
            random_index = random.randint(1, total_options-1)  # 0-based index
            medical_option = options.nth(random_index)
            expect(medical_option).to_be_visible()
            medical_option.click()
            time.sleep(1)
            selected_text = medical_option.inner_text().strip()
            medical_selected.append(selected_text)
        self.page.locator("//span[normalize-space()='Medical Conditions']").click()

    def select_program(self):
        self.page.locator("//span[normalize-space()='Programme Duration']").click()
        global program_selected
        program_selected = []
        count = self.page.locator(f"//*[@id='filter-patient']/div/div/div/div/div[2]/div/form/div[3]/div/div/div/ul/li/label").count()
        for _ in range(count):
            line_number = random.randint(1, count)
            program_option = self.page.locator( f"//*[@id='filter-patient']/div/div/div/div/div[2]/div/form/div[3]/div/div/div/ul/li[{line_number}]/label")
            expect(program_option).to_be_visible()
            program_option.click()
            time.sleep(1)
            selected_text = program_option.inner_text().strip()
            program_selected.append(selected_text)
        self.page.locator("//span[normalize-space()='Programme Duration']").click()

    def date_control(self):
        today = datetime.today()
        month = today.month
        pre_month = month - 2 if month > 1 else 12  # Fix for January
        date = today.day
        year = today.year % 100

        global Date_today, Date_pre
        Date_today = f"{date:02d}-{month:02d}-{year:02d}"
        Date_pre = f"{date:02d}-{pre_month:02d}-{year:02d}"
        print(Date_today, "to", Date_pre)

        self.page.get_by_role("button", name="Previous month (PageUp)").click()
        self.page.get_by_role("button", name="Previous month (PageUp)").click()
        # self.page.get_by_role("button", name="Previous month (PageUp)").click()

        time.sleep(1)
        self.page.get_by_title(f"{pre_month}/{date}/").locator("div").click()
        time.sleep(1)
        self.page.get_by_role("button", name="Next month (PageDown)").click()
        self.page.get_by_role("button", name="Next month (PageDown)").click()

        time.sleep(1)
        self.page.get_by_title(f"{month}/{date}/").locator("div").click()
        time.sleep(1)

    def select_all_date(self):
        time.sleep(1)
        self.page.locator("(//input[@placeholder='Start date'])[1]").click()
        self.date_control()
        self.page.locator("(//input[@placeholder='Start date'])[2]").click()
        self.date_control()
        self.page.locator("(//input[@placeholder='Start date'])[3]").click()
        self.date_control()

    def select_BP_Logged(self):
        self.page.locator("label").filter(has_text="Yes").locator("span").click()

    def click_done(self):
        self.page.get_by_role("button", name="Done").click()

    def filter_validation_doctor_user(self, f):
        time.sleep(10)

        try:
            self.page.locator("//td[normalize-space()='No results found']")

        except TimeoutError:
            clinical = self.page.locator("//tbody/tr/td[4]").inner_text().strip()

            counted = Counter(clinics_selected)
            filtered_clinics = [item for item in clinics_selected if counted[item] not in (2, 4, 6)]
            filtered_clinics = [''.join(word[0] for word in item.split()).title() for item in filtered_clinics]
            clinical_list = [item.strip() for item in clinical.split(",")]
            assert any(item in filtered_clinics for item in clinical_list), f"No expected match in Clinical list → {clinical_list}"

    def filter_validation(self, f):
        time.sleep(10)

        try:
            self.page.locator("//td[normalize-space()='No results found']")

        except TimeoutError:
            clinical = self.page.locator("//tbody/tr[1]/td[2]").inner_text().strip()
            app_setup = self.page.locator("//tbody/tr[1]/td[3]").inner_text().strip()



            counted = Counter(clinics_selected)
            filtered_clinics = [item for item in clinics_selected if counted[item] not in (2, 4, 6)]
            filtered_clinics = [''.join(word[0] for word in item.split()).title() for item in filtered_clinics]
            clinical_list = [item.strip() for item in clinical.split(",")]
            assert any(item in filtered_clinics for item in clinical_list), f"No expected match in Clinical list → {clinical_list}"
            print(f"✅ Found: At least one expected item matched in Clinical → {clinical_list}")
            if f == 1:
                last_device_sync = self.page.locator("//tbody/tr[1]/td[4]").inner_text().strip()
                last_consult = self.page.locator("//tbody/tr[1]/td[5]").inner_text().strip()
                medical_condition = self.page.locator("//tbody/tr[1]/td[6]").inner_text().strip()
                programme_duration = self.page.locator("//tbody/tr[1]/td[8]").inner_text().strip()

                counted = Counter(medical_selected)
                filtered_medical = [item for item in medical_selected if counted[item] not in (2, 4, 6)]
                medical_condition_list = [item.strip() for item in medical_condition.split(",")]
                assert any(item in filtered_medical for item in medical_condition_list), f"No expected match in Medical Condition list → {medical_condition_list}"
                print(f"✅ Found: At least one expected item matched in Medical Condition → {medical_condition_list}")

                counted = Counter(program_selected)
                filtered_program = [item for item in program_selected if counted[item] not in (2, 4, 6)]
                programme_duration_list = [item.strip() for item in programme_duration.split(",")]
                assert any(item in filtered_program for item in programme_duration_list), f" No expected match in Programme Duration list → {programme_duration_list}"


                last_device_sync = datetime.strptime(last_device_sync, "%d-%m-%y")
                last_consult = datetime.strptime(last_consult, "%d-%m-%y")

                assert Date_pre <= last_device_sync <= Date_today, f" Last Device Sync date {last_device_sync.strftime('%d-%m-%y')} is outside the range."


                assert Date_pre <= last_consult <= Date_today, f"Last Consult date {last_consult.strftime('%d-%m-%y')} is outside the range."

            # Example: converting your string dates to datetime for comparison
            app_setup = datetime.strptime(app_setup, "%d-%m-%y")

            # Replace these with actual datetime values as per your logic
            # Example format: Date_pre = datetime.strptime("13-04-25", "%d-%m-%y")
            assert Date_pre <= app_setup <= Date_today, f" App Setup date {app_setup.strftime('%d-%m-%y')} is outside the range."
            print("✅ App Setup date is within the range.")

    def cancel_filter(self):
        self.page.get_by_role("img", name="chip-remove").last.click()

    def my_user_filter(self):
        try:
            self.click_Filter()
            self.select_clinic_Myuser()
            self.select_medical()
            self.select_program()
            self.select_all_date()
            self.click_done()
            self.filter_validation(1)
            self.cancel_filter()
            self.page.reload()
            time.sleep(6)
        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"

    def normal_filter(self):
        try:
            self.click_Filter()
            self.select_clinic_normal()
            self.select_all_date()
            self.select_BP_Logged()
            self.click_done()
            self.filter_validation(0)
            self.cancel_filter()
            self.page.reload()
            time.sleep(6)
        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"

    def doctor_user_filter(self):
        try:
            time.sleep(6)
            self.click_Filter()
            self.select_clinic_normal()
            self.click_done()
            self.filter_validation_doctor_user(0)
            time.sleep(2)
        except Exception as e:
            self.page.reload()
            assert False, f"Test failed and page reloaded. Error: {e}"






