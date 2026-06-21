import re
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.Dashboard_page import Dashboardpage
from pages.pagination import PaginationPage
from pages.refresh import RefreshablePage
from pages.search_page import SearchPage
from pages.headers import UserHeader
from pages.sort_function import UserTableSort
from pages.reset_sort import ResetSort
from pages.edit_user import EditWorkflowPage
from pages.user_profile import UserProfileSearch
from pages.user_basic_info.user_BasicInfo import UserBasicInfoPage
from pages.user_basic_info.trends_comparison import UserComparisonPage
from pages.user_basic_info.wellness_score_tab import WellnessScoreTab
from pages.patient_logs.PatientLogs_page import PatientLogsPage
from pages.patient_logs.calendar import CalendarPage
from pages.patient_logs.BP import BloodPressurePage
from pages.patient_logs.FBG import GlucosePage
from pages.patient_logs.HbA1c import HbA1cPage
from pages.patient_logs.weight_bmi import BodyShapePage
from pages.patient_logs.WC import WCPage
from pages.patient_logs.data_Validation import DataValidation
from pages.patient_logs.lipids import LipidsPage
from pages.records.records_page import RecordsPage
from pages.records.upload_document import DocumentUploader
from pages.records.document_messaging import DocumentMessaging
from pages.wellness_plan import Wellnessplan
from pages.Filter import Filter
from data import Doctor_Admin_email, Doctor_Admin_password, Doctor_Admin_otp, search_user
import pytest
from pages.clinical_ws_score import validate_clinical_score
from pages.lifestyle_ws_score import validation_lifestyle_score
from playwright.sync_api import Page

# --- Simple memory-based tracking ---
passed_steps = {
    "login": False,
    "profile": False,
    "patient_log": False,
    "records": False,
    "upload_document": False
}

# --- Helper functions ---
def do_login(page: Page):
    login_page = LoginPage(page)
    login_page.login(Doctor_Admin_email, Doctor_Admin_password, Doctor_Admin_otp)

def do_user_profile(page: Page):
    user_profile = UserProfileSearch(page)
    user_profile.search_user_profile()

def do_user_profile_patient_log(page: Page):
    Patient_Logs = PatientLogsPage(page)
    Patient_Logs.navigate_to_patient_logs()

def do_records(page: Page):
    records = RecordsPage(page)
    records.navigate_to_records_files()
    records.click_files()

def do_upload_document(page: Page):
    uploader = DocumentUploader(page)
    uploader.click_upload_button()
    uploader.upload_document_file()

# ----------------------------- #
# login_flow TEST CASES (roleDA)
# --

def test_roleDoc_login_flow(page: Page):
    do_login(page)
    passed_steps["login"] = True

# # ----------------------------- #
# # My_users TEST CASES (roleDA)
# # --

