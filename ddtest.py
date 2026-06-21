import csv
import re
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from apidataprint import fetch_patient_metrics

# Globals / shared variables
calendar_path = "//div[@class='calendar left ng-star-inserted']//div[@class='calendar-table']//tr[6]/td[6]"
endDate = "2025-09-05"
date = int(endDate.split("-")[2])


CSV_PATH = "user data.csv"
def read_csv(path):
    """Read CSV into list of dict rows."""
    rows = []
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


# ------------------------ Helper functions ------------------------
def safe_value(var):
    """Return var or empty string if falsy."""
    return var if var else ""


def extract_number(text):
    """Return first numeric substring from text, else empty string."""
    match = re.findall(r"[-+]?[0-9]*\.?[0-9]+", str(text))
    return match[0] if match else ""


def clean_value(label, text):
    """
    Clean clinical value text based on label.
    For Blood Pressure returns dict with Systolic/Diastolic when possible,
    otherwise returns numeric-extracted string.
    """
    if text is None:
        text = ""
    text = str(text).strip()
    if "Blood Pressure" in label and "/" in text:
        parts = re.findall(r"\d+", text)
        return {"Systolic": parts[0], "Diastolic": parts[1]} if len(parts) >= 2 else {}
    return extract_number(text)


def parse_sleep_minutes(raw):
    """Convert raw sleep like '6 hrs 8 mins' to total minutes (368)."""
    if not raw or not isinstance(raw, str):
        return 0
    h_match = re.search(r"(\d+)\s*hr", raw)
    m_match = re.search(r"(\d+)\s*min", raw)
    h = int(h_match.group(1)) if h_match else 0
    m = int(m_match.group(1)) if m_match else 0
    return h * 60 + m


def initials(txt):
    """Convert text to initials (keep symbols like & and @)."""
    if not txt:
        return ""
    return "".join([w[0].upper() if w[0].isalpha() else w for w in txt.split()])


def get_text(page, selector):
    """Return stripped inner text for selector if exists, else empty string."""
    locator = page.locator(selector)
    return locator.inner_text().strip() if locator.count() else ""


def safe_parse_timestamp(ts):
    """Return date part (MM/DD/YYYY) if valid, else empty string."""
    if not ts or not str(ts).strip():
        return ""
    try:
        return datetime.strptime(str(ts).strip(), "%m/%d/%Y %H:%M").strftime("%m/%d/%Y")
    except ValueError:
        return ""


# Normalization helpers used for comparisons
def normalize_datetime(val):
    """Normalize date/time strings for comparison, ignoring time if needed."""
    if not val or str(val).strip() in ["--", ""]:
        return None
    val = str(val).strip()
    for fmt in ("%d-%m-%Y %H:%M", "%d-%m-%Y", "%d %b, %Y", "%d %B, %Y"):
        try:
            return datetime.strptime(val, fmt).date()
        except ValueError:
            continue
    return val


def normalize_value(val):
    """Convert None/empty/'--' to empty string, strip spaces, remove parentheses content."""
    if val is None:
        return ""
    val = str(val).strip()
    if val in ["--", ""]:
        return ""
    val = re.sub(r"\(.*?\)", "", val)
    return val.strip()


def normalize_numeric(val):
    """Extract numeric part only, ignore units."""
    if val is None:
        return None
    val = str(val).strip()
    if val in ["", "--", "None", "null"]:
        return None
    val = re.sub(r"[^\d.]+", "", val)
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        return None


def normalize_date(val):
    """Convert date into standard date object for comparison."""
    if not val or str(val).strip() in ["--", ""]:
        return None
    for fmt in ("%d-%m-%Y", "%d-%m-%y", "%Y-%m-%d", "%m/%d/%Y", "%m-%d-%y"):
        try:
            return datetime.strptime(str(val).strip(), fmt).date()
        except ValueError:
            continue
    return val


