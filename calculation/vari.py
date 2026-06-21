# from clinical_ws import clinical_WS
#
# final_clinical_value = {
#     'Body Mass Index': 21.6,
#     'Waist Circumference': 81.0,
#     'Systolic': 120.0,
#     'Diastolic': 80.0,
#     'Fasting Blood Glucose': 5.4,
#     'HbA1c': 3.4,
#     'HDL Cholesterol': 5.0,
#     'Resting Heart Rate': 'Null',
#     'Heart Rate Variability': 'Null',
#     'LDL Cholesterol': 3.0,
#     'Triglycerides': 2.0,
#     'Total Cholesterol': 8.0
# }
#
# score = clinical_WS(
#     gender="male",
#     bmi_value=final_clinical_value['Body Mass Index'],
#     waist_value=final_clinical_value['Waist Circumference'],
#     systolic=final_clinical_value['Systolic'],
#     diastolic=final_clinical_value['Diastolic'],
#     hba1c_value=final_clinical_value['HbA1c'],
#     fg_value=final_clinical_value['Fasting Blood Glucose'],
#     ldl_value=final_clinical_value['LDL Cholesterol'],
#     tg_value=final_clinical_value['Triglycerides'],
#     RHR=final_clinical_value['Resting Heart Rate'],
#     hrv_val=final_clinical_value['Heart Rate Variability']
# )
#
# print("Clinical Score:", score)
from lifestyle_ws import lifestyle_WS

gender = "male"
life_results = {'Alcohol': 'No', 'Smoking': 'No', 'Steps': 6696.0, 'Sleep': 12.0, 'Processed Food': 'No', 'Fruit & Vegetables': 4.0, 'MVPA': 181.0, 'Stress': 'Seldom/Never', 'Sedentary Time': 669.0, 'Limit Sugar': 'Seldom/Never', 'Wholegrains': 'Sometimes', 'Unhealthy Oil & Fat': 'Often'}


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


score = lifestyle_WS(
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
print("Score:", score)