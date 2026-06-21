import time
from re import search
import pytest
from pages.user_metrics_page import UserMetricsPage
from pages.login_page import LoginPage
from pages.sort_page import SortPage
from pages.search_page import SearchPage
from pages.hpb_Menu import AdminPage
from pages.refresh import RefreshablePage
from pages.pagination import PaginationPage
from playwright.sync_api import Page
from pages.Edit_Clinic_admin import EditClinic
from pages.Edit_doctor_admin import Editdector
from pages.Delete import Delete
from pages.Doctor_Users_page import Doctoruserpage
from pages.edit_user import EditWorkflowPage
from pages.Filter import Filter
from pages.user_basic_info.wellness_score_tab import WellnessScoreTab
from pages.re_invite import re_invite
from pages.Customer_Type import CustomerType
from data import FA_Admin_email, FA_Admin_password, FA_Admin_otp, fh_admin, clinic_admin, doctor_name, search_user, search_item, withdrawn_user
import pytest
from playwright.sync_api import Page



# --- Simple memory-based tracking ---
passed_steps = {
    "login": False,
    "select_fullerton_admin": False,
    "select_clinic": False,
    "select_doctor_admin": False,
    "roleFHA_search_doctor": False,
    "select_doctor_users_page": False,
    "select_Prospects": False,
    "select_user": False,
    "select_invite_user": False,
    "select_withdrawn_user": False,
    "navigate_to_user_metrics": False
}


# --- Helper functions ---
def do_loginFHA(page: Page):
    login_page = LoginPage(page)
    login_page.login(FA_Admin_email, FA_Admin_password, FA_Admin_otp)

def do_select_fullerton_admin(page: Page):
    admin = AdminPage(page)
    admin.select_fullerton_admin()

def do_select_clinic(page: Page):
    admin = AdminPage(page)
    admin.select_clinic()

def do_select_doctor_admin(page: Page):
    admin = AdminPage(page)
    admin.select_doctor_admin()

def do_roleFHA_search_doctor(page: Page):
    search_page = SearchPage(page)
    search_term = doctor_name # Replace with test name
    search_page.search_function(search_term)

def do_select_doctor_users_page(page: Page):
    select = SearchPage(page)
    select.perform_search(doctor_name)
    user_page = Doctoruserpage(page)
    user_page.select_doctor_users_page()

def do_select_Prospects(page: Page):
    prospect_page = AdminPage(page)
    prospect_page.select_Prospects()

def do_select_user(page: Page):
    user_list = AdminPage(page)
    user_list.select_user()

def do_select_invite_user(page: Page):
    invite_user = AdminPage(page)
    invite_user.select_invite_user()

def do_select_withdrawn_user(page: Page):
    Withdrawn_page = AdminPage(page)
    Withdrawn_page.select_withdrawn_user()

def do_navigate_to_user_metrics(page: Page):
    metrics = UserMetricsPage(page)
    metrics.navigate_to_user_metrics()


# ----------------------------- #
# login_flow TEST CASES (roleCA)
# --

def test_roleFHA_login_flow(page: Page):
    do_loginFHA(page)
    passed_steps["login"] = True

# ----------------------------- #
# Organization View PAGE TEST CASES (roleFHA)
# --