def normalize_case(val, mode="ignore"):
    """Normalize string case for comparison."""
    if val is None:
        return ""
    val = str(val).strip()
    if mode == "lower":
        return val.lower()
    elif mode == "upper":
        return val.upper()
    else:
        return val.lower()


def values_match(csv_val, dash_val, numeric=False, case="ignore", date=False, strip_prefix=None):
    """
    Safe comparison for text, numeric, and date values with optional prefix stripping.
    - date=True compares normalized dates
    - numeric=True compares numeric parts
    - strip_prefix will remove prefix (like "Clinic") before comparing; if strip_prefix=="Clinic" convert to initials
    """
    if date:
        return normalize_date(csv_val) == normalize_date(dash_val)
    if numeric:
        n1, n2 = normalize_numeric(csv_val), normalize_numeric(dash_val)
        return n1 == n2

    v1, v2 = normalize_value(csv_val), normalize_value(dash_val)

    if strip_prefix:
        if v1.lower().startswith(strip_prefix.lower()):
            v1 = v1[len(strip_prefix) :].strip()
        if v2.lower().startswith(strip_prefix.lower()):
            v2 = v2[len(strip_prefix) :].strip()

    if strip_prefix == "Clinic":
        v1 = initials(v1)
        v2 = initials(v2)

    v1, v2 = normalize_case(v1, case), normalize_case(v2, case)
    return v1 == v2


def strip_parentheses(text):
    """Remove anything inside parentheses and extra spaces."""
    if not text:
        return ""
    return re.sub(r"\s*\([^)]*\)", "", str(text)).strip()


