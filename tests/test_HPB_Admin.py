import re
import time
from pages.user_metrics_page import UserMetricsPage
from faker.contrib.pytest.plugin import faker
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.Dashboard_page import Dashboardpage
from faker import Faker
from playwright.sync_api import Page, expect
from pages.create.create_FH_Clinical import Create_FA_clinica
from pages.refresh import RefreshablePage
from pages.Doctor_Users_page import Doctoruserpage
from pages.login_page import LoginPage
from pages.sort_page import SortPage
from pages.search_page import SearchPage
from pages.hpb_Menu import AdminPage
from pages.refresh import RefreshablePage
from pages.pagination import PaginationPage
from playwright.sync_api import Page
from pages.Edit_doctor_admin import Editdector
from pages.Delete import Delete
from pages.Doctor_Users_page import Doctoruserpage
from pages.edit_user import EditWorkflowPage
from pages.Filter import Filter
from pages.user_basic_info.wellness_score_tab import WellnessScoreTab
from pages.re_invite import re_invite
from pages.Customer_Type import CustomerType
from pages.assign import assign
from pages.Edit_Clinic_admin import EditClinic
from pages.create.create_FH_Clinical import Create_FA_clinica
from pages.create.Create_Clinica import create_clinic_page
from pages.create.create_doctor import DoctorCreationPage
from pages.create.Create_FH_Admin import CreateFullertonHealthPage
from pages.assign_users_page import AssignUsersPage
from pages.role_manager.roleManager_page import RoleManagerPage
from pages.role_manager.default_rolesCheckbox import DefaultRolesPage
from pages.role_manager.custom_roleCheckBox import CustomRolePage
from pages.Edit_FH_admin import EditFH
from data import Org_Admin_email, Org_Admin_otp, Org_Admin_password, clinic, fullerton_health, search_user, doctor_name, fh_admin, clinic_admin, search_item, withdrawn_user

fake = Faker()
facility_name = ""
clinic_name = ""

passed_steps = {
    "login": False,
    "create_fullerton_health": False,
    "create_clinic" : False,
    "cuser_page": False,
    "cdoctor_page":False,
    "cclincal_page":False,
    "FH_user_page":False,
    "fh_doctor_page":False,
    "fh_FH_page": False,
    "fh_admin_page": False,
    "clical_admin": False,
    "create_clinic_admin": False,
    "doctor_admin": False,
    "doctor_admin_user": False,
    "prospect": False,
    "user": False,
    "invite_user": False,
    "withdrawn_user": False,
    "all_user": False,
    "user_metrics": False,
    "rolemanager": False,
    "create_doctor": False

}

def do_loginORG(page: Page):
    login_page = LoginPage(page)
    login_page.login(Org_Admin_email, Org_Admin_password, Org_Admin_otp)

def do_create_fullerton_health(page: Page):
    global facility_name
    facility_name = "AT" + fake.company()
    facility_address = "AT" + fake.address()
    sp = Create_FA_clinica(page)
    sp.add_fullerton_health(facility_name, facility_address)

def do_create_clinic(page: Page):
    global clinic_name
    clinic_name = "AT" + fake.company()
    clinic_address = "AT" + fake.street_address()
    sp = Create_FA_clinica(page)
    sp.add_clinic(clinic_name, clinic_address, facility_name)

def do_cuser_page(page: Page):
    search_page = SearchPage(page)
    search_term = clinic  # Replace with test name
    search_page.perform_search(search_term)
    user_page = Doctoruserpage(page)
    user_page.select_clinic_users_page(clinic_name)

def do_create_doctor(page: Page):
    create_clinic = DoctorCreationPage(page)
    global doctor_name1
    doctor_name1 = create_clinic.create_doctor()

def do_cdoctor_page(page: Page):
    clinic_doctor_page = AdminPage(page)
    clinic_doctor_page.select_user_to_Doctor()

def do_cclincal_page(page: Page):
    clinic_doctor_page = AdminPage(page)
    clinic_doctor_page.select_doctor_to_Clinic_Admin()

def do_FH_user_page(page: Page):
    fh_c_page = AdminPage(page)
    fh_c_page.select_Structure_page()
    time.sleep(2)
    search_page = SearchPage(page)
    search_term = fullerton_health  # Replace with test name
    search_page.perform_search(search_term)
    time.sleep(2)
    user_page= AdminPage(page)
    user_page.select_fh_user()

