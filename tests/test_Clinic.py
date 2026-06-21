from re import search
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
from pages.create.create_doctor import DoctorCreationPage
from pages.create.Create_Clinica import create_clinic_page
from data import Clinic_Admin_email, Clinic_Admin_password, Clinic_Admin_otp, search_user, clinic_admin, doctor_name

import pytest
from playwright.sync_api import Page

# --- Simple memory-based tracking ---
passed_steps = {
    "login": False,
    "open_Organization_View": False,
    "select_clinic": False,
    "select_doctor_admin": False,
    "select_doctor_users_page": False
}

# --- Helper functions ---
def do_loginCA(page: Page):
    login_page = LoginPage(page)
    login_page.login(Clinic_Admin_email, Clinic_Admin_password, Clinic_Admin_otp)

def do_open_Organization_View(page: Page):
    admin = AdminPage(page)
    admin.open_Organization_View()

def do_select_clinic(page: Page):
    clinic_admin = AdminPage(page)
    clinic_admin.select_clinic()

def do_select_doctor_admin(page: Page):
    admin = AdminPage(page)
    admin.select_doctor_admin()

def do_search_doctor(page: Page):
    search_page = SearchPage(page)
    search_term = doctor_name
    search_page.search_function(search_term)

def do_select_doctor_users_page(page: Page):
    select = SearchPage(page)
    select.perform_search(doctor_name)
    user_page = Doctoruserpage(page)
    user_page.select_doctor_users_page()


# ----------------------------- #
# login_flow TEST CASES (roleCA)
# --

def test_roleCA_HPB_login_flow(page: Page):
    do_loginCA(page)
    passed_steps["login"] = True

# ----------------------------- #
# User PAGE TEST CASES (roleCA)
# --

def test_roleCA_user_ref(page: Page):
    if not (passed_steps["login"]):
        do_loginCA(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleCA_user_pagination(page: Page):
    if not (passed_steps["login"]):
        do_loginCA(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleCA_users_filter(page: Page):
    if not (passed_steps["login"]):
        do_loginCA(page)
    user_page = Filter(page)
    user_page.normal_filter()

def test_roleCA_user_search(page: Page):
    if not (passed_steps["login"]):
        do_loginCA(page)
    search_page = SearchPage(page)
    search_term = search_user  # Replace with test name
    search_page.search_function(search_term)



# ----------------------------- #
# Organization_View PAGE TEST CASES (roleCA)
# --

def test_roleCA_CAP_click_Organization_View(page: Page):
    if not (passed_steps["login"]):
        do_loginCA(page)
    do_open_Organization_View(page)
    passed_steps["open_Organization_View"] = True

def test_roleCA_HPB_Org_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["open_Organization_View"]):
        do_loginCA(page)
        do_open_Organization_View(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

# ----------------------------- #
# CLINICAL ADMIN PAGE TEST CASES (roleCA)
# --

def test_roleCA_CAP_click_clinic_admin(page: Page):
    if not (passed_steps["login"]):
        do_loginCA(page)
    do_select_clinic(page)
    passed_steps["select_clinic"] = True

def test_roleCA_CAP_refresh_page(page: Page):
    if not (passed_steps["login"] and passed_steps["select_clinic"]):
        do_loginCA(page)
        do_select_clinic(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

def test_roleCA_CAP_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["select_clinic"]):
        do_loginCA(page)
        do_select_clinic(page)
    pagination = PaginationPage(page)
    pagination.pagination()


def test_roleCA_CAP_sort_name_last_signin(page: Page):
    if not (passed_steps["login"] and passed_steps["select_clinic"]):
        do_loginCA(page)
        do_select_clinic(page)
    sort = SortPage(page)
    sort.sort_by_name_az_and_last_sign_in()


def test_roleCA_CAP_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["select_clinic"]):
        do_loginCA(page)
        do_select_clinic(page)
    search_page = SearchPage(page)
    search_term = clinic_admin  # Replace with test name
    search_page.search_function(search_term)


# ----------------------------- #
# Doctor ADMIN PAGE TEST CASES (roleCA)
# --

def test_roleCA_click_doctor_admin(page: Page):
    if not (passed_steps["login"]):
        do_loginCA(page)
    do_select_doctor_admin(page)
    passed_steps["select_doctor_admin"] = True

def test_roleCA_DP_refresh_page(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

def test_roleCA_DP_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
    pagination = PaginationPage(page)
    pagination.pagination()


def test_roleCA_DP_sort_name_last_signin(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
    sort = SortPage(page)
    sort.sort_by_name_az_and_last_sign_in()


def test_roleCA_DP_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
    do_search_doctor(page)
    passed_steps["search_doctor"] = True

def test_roleCA_DP_admin_Edit_flow(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["search_doctor"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
        do_search_doctor(page)
    doctor = Editdector(page)
    doctor.edit_dector()

def test_roleCA_doctor_admin_delete(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["search_doctor"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
        do_search_doctor(page)
    doctor_delete = Delete(page)
    doctor_delete.delete_click()
    # doctor_delete.delete_confirm()
    doctor_delete.delete_cancel()


def test_roleCA_doctor_user_page(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
    do_select_doctor_users_page(page)
    passed_steps["select_doctor_users_page"] = True

def test_roledoctor_Doctor_users_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["select_doctor_users_page"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
        do_select_doctor_users_page(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleCA_Doctor_users_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["select_doctor_users_page"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
        do_select_doctor_users_page(page)
    search_page = SearchPage(page)
    search_term = search_user # Replace with test name
    search_page.search_function(search_term)

def test_roleCA_Doctor_users_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["select_doctor_users_page"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
        do_select_doctor_users_page(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleCA_Doctor_users_filter(page: Page):
    if not (passed_steps["login"] and passed_steps["select_doctor_admin"] and passed_steps["select_doctor_users_page"]):
        do_loginCA(page)
        do_select_doctor_admin(page)
        do_select_doctor_users_page(page)
    user_page = Filter(page)
    user_page.doctor_user_filter()