# ------------------------ Main processing ------------------------
def main():
    data_list = read_csv(CSV_PATH)
    if not data_list:
        print("No rows found in CSV.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Login once
        EMAIL = "hpbfullerton22+STM1@gmail.com"
        PASSWORD = "Wellness@123!"
        OTP = "312800"

        page.goto("https://hpb-uat.connectedlife.io/#/login")
        page.fill("input[name='username']", EMAIL)
        page.fill("input[name='password']", PASSWORD)
        page.click("input[value='Sign In']")
        time.sleep(3)
        page.fill("input[id='inp']", OTP)
        page.click("input[value='Submit']")
        time.sleep(5)

        # Loop once per user in CSV
        for user in data_list:
            time.sleep(2)
            user_id = user["user_id"]

            # Search user
            search_box = page.locator("input[placeholder='Search']")
            search_box.fill("")
            search_box.fill(user_id)
            time.sleep(5)

            # Wait for expected dashboard elements
            page.wait_for_selector("//tbody/tr/td[3]", timeout=10000)
            os_date_dashboard = page.locator("//tbody/tr/td[3]").inner_text().strip()
            clinic_dashboard = page.locator("//tbody/tr/td[2]").inner_text().strip()
            last_sync_timestamp_dashboard = page.locator("//tbody/tr/td[4]").inner_text().strip()
            if last_sync_timestamp_dashboard == "Device not synced":
                last_sync_timestamp_dashboard = ""

            texts = page.locator("//tbody/tr/td[8]").all_inner_texts()
            pcc_intervention_dashboard = (
                "Yes" if any(re.search(r"\d{1,2}/\d{1,2}/\d{4}", t) for t in texts) else "No"
            )

            # Click to open user profile/details
            page.locator("//tbody/tr/td[1]").click()
            time.sleep(5)
            age_dashboard = page.locator("//div[@class='profile-detailes-grid']//div[2]//p[2]").inner_text().strip()
            sex_dashboard = page.locator("//div[@class='ant-row ng-star-inserted']//p[@id='user-age']").inner_text().strip()
            race_dashboard = page.locator("//div[@class='profile-detailes-grid']/div[3]/p[2]").inner_text().strip()

            # Date selection (retain same clicks)
            page.locator("//div[@class='date-picker-wrap ng-star-inserted']//label[@class='date-picker-label']//img").click()
            time.sleep(1)
            page.locator("//div[@class='md-drppicker drops-down-auto ltr double show-ranges shown']//div[@class='ranges ng-star-inserted']/ul/li[2]"
            ).click()
            time.sleep(1)
            page.locator(calendar_path).click()
            page.locator(calendar_path).click()
            time.sleep(1)
            page.locator("//button[normalize-space()='Update']").click()
            time.sleep(5)

            # Clinical Values
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

            final_clinical_value = {}
            for label, value in results.items():
                if value in ("", "__", None):
                    final_clinical_value[label] = "Null"
                else:
                    # keep as float where possible (mirrors original behavior)
                    try:
                        final_clinical_value[label] = float(value)
                    except Exception:
                        final_clinical_value[label] = value



            hba1c_value_dashboard = final_clinical_value.get("HbA1c", "Null")
            ldl_value_dashboard = final_clinical_value.get("LDL Cholesterol", "Null")
            tg_value_dashboard = final_clinical_value.get("Triglycerides", "Null")
            tc_value_dashboard = final_clinical_value.get("Total Cholesterol", "Null")
            hdl_value_dashboard = final_clinical_value.get("HDL Cholesterol", "Null")
            fg_value_dashboard = final_clinical_value.get("Fasting Blood Glucose", "Null")

            # ---------------- Lifestyle Values ----------------
            page.locator("//span[@class='mdc-tab__text-label'][normalize-space()='Lifestyle']").click()
            time.sleep(10)

            lifestyle_labels = page.locator("//div[@id='wellness-score-dashboard']//ul//li//div/span").all_text_contents()
            lifestyle_values = page.locator("//div[@id='wellness-score-dashboard']//ul//li//div/p").all_text_contents()

            life_results = {}
            for label, value in zip(lifestyle_labels, lifestyle_values):
                label = label.strip()
                value = value.strip()
                if not value or value == "--":
                    life_results[label] = "Null"
                else:
                    if label.lower() == "sleep":
                        life_results[label] = value  # keep full string like "6 hrs 8 mins"
                    else:
                        match = re.findall(r"[-+]?[0-9]*\.?[0-9]+", value)
                        life_results[label] = float(match[0]) if match else value

            unhealthy_fats_dashboard = life_results.get("Unhealthy Oil & Fat", "Null")
            limit_sugar_dashboard = life_results.get("Limit Sugar", "Null")
            whole_grain_dashboard = life_results.get("Wholegrains", "Null")
            stress_dashboard = life_results.get("Stress", "Null")
            fruit_veg_dashboard = life_results.get("Fruit & Vegetables", "Null")
            alcohol_dashboard = life_results.get("Alcohol", "Null")
            smoking_dashboard = life_results.get("Smoking", "Null")
            mvpa_dashboard = life_results.get("MVPA", "Null")

            # View / Edit profile
            page.locator("//a[normalize-space()='View/Edit Profile']").click()
            time.sleep(3)

            employment_dashboard = page.locator("//div[@class='form-view-group']/div[9]/h6").inner_text().strip()
            industry_dashboard = ""
            work_wellness_prog_dashboard = ""
            if employment_dashboard == "Working":
                industry_dashboard = page.locator("//div[@class='form-view-group']/div[10]/h6").inner_text().strip()
                work_wellness_prog_dashboard = page.locator("//div[@class='form-view-group']/div[11]/h6").inner_text().strip()

            # Preferences
            page.locator("//div[normalize-space()='Preferences']").click()
            time.sleep(2)
            grocery_shopping_dashboard = page.locator("//div[@class='right-wrap']/div/div[3]/div[2]/span[1]").inner_text().strip()

            eating_out_dashboard = (
                get_text(page, "//div[@class='right-wrap']//div[@class='ng-star-inserted']/div[7]/div[2]")
                or get_text(page, "//div[@class='ack-modal']//div[4]//div[2]//span[1]")
            )

            # Physical Activity
            page.locator("//div[normalize-space()='Physical Activity']").click()
            physical_activity_dashboard = page.locator("//div[@class='right-wrap']//div[3]/div[2]/span[1]").inner_text().strip()

            # Chronic Medical Conditions
            page.locator("//div[normalize-space()='Chronic Medical Conditions']").click()
            time.sleep(2)
            items_locator = page.locator("//ul[@class='ng-star-inserted']/li")
            count = items_locator.count()
            chronic_medical_conditions_list_items = [
                re.sub(r"\s*\([^)]*\)", "", items_locator.nth(i).inner_text().strip()) for i in range(count)
            ]
            condition_self_dashboard = ",".join(chronic_medical_conditions_list_items)

            # Close edit profile
            page.get_by_role("img", name="Close").click()

            # Patient Logs
            page.locator("//a[normalize-space()='Patient Logs']").click()
            time.sleep(2)
            page.locator("//nz-date-picker[@id='overview-datepicker']").click()
            time.sleep(1)
            page.locator(f"//div[@aria-disabled='false'][normalize-space()='{date}']").click()
            time.sleep(2)

            sbp_self_dashboard = page.locator("//div[@class='info-row']/div[3]/div[2]").inner_text().strip()
            dbp_self_dashboard = page.locator("//div[@class='info-row']/div[4]/div[2]").inner_text().strip()
            sbp_clinic_dashboard = page.locator("//div[@class='info-row']/div[1]/div[2]").inner_text().strip()
            dbp_clinic_dashboard = page.locator("//div[@class='info-row']/div[2]/div[2]").inner_text().strip()

            Weight_value_dashboard = page.locator("//*[@id='overview-dashboards']/div/div[3]/div[1]/div/div[2]/div[1]/span[1]/span[1]").inner_text().strip()
            bmi_value_dashboard = page.locator("//body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[2]/div[1]/app-overview[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/span[1]"
            ).inner_text().strip()
            waist_value_dashboard = page.locator("//body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[2]/div[1]/app-overview[1]/div[3]/div[1]/div[4]/div[1]/div[1]/div[2]/span[1]/span[1]"
            ).inner_text().strip()
            # fg_value_dashboard = page.locator("//body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[2]/div[1]/app-overview[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/span[1]"
            # ).inner_text().strip()

            # Wellness plan
            page.locator("//a[@id='Wellness Plan']").click()
            time.sleep(2)
            issue_latest_wellness_plan_time_dashboard = ""
            if page.locator("//div[@id='report']").count() > 0:
                issue_latest_wellness_plan_time_dashboard = page.locator("//div[@id='dates']//div[1]/span[2]").inner_text().strip()

            # Fetch metrics from API helper (keeps same structure)
            metrics = fetch_patient_metrics(user["user_id"])
            clinical_ws_dashboard = metrics["clinical_ws_dashboard"]
            RHR_dashboard = metrics["RHR_dashboard"]
            hrv_val_dashboard = metrics["hrv_val_dashboard"]
            lifestyle_ws_dashboard = metrics["lifestyle_ws_dashboard"]
            steps_dashboard = metrics["steps_dashboard"]
            sedentary_time_dashboard = metrics["sedentary_time_dashboard"]
            sleep_dashboard = metrics["sleep_dashboard"]
            # mvpa_dashboard = metrics["mvpa_dashboard"]
            processed_food_dashboard = metrics["processed_food_dashboard"]



            # Extract CSV fields into variables (kept same names as original)
            # (This mirrors original code by assigning many fields from CSV row)

            user_id = user["user_id"]
            os_date = user.get("os_date")
            fitbit_device = user.get("fitbit_device")
            first_sync_timestamp = user.get("first_sync_timestamp")
            last_sync_timestamp = user.get("last_sync_timestamp")
            if last_sync_timestamp:
                dt_obj = datetime.strptime(last_sync_timestamp, "%Y-%m-%d %H:%M:%S")
                last_sync_timestamp = dt_obj.strftime("%d-%m-%y")
            else:
                last_sync_timestamp = ""

            pcc_intervention = user.get("pcc_intervention")
            pcc_timestamp = user.get("pcc_timestamp")
            termination_date = user.get("termination_date")
            age = user.get("age")
            sex = user.get("sex")
            race = user.get("race")
            employment = user.get("employment")
            industry = user.get("industry")
            work_wellness_prog = user.get("work_wellness_prog")
            grocery_shopping = user.get("grocery_shopping")
            eating_out = user.get("eating_out")
            physical_activity = user.get("physical_activity")
            condition_self = user.get("condition_self")
            condition_doctor = user.get("condition_doctor")
            condition_assessment = user.get("condition_assessment")
            wellness_clinical = user.get("wellness_clinical")
            wellness_lifestyle = user.get("wellness_lifestyle")
            sbp_self = user.get("sbp_self")
            dbp_self = user.get("dbp_self")
            sbp_clinic = user.get("sbp_clinic")
            dbp_clinic = user.get("dbp_clinic")
            rhr = user.get("rhr")
            hrv = user.get("hrv")
            fbg = user.get("fbg")
            hba1c = user.get("hba1c")
            tchol = user.get("tchol")
            hdl = user.get("hdl")
            ldl = user.get("ldl")
            tg = user.get("tg")
            weight = user.get("weight")
            bmi = user.get("bmi")
            wc = user.get("wc")
            assessment_date = user.get("assessment_date")
            steps = user.get("steps")
            mvpa = user.get("mvpa")
            sedentary_time = user.get("sedentary_time")
            sleep = user.get("sleep")
            smoking = user.get("smoking")
            alcohol = user.get("alcohol")
            processed_food = user.get("processed_food")
            if processed_food == "No":
                processed_food = "Seldom/Never"
            else:
                processed_food = "Often"

            unhealthy_oil_fat = user.get("unhealthy_oil_fat")
            fruit_vegetables = user.get("fruit_vegetables")
            wholegrains = user.get("wholegrains")
            limit_sugar = user.get("limit_sugar")
            stress = user.get("stress")
            open_app_daily = user.get("open_app_daily")
            parameters_open = user.get("parameters_open")
            wellness_trend_open = user.get("wellness_trend_open")
            wellness_plan_open = user.get("wellness_plan_open")
            wellness_score_duration = user.get("wellness_score_duration")
            wellness_trend_duration = user.get("wellness_trend_duration")
            wellness_plan_duration = user.get("wellness_plan_duration")
            wellness_plan_download = user.get("wellness_plan_download")
            wellness_plan_download_timestamp = user.get("wellness_plan_download_timestamp")
            health_msgs_received = user.get("health_msgs_received")
            health_msgs_opened = user.get("health_msgs_opened")
            bp_alerts_received = user.get("bp_alerts_received")
            bp_alerts_opened = user.get("bp_alerts_opened")
            exercise_received = user.get("exercise_received")
            exercise_opened = user.get("exercise_opened")
            rhs_completed = user.get("rhs_completed")
            rhs_timestamp = user.get("rhs_timestamp")
            rhs_number = user.get("rhs_number")
            yt_vids_duration = user.get("yt_vids_duration")
            doctor_id_engagement = user.get("doctor_id_engagement")
            clinic = initials(user.get("clinic", ""))
            record_open_time = user.get("record_open_time")
            issue_latest_wellness_plan_time = user.get("issue_latest_wellness_plan_time")
            final_consult = user.get("final_consult")
            wellness_trend_open_doc = user.get("wellness_trend_open_doc")
            clinical_paras_open = user.get("clinical_paras_open")
            lifestyle_paras_open = user.get("lifestyle_paras_open")
            comparison_open = user.get("comparison_open")
            lifestyle_recs_selected = user.get("lifestyle_recs_selected")
            lifestyle_recs_specific = user.get("lifestyle_recs_specific")
            pt_presurvey_date = user.get("pt_presurvey_date")
            # ... many other fields omitted here for brevity but you can add more as needed
            # (the original script listed many fields; if you rely on any omitted ones, please re-add following same pattern)

            # ------------------------
            # 🔹 Full Comparison Block (prints mismatches)
            # ------------------------

            # Date fields
            if not values_match(os_date, os_date_dashboard, date=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV os_date: {os_date} | Dashboard os_date: {os_date_dashboard}")

            if (
                    (last_sync_timestamp or last_sync_timestamp_dashboard)  # at least one has data
                    and not values_match(last_sync_timestamp, last_sync_timestamp_dashboard, date=True)
            ):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV last_sync_timestamp: {last_sync_timestamp} | Dashboard last_sync_timestamp: {last_sync_timestamp_dashboard}"
                )

            # PCC intervention
            if not values_match(pcc_intervention, pcc_intervention_dashboard, case="ignore"):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV PCC Intervention: {pcc_intervention} | Dashboard PCC Intervention: {pcc_intervention_dashboard}"
                )

            # Basic info
            if not values_match(age, age_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV age: {age} | Dashboard age: {age_dashboard}")

            if not values_match(sex, sex_dashboard, case="lower"):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV sex: {sex} | Dashboard sex: {sex_dashboard}")

            if not values_match(race, race_dashboard, case="upper"):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV race: {race} | Dashboard race: {race_dashboard}")

            # Wellness metrics
            if not values_match(wellness_clinical, clinical_ws_dashboard):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV clinical_ws: {wellness_clinical} | Dashboard clinical_ws: {clinical_ws_dashboard}"
                )

            if not values_match(weight, Weight_value_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV Weight: {bmi} | Dashboard Weight value: {Weight_value_dashboard}")

            bmi_value_dashboard = str(bmi_value_dashboard).replace("kg/m2", "").strip()
            if not values_match(bmi, bmi_value_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV BMI: {bmi} | Dashboard BMI: {bmi_value_dashboard}")

            if not values_match(wc, waist_value_dashboard, numeric=True):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV Waist Circumference: {wc} | Dashboard Waist Circumference: {waist_value_dashboard}"
                )

            # Blood & glucose
            if not values_match(hba1c, hba1c_value_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV HbA1c: {hba1c} | Dashboard HbA1c: {hba1c_value_dashboard}")

            if not values_match(fbg, fg_value_dashboard, numeric=True):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV Fasting Glucose: {fbg} | Dashboard Fasting Glucose: {fg_value_dashboard}"
                )

            if not values_match(ldl, ldl_value_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV LDL: {ldl} | Dashboard LDL: {ldl_value_dashboard}")

            if not values_match(tg, tg_value_dashboard, numeric=True):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV Triglycerides: {tg} | Dashboard Triglycerides: {tg_value_dashboard}"
                )

            if not values_match(tchol, tc_value_dashboard, numeric=True):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV tc_value: {tchol} | Dashboard tc_value_dashboard: {tc_value_dashboard}"
                )

            if not values_match(hdl, hdl_value_dashboard, numeric=True):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV hdl_value: {hdl} | Dashboard hdl_value_dashboard: {hdl_value_dashboard}"
                )

            # Heart & activity
            if not values_match(rhr, RHR_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV Resting Heart Rate: {rhr} | Dashboard RHR: {RHR_dashboard}")

            if not values_match(hrv, hrv_val_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV HRV: {hrv} | Dashboard HRV: {hrv_val_dashboard}")

            if not values_match(wellness_lifestyle, lifestyle_ws_dashboard):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV lifestyle_ws: {wellness_lifestyle} | Dashboard lifestyle_ws: {lifestyle_ws_dashboard}"
                )

            if not values_match(steps, steps_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV Steps: {steps} | Dashboard Steps: {steps_dashboard}")

            if not values_match(sedentary_time, sedentary_time_dashboard, numeric=True):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV Sedentary Time: {sedentary_time} | Dashboard Sedentary Time: {sedentary_time_dashboard}"
                )

            if not values_match(sleep, sleep_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV sleep: {sleep} | Dashboard sleep: {sleep_dashboard}")

            if not values_match(mvpa, mvpa_dashboard, numeric=True):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV mvpa: {mvpa} | Dashboard MVPA: {mvpa_dashboard}")

            # Lifestyle / Diet (ignore case)
            diet_fields = [
                ("Unhealthy Fats", unhealthy_oil_fat, unhealthy_fats_dashboard),
                ("Limit Sugar", limit_sugar, limit_sugar_dashboard),
                ("Whole Grain", wholegrains, whole_grain_dashboard),
                ("Stress", stress, stress_dashboard),
                ("Processed Food", processed_food, processed_food_dashboard),
                ("Fruit & Vegetables", fruit_vegetables, fruit_veg_dashboard),
                ("Alcohol", alcohol, alcohol_dashboard),
                ("Smoking", smoking, smoking_dashboard),
            ]

            for name, csv_val, dash_val in diet_fields:
                if name in ["Fruit & Vegetables", "MVPA", "Sleep"]:
                    numeric = True
                else:
                    numeric = False
                if not values_match(csv_val, dash_val, numeric=numeric, case="ignore"):
                    print(f"⚠️  Mismatch → user_id {user_id} | CSV {name}: {csv_val} | Dashboard {name}: {dash_val}")

            # Employment / Work fields
            work_fields = [
                ("Employment", employment, employment_dashboard),
                ("Industry", industry, industry_dashboard),
                ("Work Wellness Program", work_wellness_prog, work_wellness_prog_dashboard),
                ("Grocery Shopping", grocery_shopping, grocery_shopping_dashboard),
                ("Eating Out", eating_out, eating_out_dashboard),
                ("Physical Activity", physical_activity, physical_activity_dashboard),
            ]

            for name, csv_val, dash_val in work_fields:
                if not values_match(csv_val, dash_val, case="ignore"):
                    print(f"⚠️  Mismatch → user_id {user_id} | CSV {name}: {csv_val} | Dashboard {name}: {dash_val}")

            # Conditions
            csv_clean = strip_parentheses(condition_self)
            dash_clean = strip_parentheses(condition_self_dashboard)
            if not values_match(csv_clean, dash_clean, case="ignore"):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV Self Conditions: {condition_self} | Dashboard Self Conditions: {condition_self_dashboard}"
                )

            # Clinic → remove prefix Clinic and compare initials
            if not values_match(clinic, clinic_dashboard, case="ignore", strip_prefix="Clinic"):
                print(f"⚠️  Mismatch → user_id {user_id} | CSV Clinic: {clinic} | Dashboard Clinic: {clinic_dashboard}")

            # Blood pressure numeric ignoring units
            bp_fields = [
                ("SBP (Self)", sbp_self, sbp_self_dashboard),
                ("DBP (Self)", dbp_self, dbp_self_dashboard),
                ("SBP (Clinic)", sbp_clinic, sbp_clinic_dashboard),
                ("DBP (Clinic)", dbp_clinic, dbp_clinic_dashboard),
            ]
            for name, csv_val, dash_val in bp_fields:
                if not values_match(csv_val, dash_val, numeric=True):
                    print(f"⚠️  Mismatch → user_id {user_id} | CSV {name}: {csv_val} | Dashboard {name}: {dash_val}")

            # Latest wellness plan time
            if normalize_datetime(issue_latest_wellness_plan_time) != normalize_datetime(issue_latest_wellness_plan_time_dashboard):
                print(
                    f"⚠️  Mismatch → user_id {user_id} | CSV Issue Latest Wellness Plan Time: {issue_latest_wellness_plan_time} | Dashboard Issue Latest Wellness Plan Time: {issue_latest_wellness_plan_time_dashboard}"
                )

            # Return to My Users for next iteration
            page.locator("//span[normalize-space()='My Users']").click()
            # short wait to allow next search
            time.sleep(1)

        # close browser at end
        browser.close()


if __name__ == "__main__":
    main()