def do_fh_doctor_page(page: Page):
    clinic_doctor_page = AdminPage(page)
    clinic_doctor_page.select_user_to_Doctor()

def do_fh_FH_page(page: Page):
    FH_Admin_page = AdminPage(page)
    FH_Admin_page.select_doctor_to_Clinic_Admin()

def do_fh_admin(page: Page):
    admin = AdminPage(page)
    admin.select_fullerton_admin()

def do_clical_admin(page: Page):
    admin = AdminPage(page)
    admin.select_clinic()

def do_create_clinic_admin(page: Page):
    create_clinic = create_clinic_page(page)
    global clinic_name
    clinic_name = create_clinic.create_clinic_admin()

def do_doctor_admin(page: Page):
    admin = AdminPage(page)
    admin.select_doctor_admin()

def do_doctor_admin_user(page: Page):
    search = SearchPage(page)
    search.perform_search(doctor_name)
    user_page = Doctoruserpage(page)
    user_page.select_doctor_users_page()

def do_prospect_page(page: Page):
    prospect_page = AdminPage(page)
    prospect_page.select_Prospects()

def do_user_page(page: Page):
    user_page = AdminPage(page)
    user_page.select_user()

def do_invite_user(page: Page):
    invite_user_page = AdminPage(page)
    invite_user_page.select_invite_user()

def do_Withdrawn_user(page: Page):
    withdrawn_page = AdminPage(page)
    withdrawn_page.select_withdrawn_user()

def do_all_user(page: Page):
    all_user_page = AdminPage(page)
    all_user_page.select_All_user()

def do_user_metrics(page: Page):
    metrics_page = AdminPage(page)
    metrics_page.select_user_metrics()
    
def do_role_manager(page: Page):
    role_manager = RoleManagerPage(page)
    role_manager.navigate_to_role_manager()



# ----------------------------- #
# FH and Clinical PAGE TEST CASES (roleORG)
# --
#

def test_roleORG_HPB_login_flow(page: Page):
    do_loginORG(page)
    passed_steps["login"] = True