def test_roleDoc_my_users_page(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    dashboard = Dashboardpage(page)
    dashboard.verify_my_users_visible()

def test_roleDoc_my_users_total(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    dashboard = Dashboardpage(page)
    dashboard.click_total_users()

def test_roleDoc_my_users_pagination(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleDoc_my_users_page_Search(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    search_page = SearchPage(page)
    search_term = search_user  # Replace with test name
    search_page.search_function(search_term)

def test_roleDoc_my_users_page_Refresh(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    refresh_page = RefreshablePage(page)
    refresh_page.refresh()

def test_roleDoc_user_list_table_header(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    headers_text = UserHeader(page)
    headers_text.verify_roledoc_my_users_headers()

def test_roleDoc_user_list_table_Sort(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    cell_sort = UserTableSort(page)
    cell_sort.sort_user_table()

def test_roleDoc_Reset_Sort(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    reset_sort = ResetSort(page)
    reset_sort.Reset_Sort()

def test_roleDoc_edit(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    edit_page = EditWorkflowPage(page)
    edit_page.edit_user()

def test_roleDoc_users_filter(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    user_page = Filter(page)
    user_page.my_user_filter()

# ----------------------------- #
# User Profile TEST CASES (roleDA)
# --

def test_roleDoc_user_profile(page: Page):
    if not (passed_steps["login"]):
        do_login(page)
    do_user_profile(page)
    passed_steps["profile"] = True

def test_roleDoc_user_basic_info_section(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    basic_info_section = UserBasicInfoPage(page)
    basic_info_section.verify_basic_info()
    basic_info_section.verify_body_info()
    basic_info_section.verify_vital_info()
    basic_info_section.verify_last_updated()
    basic_info_section.verify_onboarding_date()

# ----------------------------- #
# User Profile -> Trends page TEST CASES (roleDA)
# --

def test_roleDoc_comparison_watch_clinical(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    comparison = UserComparisonPage(page)
    comparison.verify_clinical_comparison_selection()

def test_roleDoc_comparison_watch_lifestyle(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    comparison = UserComparisonPage(page)
    comparison.verify_lifestyle_comparison_selection()

def test_roleDoc_visibility_of_sections(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    comparison = UserComparisonPage(page)
    comparison.verify_clinical_comparison_selection()
    comparison.verify_lifestyle_comparison_selection()
    comparison.verify_dashboard_sections_visibility()

def test_roleDoc_clinical_value_format(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.verify_clinical_value_format()

def test_roleDoc_all_clinical_elements(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.verify_all_clinical_elements()

def test_roleDoc_lifestyle_tab_navigation(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.navigate_to_lifestyle_tab()

def test_roleDoc_lifestyle_value_format(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.verify_lifestyle_value_format()

def test_roleDoc_all_lifestyle_elements(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.verify_all_lifestyle_elements()

def test_roleDoc_calendar_filter_dropdown(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.calendar_filter_dropdown()

def test_roleDoc_view_filter_buttons(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.view_filter_buttons()

def test_roleDoc_calendar_parameter_images(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.calendar_parameter_images()

def test_roleDoc_generate_wellness_plan_button(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = WellnessScoreTab(page)
    wellness.verify_generate_wellness_plan_button()

# ----------------------------- #
# User Profile -> Patient_Logs page TEST CASES (roleDA)
# --

def test_roleDoc_Navigation_Patient_Logs_page(page: Page):
    do_user_profile_patient_log(page)
    passed_steps["patient_log"] = True

def test_roleDoc_patient_logs_calendar(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    calendar_visibility = CalendarPage(page)
    calendar_visibility.calendar_click()

def test_roleDoc_patient_logs_blood_pressure(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    bp = BloodPressurePage(page)
    bp.add_blood_pressure()

def test_roleDoc_patient_logs_fasting_blood_glucose(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    glucose = GlucosePage(page)
    glucose.add_fasting_blood_glucose()
    glucose.edit_fasting_blood_glucose()

def test_roleDoc_patient_logs_add_or_edit_hba1c(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    HbA1c = HbA1cPage(page)
    HbA1c.add_or_edit_hba1c()

def test_roleDoc_patient_logs_weight_bmi(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    weight_bmi = BodyShapePage(page)
    weight_bmi.add_weight_bmi()
    weight_bmi.edit_weight_bmi()

def test_roleDoc_patient_logs_WC(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    wc = WCPage(page)
    wc.WC_Add()
    wc.WC_edit()

def test_roleDoc_validate_BP_data_patient_logs(page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    validator = DataValidation(page)
    validator.validate_blood_pressure()

def test_roleDoc_validate_weight_data_patient_logs(page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    validator = DataValidation(page)
    validator.validate_weight()

def test_roleDoc_validate_BMI_data_patient_logs(page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    validator = DataValidation(page)
    validator.validate_bmi()

def test_roleDoc_validate_WC_data_patient_logs(page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    validator = DataValidation(page)
    validator.validate_waist_circumference()

def test_roleDoc_patient_logs_lipids_entry(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps ["patient_log"]):
        do_login(page)
        do_user_profile(page)
        do_user_profile_patient_log(page)
    lipids_page = LipidsPage(page)
    lipids_page.open_lipids_panel()
    if lipids_page.is_third_lipid_visible():
        lipids_page.edit_lipid_values()
    else:
        lipids_page.add_lipid_values()

# ----------------------------- #
# User Profile -> Records page TEST CASES (roleDA)
# --

def test_roleDoc_navigate_to_records(page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    do_records(page)
    passed_steps["records"] = True

def test_roleDoc_refresh_records(page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps["records"]):
        do_login(page)
        do_user_profile(page)
        do_records(page)
    records = RefreshablePage(page)
    records.refresh()

def test_roleDoc_records_upload_document(page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps["records"]):
        do_login(page)
        do_user_profile(page)
        do_records(page)
    uploader = DocumentUploader(page)
    uploader.click_upload_button()
    uploader.upload_document_file()
    passed_steps["upload_document"] = True

def test_roleDoc_records_select_document_and_send_message(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"] and passed_steps["records"] and passed_steps["upload_document"]):
        do_login(page)
        do_user_profile(page)
        do_records(page)
        do_upload_document(page)
    doc_msg = DocumentMessaging(page)
    doc_msg.select_document_checkbox()
    doc_msg.send_message_to_user()

# ----------------------------- #
# User Profile -> Wellness_plan page TEST CASES (roleDA)
# --

def test_roleDoc_trends_generate_wellness_plan(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    wellness = Wellnessplan(page)
    wellness.Wellness_plan_page()
    wellness.genarate_plan()

def test_validate_clinical_dashboard_score(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    validate_clinical_score(page)

def test_lifestyle_score_validation(page: Page):
    if not (passed_steps["login"] and passed_steps["profile"]):
        do_login(page)
        do_user_profile(page)
    validation_lifestyle_score(page)
