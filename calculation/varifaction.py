import re
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from clinical_ws import clinical_WS
from lifestyle_ws import lifestyle_WS

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE_URL, USERNAME, PASSWORD

def extract_number(text):
    match = re.findall(r"[-+]?[0-9]*\.?[0-9]+", text)
    return match[0] if match else ""

def clean_value(label, text):
    text = text.strip()
    if "Blood Pressure" in label and "/" in text:
        parts = re.findall(r"\d+", text)
        return {"Systolic": parts[0], "Diastolic": parts[1]} if len(parts) >= 2 else {}
    return extract_number(text)

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Login — credentials loaded from config.py (not committed)
    page.goto(BASE_URL)
    page.get_by_role("textbox", name="Username / Email").fill(USERNAME)
    page.get_by_role("textbox", name="Password eye-icon").fill(PASSWORD)
    page.get_by_role("button", name="Sign In").click()
    otp = input("Enter OTP: ")
    page.get_by_role("textbox", name="PIN").fill(otp)
    page.get_by_role("button", name="Submit").click()

    # Search and select user — set SEARCH_USER in config.py
    from config import SEARCH_USER
    page.get_by_role("textbox", name="Search").fill(SEARCH_USER)
    page.get_by_role("table").get_by_text(SEARCH_USER).click()
    time.sleep(10)

    # Set date to today
    page.locator("//div[@class='date-picker-wrap ng-star-inserted']//label[@class='date-picker-label']//img").click()
    page.locator("//div[@class='md-drppicker drops-down-auto ltr double show-ranges shown']//button[@type='button'][normalize-space()='Today']").click()
    page.locator("//button[normalize-space()='Update']").click()
    time.sleep(7)

    # Get gender
    gender = page.locator("//div[@class='ant-row ng-star-inserted']//p[@id='user-age']").text_content().strip().lower()

    # Extract labels and values
    labels = page.locator("//div[@class='dashboard-body-wrap']//ul//li/div/span").all_text_contents()
    values = page.locator("//div[@class='dashboard-body-wrap']//ul//li/div/p").all_text_contents()

    results = {}
    for label, value in zip(labels, values):
        label = label.strip()
        value = value.strip()
        cleaned = clean_value(label, value)
        if isinstance(cleaned, dict):
            results.update(cleaned)
        else:
            results[label] = cleaned

    # Print label, cleaned value (float or "Null"), and type
    final_clinical_value = {}

    for label, value in results.items():
        if value in ("", None):
            final_clinical_value[label] = "Null"
        else:
            try:
                final_clinical_value[label] = float(value)
            except:
                final_clinical_value[label] = value

    print(final_clinical_value)

    clinical = clinical_WS(
        gender=gender,
        bmi_value=final_clinical_value['Body Mass Index'],
        waist_value=final_clinical_value['Waist Circumference'],
        systolic=final_clinical_value['Systolic'],
        diastolic=final_clinical_value['Diastolic'],
        hba1c_value=final_clinical_value['HbA1c'],
        fg_value=final_clinical_value['Fasting Blood Glucose'],
        ldl_value=final_clinical_value['LDL Cholesterol'],
        tg_value=final_clinical_value['Triglycerides'],
        RHR=final_clinical_value['Resting Heart Rate'],
        hrv_val=final_clinical_value['Heart Rate Variability']
    )

    text = page.locator("//span[@class='highcharts-title']//div").text_content()
    # Extract numeric value from the text
    match = re.search(r"[-+]?\d+", text)  # match integer part only
    clinical_ws = int(match.group()) if match else 0
    print("Clinic Calculation Score:", clinical)
    print("Clinic Dashboard Score:", clinical_ws)
    assert clinical_ws == int(clinical)




    # lifestyle
    page.locator("//span[@class='mdc-tab__text-label'][normalize-space()='Lifestyle']").click()
    time.sleep(10)

    life_results = {}

    # Extract Lifestyle labels and values from page
    lifestyle_labels = page.locator("//div[@id='wellness-score-dashboard']//ul//li//div/span").all_text_contents()
    lifestyle_values = page.locator("//div[@id='wellness-score-dashboard']//ul//li//div/p").all_text_contents()

    for label, value in zip(lifestyle_labels, lifestyle_values):
        label = label.strip()
        value = value.strip()

        if not value:
            cleaned_value = "Null"
        else:
            match = re.findall(r"[-+]?[0-9]*\.?[0-9]+", value)
            cleaned_value = match[0] if match else value

        life_results[label] = cleaned_value

    print("life_results", life_results)

    def process_life_results(data):
        new_results = {}
        for key, value in data.items():
            val = str(value).strip()
            if val == '--':
                new_results[key] = 'Null'
            else:
                try:
                    new_results[key] = float(val)
                except ValueError:
                    new_results[key] = val
        return new_results

    life_results = process_life_results(life_results)

    print(life_results)

    lifestyle = lifestyle_WS(
        gender=gender.lower(),
        step=life_results['Steps'],
        time=life_results['Sedentary Time'],
        unhealthy_fats=life_results['Unhealthy Oil & Fat'],
        limit_sugar=life_results['Limit Sugar'],
        whole_grain=life_results['Wholegrains'],
        stress=life_results['Stress'],
        processed_food=life_results['Processed Food'],
        fruit_veg=life_results['Fruit & Vegetables'],
        mvpa=life_results['MVPA'],
        alcohol=life_results['Alcohol'],
        smoking=life_results['Smoking'],
        sleep=life_results['Sleep']
    )
    # Extract the text content
    text = page.locator("//span[@class='highcharts-title']//div").text_content()

    # Extract only the number
    match = re.search(r"[-+]?\d+", text)  # match integer only
    lifestyle_ws = int(match.group()) if match else 0
    print("Lifestyle Calculation Score:", lifestyle)
    print("Lifestyle Dashboard Score:", lifestyle_ws)
    assert lifestyle_ws == int(lifestyle)

    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)



