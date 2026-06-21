import os
import pytest
import base64
from datetime import datetime
from data import dashboard_link

import pytest_html
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

playwright_instance = None

@pytest.fixture(scope="module")
def browser_context():
    global playwright_instance
    playwright_instance = sync_playwright().start()
    browser = playwright_instance.chromium.launch(headless=True, args=["--window-size=1920,1080"])
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    context.set_default_timeout(20000)
    yield context
    browser.close()
    playwright_instance.stop()

@pytest.fixture(scope="module")
def page(browser_context):
    page = browser_context.new_page()
    try:
        page.goto(dashboard_link)
    except PlaywrightTimeoutError:
        print("❌ Timeout while loading login page.")
    except PlaywrightError as e:
        print(f"❌ Unexpected error: {e}")
    yield page
    page.close()

# ----------------------------
# Helper Functions
# ----------------------------

def _img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ----------------------------
# Pytest Hook to capture screenshots on pass and fail
# ----------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page = item.funcargs.get("page", None)

        if page:
            try:
                os.makedirs("screenshots", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = item.name.replace("/", "_")
                status = "pass" if report.passed else "fail"
                path = f"screenshots/{name}_{status}_{timestamp}.png"
                page.screenshot(path=path, full_page=True)

                if report.passed:
                    print(f"✅ Test Passed: {item.name}")
                elif report.failed:
                    print(f"\n❌ Test Failed: {item.name}")
                    print(f"   Reason: {str(call.excinfo.value)}")

                print(f"   Screenshot saved at: {path}")

                # Attach screenshot to HTML report if plugin is active
                html_plugin = item.config.pluginmanager.getplugin("html")
                if html_plugin:
                    extra = getattr(report, "extra", [])
                    img = _img_to_base64(path)
                    extra.append(pytest_html.extras.html(
                        f'<div><strong>{status.capitalize()} Screenshot:</strong><br>'
                        f'<img src="data:image/png;base64,{img}" style="max-width:800px;"/></div>'
                    ))
                    report.extra = extra

            except Exception as e:
                print(f"   Screenshot error: {e}")