def test_roleFHA_HPB_Org_ref(page: Page):
    if not (passed_steps["login"]):
        do_loginFHA(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

# ----------------------------- #
# Fullerton Health Admin PAGE TEST CASES (roleFHA)
# --

def test_roleFHA_click_admin(page: Page):
    if not (passed_steps["login"]):
        do_loginFHA(page)
    do_select_fullerton_admin(page)
    passed_steps["select_fullerton_admin"] = True

def test__roleFHA_FHA_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["select_fullerton_admin"]):
        do_loginFHA(page)
        do_select_fullerton_admin(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

def test_roleFHA_FHA_page(page: Page):
    if not (passed_steps["login"] and passed_steps["select_fullerton_admin"]):
        do_loginFHA(page)
        do_select_fullerton_admin(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleFHA_sort_by_name_and_last_sign_in(page : Page):
    if not (passed_steps["login"] and passed_steps["select_fullerton_admin"]):
        do_loginFHA(page)
        do_select_fullerton_admin(page)
    sort = SortPage(page)
    sort.sort_by_name_az_and_last_sign_in()

def test_roleFHA_search_functionality(page: Page):
    if not (passed_steps["login"] and passed_steps["select_fullerton_admin"]):
        do_loginFHA(page)
        do_select_fullerton_admin(page)
    search_page = SearchPage(page)
    search_term = fh_admin  # You can replace this with any valid term
    search_page.search_function(search_term)

# ----------------------------- #
# CLINICAL ADMIN PAGE TEST CASES (roleFHA)
# --

def test_roleFHA_CAP_click_clinic_admin(page: Page):
    if not (passed_steps["login"]):
        do_loginFHA(page)
    do_select_clinic(page)
    passed_steps["select_clinic"] = True

def test_roleFHA_CAP_refresh_page(page: Page):
    if not (passed_steps["login"] and passed_steps["select_clinic"]):
        do_loginFHA(page)
        do_select_clinic(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

def test_roleFHA_CAP_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["select_clinic"]):
        do_loginFHA(page)
        do_select_clinic(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleFHA_CAP_sort_name_last_signin(page: Page):
    if not (passed_steps["login"] and passed_steps["select_clinic"]):
        do_loginFHA(page)
        do_select_clinic(page)
    sort = SortPage(page)
    sort.sort_by_name_az_and_last_sign_in()

def test_roleFHA_CAP_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["select_clinic"]):
        do_loginFHA(page)
        do_select_clinic(page)
    search_page = SearchPage(page)
    search_term = clinic_admin # Replace with test name
    search_page.search_function(search_term)

# ----------------------------- #
# Doctor ADMIN PAGE TEST CASES (roleFHA)
# --

def test_roleFHA_DP_click_doctor_admin(page: Page):
    if not (passed_steps["login"]):
        do_loginFHA(page)
    do_select_doctor_admin(page)
    passed_steps["select_doctor_admin"] = True


def test_roleFHA_DP_refresh_page(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

def test_roleFHA_DP_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleFHA_DP_sort_name_last_signin(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
    sort = SortPage(page)
    sort.sort_by_name_az_and_last_sign_in()

def test_roleFHA_DP_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
    do_roleFHA_search_doctor(page)
    passed_steps["roleFHA_search_doctor"] = True


def test_roleFHA_DP_admin_Edit_flow(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["roleFHA_search_doctor"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
        do_roleFHA_search_doctor(page)
    clinic = Editdector(page)
    clinic.edit_dector()

def test_roleFHA_doctor_admin_delete(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
    search = SearchPage(page)
    search.perform_search(doctor_name)
    doctor_delete = Delete(page)
    doctor_delete.delete_click()
    # doctor_delete.delete_confirm()
    doctor_delete.delete_cancel()

def test_roleFHA_roleFHA_Doctor_users(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
    do_select_doctor_users_page(page)
    passed_steps["select_doctor_users_page"] = True

def test_roleFHA_Doctor_users_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["select_doctor_users_page"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
        do_select_doctor_users_page(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleFHA_Doctor_users_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["select_doctor_users_page"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
        do_select_doctor_users_page(page)
    search_page = SearchPage(page)
    search_term = search_user # Replace with test name
    search_page.search_function(search_term)

def test_roleFHA_Doctor_users_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["select_doctor_users_page"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
        do_select_doctor_users_page(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleFHA_Doctor_users_filter(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["select_doctor_users_page"]):
        do_loginFHA(page)
        do_select_doctor_admin(page)
        do_select_doctor_users_page(page)
    user_page = Filter(page)
    user_page.doctor_user_filter()

# ----------------------------- #
# prospect PAGE TEST CASES (roleFHA)
# --
#
def test_roleFHA_prospect_page(page: Page):
    if not (passed_steps["login"]):
        do_loginFHA(page)
    do_select_Prospects(page)
    passed_steps["select_Prospects"] = True

def test_roleFHA_prospect_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["select_Prospects"]):
        do_loginFHA(page)
        do_select_Prospects(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleFHA_prospect_search(page: Page):
    if not (passed_steps["login"] and passed_steps["select_Prospects"]):
        do_loginFHA(page)
        do_select_Prospects(page)
    search_page = SearchPage(page)
    search_term = search_item  # Replace with test name
    search_page.search_function(search_term)

def test_roleFHA_prospect_calander(page: Page):
    if not (passed_steps["login"] and passed_steps["select_Prospects"]):
        do_loginFHA(page)
        do_select_Prospects(page)
    calander = WellnessScoreTab(page)
    calander.calendar_filter_dropdown()

def test_roleFHA_prospect_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["select_Prospects"]):
        do_loginFHA(page)
        do_select_Prospects(page)
    user_page = PaginationPage(page)
    user_page.pagination()



# ----------------------------- #
# User List PAGE TEST CASES (roleFHA)
# --

def test_roleFHA_Assigned_user_page(page: Page):
    if not (passed_steps["login"]):
        do_loginFHA(page)
    do_select_user(page)
    passed_steps["select_user"] = True

def test_roleFHA_Assigned_user_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"]):
        do_loginFHA(page)
        do_select_user(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleFHA_Assigned_user_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"]):
        do_loginFHA(page)
        do_select_user(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleFHA_Assigned_users_filter(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"]):
        do_loginFHA(page)
        do_select_user(page)
    user_page = Filter(page)
    user_page.normal_filter()

def test_roleFHA_Assigned_user_search(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"]):
        do_loginFHA(page)
        do_select_user(page)
    search_page = SearchPage(page)
    search_term = search_user  # Replace with test name
    search_page.search_function(search_term)

# ----------------------------- #
# Invite User PAGE TEST CASES (roleFHA)
# --

def test_roleFHA_invite_user_page(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"]):
        do_loginFHA(page)
        do_select_user(page)
    do_select_invite_user(page)
    passed_steps["select_invite_user"] = True

def test_roleFHA_invite_user_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"] and passed_steps["select_invite_user"]):
        do_loginFHA(page)
        do_select_user(page)
        do_select_invite_user(page)
    invite_user = RefreshablePage(page)
    invite_user.refresh()

def test_roleFHA_invite_invite_user_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"] and passed_steps["select_invite_user"]):
        do_loginFHA(page)
        do_select_user(page)
        do_select_invite_user(page)
    invite_user = PaginationPage(page)
    invite_user.pagination()

def test_roleFHA_invite_user_search(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"] and passed_steps["select_invite_user"]):
        do_loginFHA(page)
        do_select_user(page)
        do_select_invite_user(page)
    search_page = SearchPage(page)
    search_term = search_item # Replace with test name
    search_page.search_function_Invited_Users(search_term)

def test_roleFHA_invite_user_re_invite(page : Page):
    if not (passed_steps["login"] and passed_steps["select_user"] and passed_steps["select_invite_user"]):
        do_loginFHA(page)
        do_select_user(page)
        do_select_invite_user(page)
    reinvite = re_invite(page)
    reinvite.re_invite()

# ----------------------------- #
# Invite User PAGE TEST CASES (roleFHA)
# --

def test_roleFHA_Withdrawn_user_page(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"]):
        do_loginFHA(page)
        do_select_user(page)
    do_select_withdrawn_user(page)
    passed_steps["select_withdrawn_user"] = True


def test_roleFHA_Withdrawn_user_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"] and passed_steps["select_withdrawn_user"]):
        do_loginFHA(page)
        do_select_user(page)
        do_select_withdrawn_user(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleFHA_Withdrawn_invite_user_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"] and passed_steps["select_withdrawn_user"]):
        do_loginFHA(page)
        do_select_user(page)
        do_select_withdrawn_user(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleFHA_Withdrawn_user_search(page: Page):
    if not (passed_steps["login"] and passed_steps["select_user"] and passed_steps["select_withdrawn_user"]):
        do_loginFHA(page)
        do_select_user(page)
        do_select_withdrawn_user(page)
    search_page = SearchPage(page)
    search_term = withdrawn_user # Replace with test name
    search_page.search_function(search_term)

# ----------------------------- #
# User metrics User PAGE TEST CASES (roleFHA)
# --

def test_user_metrics_navigation(page):
    if not (passed_steps["login"]):
        do_loginFHA(page)
    do_navigate_to_user_metrics(page)
    passed_steps["navigate_to_user_metrics"] = True

def test_roleFHA_user_metrics_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["navigate_to_user_metrics"]):
        do_loginFHA(page)
        do_navigate_to_user_metrics(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleFHA_user_metrics_calander(page: Page):
    if not (passed_steps["login"] and passed_steps["navigate_to_user_metrics"]):
        do_loginFHA(page)
        do_navigate_to_user_metrics(page)
    calander = WellnessScoreTab(page)
    calander.calendar_filter_dropdown()

def test_roleFHA_user_metrics_customerType(page: Page):
    if not (passed_steps["login"] and passed_steps["navigate_to_user_metrics"]):
        do_loginFHA(page)
        do_navigate_to_user_metrics(page)
    customerType = CustomerType(page)
    customerType.customtype()