def test_roleORG_total(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    dashboard = Dashboardpage(page)
    dashboard.click_total_users()

def test_roleORG_create_fullerton_health(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_create_fullerton_health(page)
    passed_steps["create_fullerton_health"] = True

def test_roleORG_create_clinic(page: Page):
    if not (passed_steps["login"] and passed_steps["create_fullerton_health"]):
        do_loginORG(page)
        do_create_fullerton_health(page)
    do_create_clinic(page)
    passed_steps["create_clinic"] = True

def test_roleORG_delete_clinic(page: Page):
    if not (passed_steps["login"] and passed_steps["create_fullerton_health"] and passed_steps["create_clinic"]):
        do_loginORG(page)
        do_create_fullerton_health(page)
        do_create_clinic(page)
    search_delete = SearchPage(page)
    search_delete.perform_search(clinic_name)
    delete = Delete(page)
    delete.delete_clinic()

def test_roleORG_delete_FH(page: Page):
    if not (passed_steps["login"] and passed_steps["create_clinic"]):
        do_loginORG(page)
        do_create_fullerton_health(page)
    search_delete = SearchPage(page)
    search_delete.perform_search(facility_name)
    delete = Delete(page)
    delete.delete_FH()

def test_roleORG_FHC_page_ref(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    refresh = RefreshablePage(page)
    refresh.refresh()

def test_roleORG_clinic_SearchPage(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    search_page = SearchPage(page)
    search_term = fullerton_health # Replace with test name
    search_page.search_function_FH(search_term)
    time.sleep(2)

# ----------------------------- #
#  Clinical user PAGE TEST CASES (roleORG)
# --


def test_roleORG_cuser_page(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_cuser_page(page)
    passed_steps["cuser_page"] = True

def test_roleORG_cuser_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"]):
        do_loginORG(page)
        do_cuser_page(page)
    time.sleep(5)
    search_page = SearchPage(page)
    search_term = search_user # Replace with test name
    search_page.search_function_clinic(search_term)

def test_roleORG_assign_users_flow(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"]):
        do_loginORG(page)
        do_cuser_page(page)
    assign_page = AssignUsersPage(page)
    assign_page.assign_and_confirm()

def test_roleORG_cuser_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"]):
        do_loginORG(page)
        do_cuser_page(page)
    pagination = PaginationPage(page)
    pagination.pagination()
    time.sleep(2)

def test_roleORG_cuser_refresh_page(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"]):
        do_loginORG(page)
        do_cuser_page(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

# Note: After the edit page not loaded
def test_roleORG_clinicUser_edit_user(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"]):
        do_loginORG(page)
        do_cuser_page(page)
    edit_user = EditWorkflowPage(page)
    edit_user.edit_userORG()


# ----------------------------- #
# Clinical Doctor PAGE TEST CASES (roleORG)
# --


def test_roleORG_clinic_doctor_page(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"]):
        do_loginORG(page)
        do_cuser_page(page)
    do_cdoctor_page(page)
    passed_steps["cdoctor_page"] = True


def test_roleORG_clinic_doctor_page_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"]):
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
    search_page = SearchPage(page)
    search_term = doctor_name  # Replace with test name
    search_page.search_function_clinic(search_term)

def test_roleORG_clinic_doctor_page_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"]):
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
    refresh = RefreshablePage(page)
    refresh.refresh()

def test_roleORG_assign_user(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"]):
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
    assign_doctor = assign(page)
    assign_doctor.assign_doctor()

def test_roleORG_clinic_doctor_page_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"]):
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
    pagination = PaginationPage(page)
    pagination.pagination()


def test_roleORG_clinic_doctor_page_edit(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"]):
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
    edit_page = Editdector(page)
    edit_page.edit_dector()


# ----------------------------- #
# Clinical Clinic_Admin PAGE TEST CASES (roleORG)
# --
#

def test_roleORG_clinic_Clinic_Admin_page(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"]):
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
    do_cclincal_page(page)
    passed_steps["cclincal_page"] = True

def test_roleORG_clinic_Clinic_Admin_page_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"] and passed_steps ["cclincal_page"]) :
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
        do_cclincal_page(page)
    search_page = SearchPage(page)
    global search_term
    search_term = "Riyaz Walikar"  # Replace with test name
    search_page.search_function_clinic(search_term)

def test_roleORG_clinic_Clinic_Admin_page_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"] and passed_steps ["cclincal_page"]) :
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
        do_cclincal_page(page)
    refresh = RefreshablePage(page)
    refresh.refresh()

def test_roleORG_clinic_Clinic_Admin_page_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"] and passed_steps ["cclincal_page"]) :
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
        do_cclincal_page(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleORG_Clinic_Admin_assign_user(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"] and passed_steps ["cclincal_page"]) :
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
        do_cclincal_page(page)
    assign_doctor = assign(page)
    assign_doctor.assign_Clinic_Admin()

def test_roleORG_clinic_page_edit(page: Page):
    if not (passed_steps["login"] and passed_steps["cuser_page"] and passed_steps["cdoctor_page"] and passed_steps ["cclincal_page"]) :
        do_loginORG(page)
        do_cuser_page(page)
        do_cdoctor_page(page)
        do_cclincal_page(page)
    edit_search = SearchPage(page)
    edit_search.perform_search(clinic_admin)
    edit_page = EditClinic(page)
    edit_page.edit_clinic()

# ----------------------------- #
# Back Fullerton Health and clinical PAGE FH Opration TEST CASES (roleORG)
# --
# ----------------------------- #
# FH User PAGE TEST CASES (roleORG)
# --
#
def test_roleORG_FH_user_page(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_FH_user_page(page)
    passed_steps["FH_user_page"] = True

def test_roleORG_fh_cuser_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
    time.sleep(5)
    search_page = SearchPage(page)
    search_term = search_user  # Replace with test name
    search_page.search_function_clinic(search_term)


def test_roleORG_fh_cuser_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
    pagination = PaginationPage(page)
    pagination.pagination()
    time.sleep(2)

def test_roleORG_fh_cuser_refresh_page(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()


# Note: After the edit page not loaded
def test_roleORG_cuser_edit_user(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
    edit_user = EditWorkflowPage(page)
    edit_user.edit_userORG()

# ----------------------------- #
# FH Doctor PAGE TEST CASES (roleORG)
# --
#

def test_roleORG_fh_doctor_page(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
    do_fh_doctor_page(page)
    passed_steps["fh_doctor_page"] = True


def test_roleORG_fh_doctor_page_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
    search_page = SearchPage(page)
    search_term = doctor_name  # Replace with test name
    search_page.search_function_clinic(search_term)

def test_roleORG_fh_doctor_page_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
    refresh = RefreshablePage(page)
    refresh.refresh()

def test_roleORG_fh_assign_user(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
    assign_doctor = assign(page)
    assign_doctor.assign_doctor()


def test_roleORG_FH_doctor_page_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
    pagination = PaginationPage(page)
    pagination.pagination()


def test_roleORG_FH_doctor_page_edit(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
    edit_page = Editdector(page)
    edit_page.edit_dector()


# ----------------------------- #
# Facility - FH_Admin PAGE TEST CASES (roleORG)
# --
#

def test_roleORG_fh_FH_Admin_page(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
    do_fh_FH_page(page)
    passed_steps["fh_FH_page"] = True
    time.sleep(5)


def test_roleORG_fh_FH_Admin_page_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"] and passed_steps["fh_FH_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
        do_fh_FH_page(page)

    search_page = SearchPage(page)
    search_term = fh_admin  # Replace with test name
    search_page.search_function_clinic(search_term)

def test_roleORG_fh_FH_Admin_page_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"] and passed_steps["fh_FH_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
        do_fh_FH_page(page)
    refresh = RefreshablePage(page)
    refresh.refresh()

def test_roleORG_fh_FH_Admin_page_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"] and passed_steps["fh_FH_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
        do_fh_FH_page(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleORG_fh_FH_Admin_assign_user(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"] and passed_steps["fh_FH_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
        do_fh_FH_page(page)
    assign_doctor = assign(page)
    assign_doctor.assign_fh_Admin()

# Have a Issue
def test_roleORG_fh_FHAdmin_page_edit(page: Page):
    if not (passed_steps["login"] and passed_steps["FH_user_page"] and passed_steps["fh_doctor_page"] and passed_steps["fh_FH_page"]):
        do_loginORG(page)
        do_FH_user_page(page)
        do_fh_doctor_page(page)
        do_fh_FH_page(page)
    edit_page = EditFH(page)
    edit_page.edit_fh()


# ----------------------------- #
# Fullerton Health Admin PAGE TEST CASES (roleORG)
# --

def test_roleORG_FH_admin_page(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_fh_admin(page)
    time.sleep(5)
    passed_steps["fh_admin_page"] = True

def test_roleORG_create_FH_admin(page: Page):
    if not (passed_steps["login"] and passed_steps["fh_admin_page"]):
        do_loginORG(page)
        do_fh_admin(page)
    create_FH = CreateFullertonHealthPage(page)
    create_FH.create_fh_admin()

def test__roleORG_FHA_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["fh_admin_page"]):
        do_loginORG(page)
        do_fh_admin(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

def test_roleORG_FHA_page(page: Page):
    if not (passed_steps["login"] and passed_steps["fh_admin_page"]):
        do_loginORG(page)
        do_fh_admin(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleORG_sort_by_name_and_last_sign_in(page : Page):
    if not (passed_steps["login"] and passed_steps["fh_admin_page"]):
        do_loginORG(page)
        do_fh_admin(page)
    sort = SortPage(page)
    sort.sort_by_name_az_and_last_sign_in()

def test_roleORG_search_functionality(page: Page):
    if not (passed_steps["login"] and passed_steps["fh_admin_page"]):
        do_loginORG(page)
        do_fh_admin(page)
    search_page = SearchPage(page)
    search_term = fh_admin  # You can replace this with any valid term
    search_page.search_function(search_term)

# ----------------------------- #
# CLINIC ADMIN PAGE TEST CASES (roleORG)
# --

def test_roleORG_CAP_click_clinic_admin(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_clical_admin(page)
    passed_steps["clical_admin"] = True

def test_roleORG_CAP_refresh_page(page: Page):
    if not (passed_steps["login"] and passed_steps["clical_admin"]):
        do_loginORG(page)
        do_clical_admin(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

def test_roleORG_CAP_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["clical_admin"]):
        do_loginORG(page)
        do_clical_admin(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleORG_CAP_sort_name_last_signin(page: Page):
    if not (passed_steps["login"] and passed_steps["clical_admin"]):
        do_loginORG(page)
        do_clical_admin(page)
    sort = SortPage(page)
    sort.sort_by_name_az_and_last_sign_in()

def test_roleORG_CAP_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["clical_admin"]):
        do_loginORG(page)
        do_clical_admin(page)
    search_page = SearchPage(page)
    search_term = clinic_admin # Replace with test name
    search_page.search_function(search_term)

def test_roleORG_clinic_admin_Edit_flow(page: Page):
    if not (passed_steps["login"] and passed_steps["clical_admin"]):
        do_loginORG(page)
        do_clical_admin(page)
    clinic = EditClinic(page)
    clinic.edit_clinic()

def test_roleORG_create_clinic_admin(page: Page):
    if not (passed_steps["login"] and passed_steps["clical_admin"]):
        do_loginORG(page)
        do_clical_admin(page)
    do_create_clinic_admin(page)
    passed_steps["create_clinic_admin"] = True

def test_roleORG_clinic_admin_delete(page: Page):
    if not (passed_steps["login"] and passed_steps["clical_admin"] and passed_steps["create_clinic_admin"]):
        do_loginORG(page)
        do_clical_admin(page)
        do_create_clinic_admin(page)
    search_delete = SearchPage(page)
    search_delete.perform_search(clinic_name)
    clinic_delete = Delete(page)
    clinic_delete.delete_click()
    clinic_delete.delete_confirm()
    # clinic_delete.delete_cancel()



# ----------------------------- #
# Doctor ADMIN PAGE TEST CASES (roleORG)
# --


def test_roleORG_DP_click_clinic_admin(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_doctor_admin(page)
    passed_steps["doctor_admin"] = True


def test_roleORG_DP_refresh_page(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"]):
        do_loginORG(page)
        do_doctor_admin(page)
    ref_page = RefreshablePage(page)
    ref_page.refresh()

def test_roleORG_DP_pagination_controls(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"]):
        do_loginORG(page)
        do_doctor_admin(page)
    pagination = PaginationPage(page)
    pagination.pagination()

def test_roleORG_DP_sort_name_last_signin(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"]):
        do_loginORG(page)
        do_doctor_admin(page)
    sort = SortPage(page)
    sort.sort_by_name_az_and_last_sign_in()

def test_roleORG_create_Doctor_admin(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"]):
        do_loginORG(page)
        do_doctor_admin(page)
    do_create_doctor(page)
    passed_steps["create_doctor_admin"] = True


def test_roleORG_DP_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"]):
        do_loginORG(page)
        do_doctor_admin(page)
    search_page = SearchPage(page)
    search_term = doctor_name  # Replace with test name
    search_page.search_function(search_term)

def test__roleORG_DP_admin_Edit_flow(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"]):
        do_loginORG(page)
        do_doctor_admin(page)
    clinic = Editdector(page)
    clinic.edit_dector()


def test_roleORG_doctor_admin_delete(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"] and passed_steps["create_clinic_admin"]):
        do_loginORG(page)
        do_doctor_admin(page)
        do_create_doctor(page)
    serarch_delete = SearchPage(page)
    serarch_delete.perform_search(doctor_name1)
    doctor_delete = Delete(page)
    doctor_delete.delete_click()
    doctor_delete.delete_confirm()
    # doctor_delete.delete_cancel()


def test_roleORG_Doctor_users(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"]):
        do_loginORG(page)
        do_doctor_admin(page)
    do_doctor_admin_user(page)
    passed_steps["doctor_admin_user"] = True

def test_roleORG_Doctor_users_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"] and passed_steps ["doctor_admin_user"]):
        do_loginORG(page)
        do_doctor_admin(page)
        do_doctor_admin_user(page)
    user_page = PaginationPage(page)
    user_page.pagination()


def test_roleORG_Doctor_users_search_by_name(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"] and passed_steps ["doctor_admin_user"]):
        do_loginORG(page)
        do_doctor_admin(page)
        do_doctor_admin_user(page)
    search_page = SearchPage(page)
    search_term = search_user # Replace with test name
    search_page.search_function(search_term)


def test_roleORG_Doctor_users_Edit(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"] and passed_steps ["doctor_admin_user"]):
        do_loginORG(page)
        do_doctor_admin(page)
        do_doctor_admin_user(page)
    user_page = EditWorkflowPage(page)
    user_page.edit_roleOrg_doc_user()

def test_roleORG_Doctor_users_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"] and passed_steps ["doctor_admin_user"]):
        do_loginORG(page)
        do_doctor_admin(page)
        do_doctor_admin_user(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleORG_Doctor_users_filter(page: Page):
    if not (passed_steps["login"] and passed_steps["doctor_admin"] and passed_steps ["doctor_admin_user"]):
        do_loginORG(page)
        do_doctor_admin(page)
        do_doctor_admin_user(page)
    user_page = Filter(page)
    user_page.doctor_user_filter()



# ----------------------------- #
# prospect PAGE TEST CASES (roleORG)
# --
#


def test_roleORG_prospect_page(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_prospect_page(page)
    passed_steps["prospect_page"] = True

def test_roleORG_prospect_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["prospect_page"]):
        do_loginORG(page)
        do_prospect_page(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleORG_prospect_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["prospect_page"]):
        do_loginORG(page)
        do_prospect_page(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleORG_prospect_calander(page: Page):
    if not (passed_steps["login"] and passed_steps["prospect_page"]):
        do_loginORG(page)
        do_prospect_page(page)
    calander = WellnessScoreTab(page)
    calander.calendar_filter_dropdown()

def test_roleORG_prospect_search(page: Page):
    if not (passed_steps["login"] and passed_steps["prospect_page"]):
        do_loginORG(page)
        do_prospect_page(page)
    time.sleep(2)
    search_page = SearchPage(page)
    search_term = search_item  # Replace with test name
    search_page.search_function(search_term)


# ----------------------------- #
# User PAGE TEST CASES (roleORG)
# --


def test_roleORG_user_page(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_user_page(page)
    passed_steps["user_page"] = True

def test_roleORG_user_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleORG_user_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleORG_users_filter(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    user_page = Filter(page)
    user_page.normal_filter()

def test_roleORG_user_search(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    time.sleep(5)
    search_page = SearchPage(page)
    search_term = search_user  # Replace with test name
    search_page.search_function(search_term)

def test_roleORG_user_edit(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    edit = EditWorkflowPage(page)
    edit.edit_userORG()

def test_roleORG_user_delete(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    delete = Delete(page)
    delete.delete_click()
    # delete.delete_confirm()
    delete.delete_cancel()


# ----------------------------- #
# Invite User PAGE TEST CASES (roleORG)
# --


def test_roleORG_invite_user_page(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    do_invite_user(page)
    passed_steps["invite_user"] = True

def test_roleORG_invite_user_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["invite_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_invite_user(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleORG_invite_invite_user_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["invite_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_invite_user(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleORG_invite_user_search(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["invite_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_invite_user(page)
    search_page = SearchPage(page)
    search_term = search_item # Replace with test name
    search_page.search_function_Invited_Users(search_term)

def test_roleORG_invite_user_re_invaite(page : Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["invite_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_invite_user(page)
    reinvite = re_invite(page)
    reinvite.re_invite()


# ----------------------------- #
# Withdrawn User PAGE TEST CASES (roleORG)
# --


def test_roleORG_Withdrawn_user_page(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    do_Withdrawn_user(page)
    passed_steps["withdrawn_user"] = True

def test_roleORG_Withdrawn_user_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["withdrawn_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_Withdrawn_user(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleORG_Withdrawn_invite_user_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["withdrawn_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_Withdrawn_user(page)
    user_page = PaginationPage(page)
    user_page.pagination()


def test_roleORG_Withdrawn_user_search(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["withdrawn_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_Withdrawn_user(page)
    search_page = SearchPage(page)
    search_term = withdrawn_user  # Replace with test name
    search_page.search_function(search_term)


# ----------------------------- #
# All User PAGE TEST CASES (roleORG)
# --


def test_roleORG_Alluser_page(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"]):
        do_loginORG(page)
        do_user_page(page)
    do_all_user(page)
    passed_steps["all_user"] = True

def test_roleORG_Alluser_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["all_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_all_user(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleORG_Alluser_pagination(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["all_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_all_user(page)
    user_page = PaginationPage(page)
    user_page.pagination()

def test_roleORG_Allusers_filter(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["all_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_all_user(page)
    user_page = Filter(page)
    user_page.normal_filter()

def test_roleORG_Alluser_search(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["all_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_all_user(page)
    search_page = SearchPage(page)
    search_term = search_user  # Replace with test name
    search_page.search_function(search_term)

def test_roleORG_Alluser_edit(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["all_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_all_user(page)
    edit = EditWorkflowPage(page)
    edit.edit_user()

def test_roleORG_Alluser_delete(page: Page):
    if not (passed_steps["login"] and passed_steps["user_page"] and passed_steps["all_user"]):
        do_loginORG(page)
        do_user_page(page)
        do_all_user(page)
    delete = Delete(page)
    delete.delete_click()
    # delete.delete_confirm()
    delete.delete_cancel()


# ----------------------------- #
# User metrics User PAGE TEST CASES (roleORG)
# --

def test_roleORG_user_metrics_navigation(page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_user_metrics(page)
    passed_steps["user_metrics"] = True

def test_roleORG_user_metrics_ref(page: Page):
    if not (passed_steps["login"] and passed_steps["user_metrics"]):
        do_loginORG(page)
        do_user_metrics(page)
    user_page = RefreshablePage(page)
    user_page.refresh()

def test_roleORG_user_metrics_calander(page: Page):
    if not (passed_steps["login"] and passed_steps["user_metrics"]):
        do_loginORG(page)
        do_user_metrics(page)
    calander = WellnessScoreTab(page)
    calander.calendar_filter_dropdown()

def test_roleORG_user_metrics_customerType(page: Page):
    if not (passed_steps["login"] and passed_steps["user_metrics"]):
        do_loginORG(page)
        do_user_metrics(page)
    customerType = CustomerType(page)
    customerType.customtype()


# ----------------------------- #
# Role Manager PAGE Default Role TEST CASES (roleORG)
# --

def test_role_manager_navigation(page: Page):
    if not (passed_steps["login"]):
        do_loginORG(page)
    do_role_manager(page)
    passed_steps["rolemanager"] = True

def test_role_manager_defaultRole_checkboxIn(page: Page):
    if not (passed_steps["login"] and passed_steps["rolemanager"]):
        do_loginORG(page)
        do_role_manager(page)
    defaultRole_checkbox = DefaultRolesPage(page)
    defaultRole_checkbox.CheckboxIn()

def test_roleManager_defaultRole_checkboxOut(page: Page):
    if not (passed_steps["login"] and passed_steps["rolemanager"]):
        do_loginORG(page)
        do_role_manager(page)
    defaultRole_checkbox = DefaultRolesPage(page)
    defaultRole_checkbox.CheckboxOut()


# Role Manager PAGE Custom Role TEST CASES (roleORG)
# --

def test_roleManager_customRole_create(page: Page):
    if not (passed_steps["login"] and passed_steps["rolemanager"]):
        do_loginORG(page)
        do_role_manager(page)
    customRole_create = CustomRolePage(page)
    customRole_create.customRole_Create()

def test_roleManager_customRole_edit(page: Page):
    if not (passed_steps["login"] and passed_steps["rolemanager"]):
        do_loginORG(page)
        do_role_manager(page)
    customRole_edit = CustomRolePage(page)
    customRole_edit.customRole_Edit()

def test_roleManager_customRole_checkboxIn(page: Page):
    if not (passed_steps["login"] and passed_steps["rolemanager"]):
        do_loginORG(page)
        do_role_manager(page)
    customRole_checkbox = CustomRolePage(page)
    customRole_checkbox.customRole_CheckboxIn()

def test_roleManager_customRole_checkboxOut(page: Page):
    if not (passed_steps["login"] and passed_steps["rolemanager"]):
        do_loginORG(page)
        do_role_manager(page)
    customRole_checkbox = CustomRolePage(page)
    customRole_checkbox.customRole_CheckboxOut()

def test_roleManager_customRole_delete(page: Page):
    if not (passed_steps["login"] and passed_steps["rolemanager"]):
        do_loginORG(page)
        do_role_manager(page)
    customRole_delete = CustomRolePage(page)
    customRole_delete.customrole_Delete()