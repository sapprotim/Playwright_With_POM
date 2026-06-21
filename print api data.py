import requests
import json
from datetime import datetime, timedelta

patientId = [837896171, 2050514129, 2026484010]
endDate = "2025-09-05"

def get_latest_value(history, value_key="value"):
    """
    Iterate from last to first in history and return first non-null, non-zero value.
    """
    for entry in reversed(history):
        if value_key in entry and entry[value_key] not in [None, 0]:
            return entry[value_key]
    return None  # fallback if all null or zero

for patient_ids in patientId:
    print(f"\n\nProcessing for Patient ID: {patient_ids}")

    # Login
    url = "https://hpb-uat-api.connectedlife.io/user-jwt/auth/login"
    payload = json.dumps({
        "userId": "hpbfullerton22+STM1@gmail.com",
        "password": "U2FsdGVkX18Kl7OJsyiNrVvckuuPUC5gizrCss3vvno="
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)

    login_data = response.json()
    roleId = login_data["patientId"]
    temp_token = login_data["tempToken"]

    # OTP
    url = "https://hpb-uat-api.connectedlife.io/user-management/user/verify-2fa-pin-dashboard"
    payload = {"patientId": roleId, "pin": "312800"}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {temp_token}"}
    response = requests.post(url, headers=headers, json=payload)

    login_data = response.json()
    auth_token = login_data["token"]

    # Onboarding date
    url = "https://hpb-uat-api.connectedlife.io/user-management/user/onboard-date"
    payload = json.dumps({"patientId": patient_ids})
    headers = {
        'accept': 'application/json, text/plain, /',
        'authorization': f'Bearer {auth_token}',
        'content-type': 'application/json',
        'organisationid': '2'
    }
    response = requests.post(url, headers=headers, data=payload)
    onb_data = response.json()

    if 'data' in onb_data and 'onBoardDate' in onb_data['data']:
        onboarddate = onb_data['data']['onBoardDate']
    else:
        onboarddate = endDate
        print(f"No onboarding date found for Patient ID {patient_ids}, using endDate as fallback.")

    print("Onboarding date:", onboarddate)

    # Wellness Score – Clinical & Lifestyle (latest value)
    ws_url = "https://hpb-uat-api.connectedlife.io/wellness-score-snapshots/wellness-score/userAnalytics"
    for metric in ["clinical", "lifestyle"]:
        last_value = None
        check_date = endDate
        attempts = 0

        while last_value is None and attempts < 30:  # check max 30 days back
            payload = json.dumps({
                "patientId": patient_ids,
                "startDate": check_date,
                "endDate": check_date,
                "flag": "day",
                "metric": metric
            })
            headers_ws = {'Content-Type': 'application/json', 'Authorization': f'Bearer {auth_token}'}
            response = requests.post(ws_url, headers=headers_ws, data=payload)
            data = response.json()

            # Check if 'history' or 'data' exists
            if "history" in data and data["history"]:
                last_value = get_latest_value(data["history"])
            elif "data" in data and isinstance(data["data"], list) and data["data"]:
                for entry in reversed(data["data"]):
                    if 'value' in entry and entry['value'] not in [None, 0]:
                        last_value = entry['value']
                        break

            if last_value is None:
                dt = datetime.strptime(check_date, "%Y-%m-%d") - timedelta(days=1)
                check_date = dt.strftime("%Y-%m-%d")
                attempts += 1

        print(f"Wellness Score {metric.capitalize()} (latest):", last_value if last_value is not None else "No data available")

    # Other metrics
    metrics = {
        "HRV": ("https://hpb-uat-api.connectedlife.io/hrm/hrv/userAnalytics", "value"),
        "Resting Heart Rate": ("https://hpb-uat-api.connectedlife.io/hrm/resting-heart-rate/userAnalytics", "value"),
        "Steps": ("https://hpb-uat-api.connectedlife.io/step-sleep/common/steps/userAnalytics", "value"),
        "MVPA": ("https://hpb-uat-api.connectedlife.io/activity-classification/activityClassification/Exercise/userAnalytics", "value"),
        "Sedentary time": ("https://hpb-uat-api.connectedlife.io/step-sleep/sedentaryTime/userAnalytics", "value"),
        "Sleep": ("https://hpb-uat-api.connectedlife.io/step-sleep/common/sleep/userAnalytics", "value")
    }

    for metric_name, (url, value_key) in metrics.items():
        payload = json.dumps({
            "patientId": patient_ids,
            "startDate": onboarddate,
            "endDate": endDate,
            "flag": "week"
        })
        response = requests.post(url, headers=headers_ws, data=payload)
        data = response.json()
        if "history" in data:
            latest = get_latest_value(data["history"], value_key=value_key)
            print(f"{metric_name} (latest):", latest)
        else:
            print(f"{metric_name} (latest): No data available")