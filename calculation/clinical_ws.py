import math
def clinical_WS(gender,bmi_value,waist_value, systolic, diastolic, hba1c_value, fg_value, ldl_value, tg_value, RHR, hrv_val):
    # gender = input("Enter gender (Female/Male): ").strip().lower()

    def evaluate_bmi(value):
        if 18.5 <= value <= 22.9:
            return 1.0
        elif value >= 23:
            return 1.15
        elif value < 18.5:
            return 1.66
        else:
            return None

    # bmi_value = float(input("Enter BMI: "))
    bmi_multiplier = evaluate_bmi(bmi_value)

    def evaluate_waist_men(value):
        if value <= 90:
            return 1.0
        elif value > 90:
            return 1.1
        else:
            return None

    def evaluate_waist_women(value):
        if value <= 80:
            return 1.0
        elif value > 80:
            return 1.15
        else:
            return None

    # waist_value = float(input("Enter Waist Circumference (cm): "))
    if gender == "male":
        waist_multiplier = evaluate_waist_men(waist_value)
    elif gender == "female":
        waist_multiplier = evaluate_waist_women(waist_value)
    else:
        waist_multiplier = None

    def evaluate_systolic(systolic):
        if systolic <= 90:
            return 1.31
        elif 91 <= systolic <= 120:
            return 1.00
        elif 121 <= systolic <= 130:
            return 1.13
        elif systolic > 130:
            return 1.40
        else:
            return None

    def evaluate_diastolic(diastolic):
        if diastolic <= 60:
            return 1.31
        elif 61 <= diastolic <= 80:
            return 1.00
        elif diastolic > 80:
            return 1.40
        else:
            return None

    # systolic = float(input("Enter Systolic BP (mmHg): "))
    # diastolic = float(input("Enter Diastolic BP (mmHg): "))

    sys_multiplier = evaluate_systolic(systolic)
    dia_multiplier = evaluate_diastolic(diastolic)

    if sys_multiplier > dia_multiplier:
        blood_pressure_multiplier = sys_multiplier
    else:
        blood_pressure_multiplier = dia_multiplier

    def evaluate_hba1c(value):
        if value <= 6:
            return value, 1.0
        elif 6 < value < 7.0:
            return value, 1.04
        elif value >= 7.0:
            return value, 1.77
        else:
            return value, None

    # hba1c_value = float(input("Enter HbA1c (%): "))
    hba1c_total, hba1c_multiplier = evaluate_hba1c(hba1c_value)

    def evaluate_fasting_glucose(value):
        if value <= 6.0:
            return value, 1.0
        elif 6.0 < value < 7.0:
            return value, 1.17
        elif value >= 7.0:
            return value, 2.23
        else:
            return value, None

    # fg_value = float(input("Enter Fasting Glucose (mmol/L): "))
    fg_total, fg_multiplier = evaluate_fasting_glucose(fg_value)

    def evaluate_ldl(value):
        if value < 2.6:
            return value, 1.0
        elif value >= 2.6:
            return value, 1.33
        else:
            return value, None

    # ldl_value = float(input("Enter LDL (mmol/L): "))
    ldl_total, ldl_multiplier = evaluate_ldl(ldl_value)

    def evaluate_triglycerides(value):
        if value < 1.7:
            return 1.0
        elif value >= 1.7:
            return 1.19
        else:
            return None

    # tg_value = float(input("Enter TG (mmol/L): "))
    triglycerides_multiplier = evaluate_triglycerides(tg_value)

    def evaluate_resting_hr(RHR):
        if 50 <= RHR <= 70:
            return 1.00
        elif 70.001 <= RHR <= 80:
            return 1.30
        elif 80.001 <= RHR <= 90:
            return 1.69
        elif 90.001 <= RHR <= 100:
            return 2.19
        elif 100.001 <= RHR <= 110:
            return 2.84
        elif 110.001 <= RHR <= 120:
            return 3.68
        elif RHR > 120:
            return 4.78
        else:
            return None

    if RHR == "Null":
        resting_hr_multiplier = 0
    else:
        resting_hr_multiplier = evaluate_resting_hr(RHR)

    def evaluate_hrv_female(hrv):
        if 0 <= hrv <= 18.8:
            return 1.18
        elif hrv > 18.9:
            return 0.96
        else:
            return None

    def evaluate_hrv_male(hrv):
        if 0 <= hrv <= 18.8:
            return 1.11
        elif hrv > 18.9:
            return 1.00
        else:
            return None

    # hrv_val = input("Enter HRV (ms): ")
    if hrv_val == "Null":
        hrv_multiplier = 0
    else:
        if gender == "female":
            hrv_multiplier = evaluate_hrv_female(hrv_val)
        else:
            hrv_multiplier = evaluate_hrv_male(hrv_val)


    def safe_add(*args):
        return sum([val for val in args if isinstance(val, (int, float))])

    clinical_Total_HR = safe_add(
        bmi_multiplier, waist_multiplier, blood_pressure_multiplier,
        hba1c_multiplier, fg_multiplier, ldl_multiplier,
        triglycerides_multiplier, resting_hr_multiplier, hrv_multiplier
    )

    def safe_weightage(multiplier, total_hr):
        if multiplier is None or total_hr in (None, 0):
            return 0
        return (multiplier / total_hr) * 100

    Weightage_bmi = safe_weightage(bmi_multiplier, clinical_Total_HR)
    Weightage_waist = safe_weightage(waist_multiplier, clinical_Total_HR)
    Weightage_blood_pressure = safe_weightage(blood_pressure_multiplier, clinical_Total_HR)
    Weightage_hba1c = safe_weightage(hba1c_multiplier, clinical_Total_HR)
    Weightage_fg = safe_weightage(fg_multiplier, clinical_Total_HR)
    Weightage_ldl = safe_weightage(ldl_multiplier, clinical_Total_HR)
    Weightage_triglycerides = safe_weightage(triglycerides_multiplier, clinical_Total_HR)
    Weightage_resting_hr = safe_weightage(resting_hr_multiplier, clinical_Total_HR)
    Weightage_hrv = safe_weightage(hrv_multiplier, clinical_Total_HR)

    def safe_exp_calculation(multiplier, reference=1.0):
        if multiplier is None:
            return 0
        else:
            return math.exp(-(((multiplier / reference) ** 2) - 1))

    bmi_Exponential_Function = safe_exp_calculation(bmi_multiplier)
    waist_Exponential_Function = safe_exp_calculation(waist_multiplier)
    blood_pressure_Exponential_Function = safe_exp_calculation(blood_pressure_multiplier)
    hba1c_Exponential_Function = safe_exp_calculation(hba1c_multiplier)
    fg_Exponential_Function = safe_exp_calculation(fg_multiplier)
    ldl_Exponential_Function = safe_exp_calculation(ldl_multiplier)
    triglycerides_Exponential_Function = safe_exp_calculation(triglycerides_multiplier)
    resting_hr_Exponential_Function = safe_exp_calculation(resting_hr_multiplier)
    hrv_Exponential_Function = safe_exp_calculation(hrv_multiplier)

    bmi = Weightage_bmi * bmi_Exponential_Function
    waist = Weightage_waist * waist_Exponential_Function
    blood_pressure = Weightage_blood_pressure * blood_pressure_Exponential_Function
    hba1c = Weightage_hba1c * hba1c_Exponential_Function
    fg = Weightage_fg * fg_Exponential_Function
    ldl = Weightage_ldl * ldl_Exponential_Function
    triglycerides = Weightage_triglycerides * triglycerides_Exponential_Function
    resting_hr = Weightage_resting_hr * resting_hr_Exponential_Function
    hrv = Weightage_hrv * hrv_Exponential_Function

    clinical_score_sum = round(safe_add(
        bmi, waist, blood_pressure, hba1c, fg, ldl, triglycerides, resting_hr, hrv
    ))

    return clinical_score_sum

