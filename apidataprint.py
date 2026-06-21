

base_url = "https://hpb-uat-api.connectedlife.io"

import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from ddtest import calendar_path, endDate, date


# Convert imported endDate to datetime object
end_date_obj = datetime.strptime(endDate, "%Y-%m-%d")
startDate_step = (end_date_obj - timedelta(days=6)).strftime("%Y-%m-%d")
startDate_mpva = (end_date_obj - timedelta(days=12)).strftime("%Y-%m-%d")


def get_latest_value(history: List[Dict[str, Any]], value_key: str = "value") -> Optional[Any]:
    """
    Get the latest non-zero, non-None value from history.
    """
    for entry in reversed(history):
        if value_key in entry and entry[value_key] not in [None, 0]:
            return entry[value_key]
    return None


def fetch_patient_metrics(patient_id: int, end_date: str = "2025-09-05") -> Dict[str, Any]:
    """
    Fetch wellness and other health metrics for a patient and return a dictionary.
    patient_id can be int or str (auto-converted to int).
    """
    try:
        patient_id = int(patient_id)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid patient_id: {patient_id}")

    # ---- Credentials ----
    EMAIL = "hpbfullerton22+STM1@gmail.com"
    PASSWORD = "U2FsdGVkX18Kl7OJsyiNrVvckuuPUC5gizrCss3vvno="
    OTP = "312800"

    session = requests.Session()

    # ---- Login ----
    login_url = f"{base_url}/user-jwt/auth/login"
    response = session.post(login_url, json={"userId": EMAIL, "password": PASSWORD})
    response.raise_for_status()
    login_data = response.json()
    temp_token = login_data.get("tempToken")
    roleId = login_data.get("patientId")

    # ---- OTP Verification ----
    otp_url = f"{base_url}/user-management/user/verify-2fa-pin-dashboard"
    response = session.post(
        otp_url,
        json={"patientId": roleId, "pin": OTP},
        headers={"Authorization": f"Bearer {temp_token}"}
    )
    response.raise_for_status()
    auth_token = response.json().get("token")
    session.headers.update({"Authorization": f"Bearer {auth_token}"})

    # ---- Onboard Date ----
    onboard_url = f"{base_url}/user-management/user/onboard-date"
    response = session.post(onboard_url, json={"patientId": patient_id}, headers={'organisationid': '2'})
    onboard_date = response.json().get('data', {}).get('onBoardDate', end_date)

    # ---- Result dict ----
    result: Dict[str, Any] = {}

    # ---- Wellness Scores ----
    ws_url = f"{base_url}/wellness-score-snapshots/wellness-score/userAnalytics"
    for metric in ["clinical", "lifestyle"]:
        response = session.post(ws_url, json={
            "patientId": patient_id,
            "startDate": end_date,
            "endDate": end_date,
            "flag": "day",
            "metric": metric
        }
                                )
        data = response.json()
        history = data.get("history", [])
        result[f"{metric}_ws_dashboard"] = get_latest_value(history)


    # ---- MVPA Rolling Window logic ----
    mvpa_found = False
    guard_rail = 14  # Guardrail: stop searching after 14 days
    mvpa_url = f"{base_url}/activity-classification/activityClassification/Exercise/userAnalytics"
    current_end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    for i in range(guard_rail + 1):
        current_start_dt = current_end_dt - timedelta(days=6)
        start_date_str = current_start_dt.strftime("%Y-%m-%d")
        end_date_str = current_end_dt.strftime("%Y-%m-%d")

        # print(f"Checking MVPA window: {start_date_str} -> {end_date_str}")

        try:
            payload = {
                "patientId": patient_id,
                "startDate": start_date_str,
                "endDate": end_date_str,
                "flag": "week"
            }
            response = session.post(mvpa_url, json=payload)
            response.raise_for_status()
            data = response.json()

            if i == 0:
                if data and data.get("total") is not None and data.get("total") > 0:
                    result["mvpa_dashboard"] = data.get("total")
                    mvpa_found = True
                    break
                else:
                    print(" MVPA First query returned 0. Sliding window...")
            else:
                latest_value = get_latest_value(data.get("history", []))
                if latest_value is not None:
                    result["mvpa_dashboard"] = latest_value
                    mvpa_found = True
                    break

        except requests.exceptions.RequestException as e:
            print(f"API call for MVPA failed at {start_date_str} -> {end_date_str}: {e}")

        current_end_dt -= timedelta(days=1)

    if not mvpa_found:
        result["mvpa_dashboard"] = None
        print("No MVPA data found within the specified guard rail period.")

    # ---- Other Metrics 
    metrics_map = {
        "hrv_val_dashboard": "/hrm/hrv/userAnalytics",
        "RHR_dashboard": "/hrm/resting-heart-rate/userAnalytics",
        "steps_dashboard": "/step-sleep/common/steps/userAnalytics",
        "sedentary_time_dashboard": "/step-sleep/sedentaryTime/userAnalytics",
        "sleep_dashboard": "/step-sleep/common/sleep/userAnalytics",
        "processed_food_dashboard": "/selfLabel/patient/selfLabel/userAnalytics"
    }

    for key, path in metrics_map.items():
        if key == "processed_food_dashboard":
            payload = {
                "patientId": patient_id,
                "startDate": onboard_date,
                "endDate": end_date,
                "metric": "processedfood",
                "flag": "week"
            }
        elif key in ["steps_dashboard"]:
            payload = {
                "patientId": patient_id,
                "startDate": onboard_date,
                "endDate": end_date,
                "flag": "week"
            }
        else:
            payload = {
                "patientId": patient_id,
                "startDate": onboard_date,
                "endDate": end_date,
                "flag": "week"
            }

        response = session.post(f"{base_url}{path}", json=payload)
        data = response.json()
        result[key] = get_latest_value(data.get("history", []))

    return result
