import math 


def lifestyle_WS(gender, step, time, unhealthy_fats, limit_sugar, whole_grain, stress, processed_food, fruit_veg, sleep, mvpa, alcohol, smoking):
    def evaluate_step(step):
        if 0 <= step <= 1500:
            return 2.74
        elif 1501 <= step <= 3000:
            return 1.96
        elif 3001 <= step <= 5000:
            return 1.27
        elif 5001 <= step <= 5800:
            return 1.00
        elif 5801 <= step <= 8500:
            return 0.60
        elif step >= 8501:
            return 0.48
        else:
            return 0
    
    # step = input("Enter step: ")
    if step == "Null" or step == "null" or step == "":
        step_multiplier = 0
    else:
        step_multiplier = float(evaluate_step(step))
    
    def evaluate_sedentary_time(time):
        if 0 <= time <= 560:
            return 0.37
        elif 561 <= time <= 600:
            return 0.44
        elif 601 <= time <= 640:
            return 0.53
        elif 641 <= time <= 680:
            return 0.66
        elif 681 <= time <= 720:
            return 0.81
        elif 721 <= time <= 760:
            return 0.99
        elif 761 <= time <= 800:
            return 1.22
        elif 801 <= time <= 840:
            return 1.50
        elif 841 <= time <= 880:
            return 1.88
        elif time >= 881:
            return 2.23
        else:
            return 0
    
    # time = input("Enter sedentary time in minutes: ")
    if time == "Null" or time == "null" or time == "":
        sedentary_time_multiplier = 0
    else:
        time = math.floor(float(time))
        sedentary_time_multiplier = float(evaluate_sedentary_time(time))
    
    def evaluate_unhealthy_fats(unhealthy_fats):
        frequency = unhealthy_fats.strip().lower()
        if frequency in ["seldom", "never", "seldom/never"]:
            return 0.98
        elif frequency == "sometimes":
            return 1.04
        elif frequency == "often":
            return 1.08
        else:
            return 0
    
    # unhealthy_fats = input("Enter frequency for unhealthy_fats : (Seldom / Never, Sometimes, Often): ")
    unhealthy_fats_multiplier = float(evaluate_unhealthy_fats(unhealthy_fats))
    
    def evaluate_limit_sugar(limit_sugar):
        limit_sugar = limit_sugar.strip().lower()
        if limit_sugar == "often":
            return 0.96
        elif limit_sugar == "sometimes":
            return 0.99
        elif limit_sugar in ["seldom", "never", "seldom/never"]:
            return 1.15
        else:
            return 0
    
    # limit_sugar = input("Enter sugar intake frequency (Often, Sometimes, Seldom / Never): ")
    limit_sugar_multiplier = float(evaluate_limit_sugar(limit_sugar))
    
    def evaluate_whole_grain_intake(whole_grain):
        whole_grain = whole_grain.strip().lower()
        if whole_grain in ["seldom", "never", "seldom/never"]:
            return 0.88
        elif whole_grain == "sometimes":
            return 0.80
        elif whole_grain == "often":
            return 0.79
        else:
            return 0
    
    # whole_grain = input("Enter whole grain intake frequency (Seldom / Never, Sometimes, Often): ")
    whole_grain_multiplier = float(evaluate_whole_grain_intake(whole_grain))
    
    def evaluate_stress_level(stress):
        stress = stress.strip().lower()
        if stress in ["seldom", "never", "seldom/never"]:
            return 0.18
        elif stress == "sometimes":
            return 0.59
        elif stress == "often":
            return 1.00
        else:
            return 0
    
    # stress = input("Enter stress frequency (Seldom/Never, Sometimes, Often): ")
    stress_multiplier = float(evaluate_stress_level(stress))
    
    def evaluate_processed_food_male(answer):
        answer = answer.strip().lower()
        if answer == "no":
            return 1.00
        elif answer == "yes":
            return 1.27
        else:
            return 0
    
    def evaluate_processed_food_female(answer):
        answer = answer.strip().lower()
        if answer == "no":
            return 1.00
        elif answer == "yes":
            return 1.30
        else:
            return 0
    
    # processed_food = input("Processed Food Intake? (Yes/No): ")
    if gender == "male":
        processed_food_multiplier = float(evaluate_processed_food_male(processed_food))
    else:
        processed_food_multiplier= float(evaluate_processed_food_female(processed_food))

    
    def evaluate_fruit_veg_intake(fruit_veg):
        if 0 <= fruit_veg <= 3:
            return 1.0
        elif 4 <= fruit_veg <= 20:
            return 0.64
        else:
            return 0
    
    # fruit_veg = float(input("Fruit & Vegetable servings: "))
    fruit_veg_multiplier = float(evaluate_fruit_veg_intake(fruit_veg))
    
    def evaluate_mvpa(mvpa):
        if mvpa == 0:
            return 1.0
        elif 1 <= mvpa <= 19:
            return 0.91
        elif 20 <= mvpa <= 59:
            return 0.83
        elif 60 <= mvpa <= 149:
            return 0.76
        elif 150 <= mvpa <= 179:
            return 0.70
        elif 180 <= mvpa <= 219:
            return 0.64
        elif 220 <= mvpa <= 259:
            return 0.59
        elif mvpa >= 260:
            return 0.55
        else:
            return 0

    if mvpa == "Null" or mvpa == "null" or mvpa == "":
        mvpa_multiplier = 0
    else:
        mvpa_multiplier = evaluate_mvpa(mvpa)
    
    def evaluate_sleep(sleep):
        if sleep < 7:
            return 1.45
        elif sleep >= 7:
            return 1.0
        else:
            return 0
    
    # sleep = input("Sleep hours: ")
    if sleep == "Null" or sleep == "null" or sleep == "":
        sleep_multiplier = 0
    else:
        sleep_multiplier= float(evaluate_sleep(sleep))
    
    def evaluate_alcohol(alcohol):
        alcohol = alcohol.strip().lower()
        if alcohol == "no":
            return 0.91
        elif alcohol == "yes":
            return 1.33
        else:
            return 0
    
    # alcohol = input("Alcohol consumption (Yes/No): ")
    alcohol_multiplier = float(evaluate_alcohol(alcohol))
    
    def evaluate_smoking(smoking):
        smoking = smoking.strip().lower()
        if smoking == "no":
            return 1.0
        else:
            return 1.46
    
    # smoking = input("Smoking (Yes/No): ")
    smoking_multiplier = float(evaluate_smoking(smoking))

    def safe_add(*args):
        return sum([val for val in args if isinstance(val, (int, float))])
    
    lifestyle_Total_HR = safe_add(step_multiplier, mvpa_multiplier, sedentary_time_multiplier, processed_food_multiplier, fruit_veg_multiplier,
                                  whole_grain_multiplier, unhealthy_fats_multiplier, limit_sugar_multiplier, alcohol_multiplier, smoking_multiplier,
                                  sleep_multiplier, stress_multiplier)
    
    def safe_weightage(multiplier, total_hr):
        if multiplier is None or total_hr in (None, 0):
            return 0
        return (multiplier / total_hr) * 100
    
    Weightage_step = safe_weightage(step_multiplier, lifestyle_Total_HR)
    Weightage_mvpa = safe_weightage(mvpa_multiplier, lifestyle_Total_HR)
    Weightage_sedentary_time = safe_weightage(sedentary_time_multiplier, lifestyle_Total_HR)
    Weightage_processed_food = safe_weightage(processed_food_multiplier, lifestyle_Total_HR)
    Weightage_fruit_veg = safe_weightage(fruit_veg_multiplier, lifestyle_Total_HR)
    Weightage_whole_grain = safe_weightage(whole_grain_multiplier, lifestyle_Total_HR)
    Weightage_unhealthy_fats = safe_weightage(unhealthy_fats_multiplier, lifestyle_Total_HR)
    Weightage_limit_sugar = safe_weightage(limit_sugar_multiplier, lifestyle_Total_HR)
    Weightage_alcohol = safe_weightage(alcohol_multiplier, lifestyle_Total_HR)
    Weightage_smoking = safe_weightage(smoking_multiplier, lifestyle_Total_HR)
    Weightage_sleep = safe_weightage(sleep_multiplier, lifestyle_Total_HR)
    Weightage_stress = safe_weightage(stress_multiplier, lifestyle_Total_HR)
    
    def safe_exp_calculation(multiplier, reference):
        if multiplier is None:
            return 0
        return math.exp(-(((multiplier / reference) ** 2) - 1))
    
    step_Exponential_Function = safe_exp_calculation(step_multiplier, 0.48)
    mvpa_Exponential_Function = safe_exp_calculation(mvpa_multiplier, 0.55)
    sedentary_time_Exponential_Function = safe_exp_calculation(sedentary_time_multiplier, 0.37)
    processed_food_Exponential_Function = safe_exp_calculation(processed_food_multiplier, 1.0)
    fruit_veg_Exponential_Function = safe_exp_calculation(fruit_veg_multiplier, 0.64)
    whole_grain_Exponential_Function = safe_exp_calculation(whole_grain_multiplier, 0.79)
    unhealthy_fats_Exponential_Function = safe_exp_calculation(unhealthy_fats_multiplier, 0.98)
    limit_sugar_Exponential_Function = safe_exp_calculation(limit_sugar_multiplier, 0.96)
    alcohol_Exponential_Function = safe_exp_calculation(alcohol_multiplier, 0.91)
    smoking_Exponential_Function = safe_exp_calculation(smoking_multiplier, 1.0)
    sleep_Exponential_Function = safe_exp_calculation(sleep_multiplier, 1.0)
    stress_Exponential_Function = safe_exp_calculation(stress_multiplier, 0.18)
    
    step = Weightage_step * step_Exponential_Function
    mvpa = Weightage_mvpa * mvpa_Exponential_Function
    sedentary_time = Weightage_sedentary_time * sedentary_time_Exponential_Function
    processed_food = Weightage_processed_food * processed_food_Exponential_Function
    fruit_veg = Weightage_fruit_veg * fruit_veg_Exponential_Function
    whole_grain = Weightage_whole_grain * whole_grain_Exponential_Function
    unhealthy_fats = Weightage_unhealthy_fats * unhealthy_fats_Exponential_Function
    limit_sugar = Weightage_limit_sugar * limit_sugar_Exponential_Function
    alcohol = Weightage_alcohol * alcohol_Exponential_Function
    smoking = Weightage_smoking * smoking_Exponential_Function
    sleep = Weightage_sleep * sleep_Exponential_Function
    stress = Weightage_stress * stress_Exponential_Function
    
    lifestyle_score_sum = round(safe_add(step, mvpa, sedentary_time, processed_food, fruit_veg, whole_grain, unhealthy_fats, limit_sugar,
                                         alcohol, smoking, sleep, stress))

    return lifestyle_score_sum

    # return (step_multiplier, sedentary_time_multiplier, unhealthy_fats_multiplier, limit_sugar_multiplier, whole_grain_multiplier, stress_multiplier, processed_food_multiplier, fruit_veg_multiplier, mvpa_multiplier, sleep_multiplier, alcohol_multiplier, smoking_multiplier)
