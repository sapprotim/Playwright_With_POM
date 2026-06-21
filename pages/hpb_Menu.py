from asyncio import timeout

from playwright.sync_api import Page, expect
import time

class AdminPage:
    def __init__(self, page: Page):
        self.page = page

    def open_admin_tab(self):
        self.page.locator(".tab-name").first.click()

    def open_Organization_View(self):
        self.page.locator(".tab-name").first.click()
        Organization_View = self.page.get_by_text("Organization View", exact=True).first
        expect(Organization_View).to_be_visible()
        Organization_View.click()

    def select_HPB_admin(self):
        self.open_admin_tab()
        fullerton_admin = self.page.get_by_text("HPB Admin", exact=True).first
        expect(fullerton_admin).to_be_visible()
        fullerton_admin.click()
        title = self.page.locator("//div[@class='user-list-title']")
        assert "HPB Admin" == title.inner_text().strip()


    def select_fullerton_admin(self):
        self.open_admin_tab()
        fullerton_admin = self.page.get_by_text("Fullerton Health Admin", exact=True).first
        expect(fullerton_admin).to_be_visible()
        fullerton_admin.click()
        title = self.page.locator("//div[@class='user-list-title']")
        assert "Fullerton Health Admin" == title.inner_text().strip()

    def select_clinic(self):
        self.open_admin_tab()
        self.page.get_by_text("Clinic Admin", exact=True).click()
        title = self.page.locator("//div[@class='user-list-title']")
        assert "Clinic Admin" == title.inner_text().strip()

    def select_doctor_admin(self):
        time.sleep(1)
        self.open_admin_tab()
        time.sleep(1)
        self.page.get_by_text("Doctor", exact=True).click()
        time.sleep(1)
        self.page.mouse.move(500, 300)


    def select_Prospects(self):
        time.sleep(1)
        self.open_admin_tab()
        self.page.locator("a").filter(has_text="Users").click()
        users_Prospects = self.page.get_by_role("link", name="Prospects")
        expect(users_Prospects).to_be_visible()
        users_Prospects.click()

        title = self.page.locator("//div[@class='user-list-title']")
        assert "Prospects" == title.inner_text().strip()


    def select_user(self):
        time.sleep(1)
        self.open_admin_tab()
        self.page.locator("a").filter(has_text="Users").click()
        users = self.page.locator("//a[@routerlink='/users']")
        expect(users).to_be_visible()
        users.click()
        self.page.locator("//img[@title='Refresh']").click()


    def select_invite_user(self):
        time.sleep(1)
        self.page.locator("//div[@class='user-list-title']//div[@class='dropdown']/button").click()
        invite_user = self.page.get_by_text("Invited Users")
        expect(invite_user).to_be_visible()
        invite_user.click()

    def select_withdrawn_user(self):
        time.sleep(1)
        self.page.locator("//div[@class='user-list-title']//div[@class='dropdown']/button").click()
        withdrawn_user = self.page.get_by_text("Withdrawn Users")
        expect(withdrawn_user).to_be_visible()
        withdrawn_user.click()

    def select_All_user(self):
        try:
            time.sleep(5)
            self.page.locator("//div[@class='user-list-title']/div//button").click()
        except:
            try:
                self.page.locator("//div[@class='user-list-title']//div[@class='dropdown']//button").click()
            except:
                pass  # Optional: you can log or raise error if both are not found
        # Then click the common "All Users" link
        self.page.locator("//div[@class='user-list-title']//li[1]").click()

    def select_user_metrics(self):
        time.sleep(1)
        self.open_admin_tab()
        time.sleep(1)
        self.page.locator("//a[normalize-space()='Users']").click()
        time.sleep(1)
        self.page.locator("//a[normalize-space()='User Metrics']").first.click()
        time.sleep(1)
        title = self.page.locator("//h1[normalize-space()='User Metrics']")
        assert "User Metrics" == title.inner_text().strip()

    def select_user_to_Doctor(self):
        time.sleep(1)
        self.page.get_by_role("button", name="Users").click()
        self.page.locator("#CareTeam").click()

    def select_doctor_to_Clinic_Admin(self):
        time.sleep(1)
        self.page.locator("//button[normalize-space()='Doctor']").click()
        self.page.locator("//a[@id='FacilityAdministrator']").click()

    def select_Structure_page(self):
        self.page.locator("//div[@id='admin']").click()
        self.page.get_by_text("Structure").click()

    def select_fh_user(self):
        self.page.locator("//tbody/tr/td[1]/span").click()




