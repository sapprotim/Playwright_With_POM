import math

gender = input("Enter gender (Female/Male): ").strip().lower()

def evaluate_step(value):
    if 0 <= value <= 1500:
        return 2.74, "Needs Improvement"
    elif 1501 <= value <= 3000:
        return 1.96, "Needs Improvement"
    elif 3001 <= value <= 5000:
        return 1.27, "Needs Improvement"
    elif 5001 <= value <= 5800:
        return 1.00, "Good"
    elif 5801 <= value <= 8500:
        return 0.60, "Good"
    elif value >= 8501:
        return 0.48, "Good"
    else:
        return 0
# Example usage
score = input("Enter step: ")
if score == "Null" or score == "null" or score == "":
    step_multiplier = 0
    step_status = "Needs Improvement"
else:
    score = math.floor(float(score))
    step_multiplier, step_status = evaluate_step(score)
    print(f"Multiplier: {step_multiplier}, Status: {step_status}")


def evaluate_sedentary_time(minutes):
    if 0 <= minutes <= 560:
        return 0.37, "Good"
    elif 561 <= minutes <= 600:
        return 0.44, "Needs Improvement"
    elif 601 <= minutes <= 640:
        return 0.53, "Needs Improvement"
    elif 641 <= minutes <= 680:
        return 0.66, "Needs Improvement"
    elif 681 <= minutes <= 720:
        return 0.81, "Needs Improvement"
    elif 721 <= minutes <= 760:
        return 0.99, "Needs Improvement"
    elif 761 <= minutes <= 800:
        return 1.22, "Needs Improvement"
    elif 801 <= minutes <= 840:
        return 1.50, "Needs Improvement"
    elif 841 <= minutes <= 880:
        return 1.88, "Needs Improvement"
    elif minutes >= 881:
        return 2.23, "Needs Improvement"
    else:
        return 0

# Example usage
time = input("Enter sedentary time in minutes: ")
if time == "Null" or time == "null" or time == "":
    sedentary_time_multiplier = 0
    sedentary_time_status = "Needs Improvement"
else:
    time = math.floor(float(time))
    sedentary_time_multiplier, sedentary_time_status = evaluate_sedentary_time(time)
    print(f"Multiplier: {sedentary_time_multiplier}, Status: {sedentary_time_status}")


def evaluate_unhealthy_fats(frequency):
    frequency = frequency.strip().lower()

    if frequency in ["seldom", "never", "seldom / never"]:
        return 0.98, "Good"
    elif frequency == "sometimes":
        return 1.04, "Needs Improvement"
    elif frequency == "often":
        return 1.08, "Needs Improvement"
    else:
        return 0

# Example usage
freq = input("Enter frequency for unhealthy_fats : (Seldom / Never, Sometimes, Often): ")
unhealthy_fats_multiplier, unhealthy_fats_status = evaluate_unhealthy_fats(freq)
print(f"Multiplier: {unhealthy_fats_multiplier}, Status: {unhealthy_fats_status}")


def evaluate_limit_sugar(frequency):
    frequency = frequency.strip().lower()

    if frequency == "often":
        return 0.96, "Good"
    elif frequency == "sometimes":
        return 0.99, "Needs Improvement"
    elif frequency in ["seldom", "never", "seldom / never"]:
        return 1.15, "Needs Improvement"
    else:
        return 0
# Example usage
freq = input("Enter sugar intake frequency (Often, Sometimes, Seldom / Never): ")
limit_sugar_multiplier, limit_sugar_status = evaluate_limit_sugar(freq)
print(f"Multiplier: {limit_sugar_multiplier}, Status: {limit_sugar_status}")


def evaluate_whole_grain_intake(frequency):
    frequency = frequency.strip().lower()

    if frequency in ["seldom", "never", "seldom / never"]:
        return 0.88, "Needs Improvement"
    elif frequency == "sometimes":
        return 0.80, ""
    elif frequency == "often":
        return 0.79, "Good"
    else:
        return 0

# Example usage
freq = input("Enter whole grain intake frequency (Seldom / Never, Sometimes, Often): ")
whole_grain_multiplier, whole_grain_status = evaluate_whole_grain_intake(freq)
print(f"Multiplier: {whole_grain_multiplier}, Status: {whole_grain_status}")





def evaluate_stress_level(frequency):
    frequency = frequency.strip().lower()
    if frequency in ["seldom", "never", "seldom/never", "seldom / never"]:
        return 0.18, "Good"
    elif frequency == "sometimes":
        return 0.59, "Needs Improvement"
    elif frequency == "often":
        return 1.00, ""
    else:
        return 0

# Example usage
freq = input("Enter stress frequency (Seldom/Never, Sometimes, Often): ")
stress_multiplier, stress_status = evaluate_stress_level(freq)
print(f"Multiplier: {stress_multiplier}, Status: {stress_status}")


def evaluate_processed_food_male(answer):
    answer = answer.strip().lower()
    if answer == "no":
        return 1.00, "Good"
    elif answer == "yes":
        return 1.27, "Needs Improvement"
    else:
        return 0

def evaluate_processed_food_female(answer):
    answer = answer.strip().lower()
    if answer == "no":
        return 1.00, "Good"
    elif answer == "yes":
        return 1.30, "Needs Improvement"
    else:
        return 0

# Example usage
answer = input("Processed Food Intake? (Yes/No): ")
if gender == "male":
    processed_food_multiplier, processed_food_status = evaluate_processed_food_male(answer)
elif gender == "female":
    processed_food_multiplier, processed_food_status = evaluate_processed_food_female(answer)
else:
    processed_food_multiplier, processed_food_status = None, "Invalid gender input"

print(f"Processed Food Multiplier: {processed_food_multiplier}, Status: {processed_food_status}")


def evaluate_fruit_veg_intake(servings):
    if 0 <= servings <= 3:
        return 1.0, "Needs Improvement"
    elif 4 <= servings <= 20:
        return 0.64, "Good"
    else:
        return 0

# Example
servings = float(input("Fruit & Vegetable servings: "))
fruit_veg_multiplier, fruit_veg_status = evaluate_fruit_veg_intake(servings)
print(f"Multiplier: {fruit_veg_multiplier}, Status: {fruit_veg_status}")

def evaluate_mvpa(mins):
    if mins == 0:
        return 1.0, "Needs Improvement"
    elif 1 <= mins <= 19:
        return 0.91, ""
    elif 20 <= mins <= 59:
        return 0.83, ""
    elif 60 <= mins <= 149:
        return 0.76, ""
    elif 150 <= mins <= 179:
        return 0.70, "Good"
    elif 180 <= mins <= 219:
        return 0.64, ""
    elif 220 <= mins <= 259:
        return 0.59, ""
    elif mins >= 260:
        return 0.55, ""
    else:
        return 0

mins = input("MVPA minutes: ")
if mins == "Null" or mins == "null" or mins == "":
    mvpa_multiplier = 0
    mvpa_status = "Needs Improvement"
else:
    mins = math.floor(float(time))
    mvpa_multiplier, mvpa_status = evaluate_mvpa(mins)
    print(f"Multiplier: {mvpa_multiplier}, Status: {mvpa_status}")


def evaluate_sleep(hours):
    if hours < 7:
        return 1.45, "Needs Improvement"
    elif hours >= 7:
        return 1.0, "Good"
    else:
        return 0

hours = input("Sleep hours: ")
if hours == "Null" or hours == "null" or hours == "":
    sleep_multiplier = 0
    sleep_status = "Needs Improvement"
else:
    hours = math.floor(float(hours))
    sleep_multiplier, sleep_status = evaluate_sleep(hours)
    print(f"Multiplier: {sleep_multiplier}, Status: {sleep_status}")


def evaluate_alcohol(answer):
    answer = answer.strip().lower()
    if answer == "no":
        return 0.91, "Good"
    elif answer == "yes":
        return 1.33, "Needs Improvement"
    else:
        return 0

answer = input("Alcohol consumption (Yes/No): ")
alcohol_multiplier, alcohol_status = evaluate_alcohol(answer)
print(f"Multiplier: {alcohol_multiplier}, Status: {alcohol_status}")



def evaluate_smoking(answer):
    answer = answer.strip().lower()
    if answer == "no":
        return answer, 1.0, "Good"
    elif answer == "yes":
        return answer, 1.46, "Needs Improvement"
    else:
        return answer, None, "Invalid input"

# Example usage
smoking_answer = input("Smoking (Yes/No): ")
smoking_total, smoking_multiplier, smoking_status = evaluate_smoking(smoking_answer)
print(f"Smoking: {smoking_total}, Multiplier: {smoking_multiplier}, Status: {smoking_status}")



#Lifestyle Parameters:

def safe_add(*args):
    return sum([val for val in args if isinstance(val, (int, float))])

lifestyle_Total_HR = safe_add(step_multiplier, mvpa_multiplier, sedentary_time_multiplier, processed_food_multiplier, fruit_veg_multiplier,
                              whole_grain_multiplier, unhealthy_fats_multiplier, limit_sugar_multiplier, alcohol_multiplier, smoking_multiplier,
                              sleep_multiplier, stress_multiplier)


print("lifestyle_Total_HR", lifestyle_Total_HR )

def safe_weightage(multiplier, total_hr):
    if multiplier is None or total_hr in (None, 0):
        return 0
    return (multiplier / total_hr) * 100

Weightage_step = safe_weightage(step_multiplier, lifestyle_Total_HR)
print(Weightage_step)
Weightage_mvpa = safe_weightage(mvpa_multiplier, lifestyle_Total_HR)
print(Weightage_mvpa)
Weightage_sedentary_time = safe_weightage(sedentary_time_multiplier, lifestyle_Total_HR)
print(Weightage_sedentary_time)
Weightage_processed_food = safe_weightage(processed_food_multiplier, lifestyle_Total_HR)
print(Weightage_processed_food)
Weightage_fruit_veg = safe_weightage(fruit_veg_multiplier, lifestyle_Total_HR)
print(Weightage_fruit_veg)
Weightage_whole_grain = safe_weightage(whole_grain_multiplier, lifestyle_Total_HR)
print(Weightage_whole_grain)
Weightage_unhealthy_fats = safe_weightage(unhealthy_fats_multiplier, lifestyle_Total_HR)
print(Weightage_unhealthy_fats)
Weightage_limit_sugar = safe_weightage(limit_sugar_multiplier, lifestyle_Total_HR)
print(Weightage_limit_sugar)
Weightage_alcohol = safe_weightage(alcohol_multiplier, lifestyle_Total_HR)
print(Weightage_alcohol)
Weightage_smoking = safe_weightage(smoking_multiplier, lifestyle_Total_HR)
print(Weightage_smoking)
Weightage_sleep = safe_weightage(sleep_multiplier, lifestyle_Total_HR)
print(Weightage_sleep)
Weightage_stress = safe_weightage(stress_multiplier, lifestyle_Total_HR)
print(Weightage_stress)

print("safe_exp_calculation")
def safe_exp_calculation(multiplier, reference):
    if multiplier is None:
        return 0  # or 1 if you want neutral effect
    return math.exp(-(((multiplier / reference) ** 2) - 1))

step_Exponential_Function = safe_exp_calculation(step_multiplier, 0.48)
print(step_Exponential_Function)
mvpa_Exponential_Function = safe_exp_calculation(mvpa_multiplier, 0.55)
print(mvpa_Exponential_Function)
sedentary_time_Exponential_Function = safe_exp_calculation(sedentary_time_multiplier, 0.37)
print(sedentary_time_Exponential_Function)
processed_food_Exponential_Function = safe_exp_calculation(processed_food_multiplier, 1.0)
print(processed_food_Exponential_Function)
fruit_veg_Exponential_Function = safe_exp_calculation(fruit_veg_multiplier, 0.64)
print(fruit_veg_Exponential_Function)
whole_grain_Exponential_Function = safe_exp_calculation(whole_grain_multiplier, 0.79)
print(whole_grain_Exponential_Function)
unhealthy_fats_Exponential_Function = safe_exp_calculation(unhealthy_fats_multiplier, 0.98)
print(unhealthy_fats_Exponential_Function)
limit_sugar_Exponential_Function = safe_exp_calculation(limit_sugar_multiplier, 0.96)
print(limit_sugar_Exponential_Function)
alcohol_Exponential_Function = safe_exp_calculation(alcohol_multiplier, 0.91)
print(alcohol_Exponential_Function)
smoking_Exponential_Function = safe_exp_calculation(smoking_multiplier, 1.0)
print(smoking_Exponential_Function)
sleep_Exponential_Function = safe_exp_calculation(sleep_multiplier, 1.0)
sleep_Exponential_Function
stress_Exponential_Function = safe_exp_calculation(stress_multiplier, 0.18)
print(stress_Exponential_Function)

# Final lifestyle adjusted values
step = Weightage_step * step_Exponential_Function
print(step)
mvpa = Weightage_mvpa * mvpa_Exponential_Function
print(mvpa)
sedentary_time = Weightage_sedentary_time * sedentary_time_Exponential_Function
print(sedentary_time)
processed_food = Weightage_processed_food * processed_food_Exponential_Function
print(processed_food)
fruit_veg = Weightage_fruit_veg * fruit_veg_Exponential_Function
print(fruit_veg)
whole_grain = Weightage_whole_grain * whole_grain_Exponential_Function
print(whole_grain)
unhealthy_fats = Weightage_unhealthy_fats * unhealthy_fats_Exponential_Function
print(unhealthy_fats_multiplier)
limit_sugar = Weightage_limit_sugar * limit_sugar_Exponential_Function
print(limit_sugar)
alcohol = Weightage_alcohol * alcohol_Exponential_Function
print(alcohol)
smoking = Weightage_smoking * smoking_Exponential_Function
print(smoking)
sleep = Weightage_sleep * sleep_Exponential_Function
print(sleep)
stress = Weightage_stress * stress_Exponential_Function
print(stress)

# Sum all lifestyle adjusted scores
lifestyle_score_sum = round(safe_add(step, mvpa, sedentary_time, processed_food, fruit_veg, whole_grain, unhealthy_fats, limit_sugar,
                               alcohol, smoking, sleep, stress))

print(f"Total Lifestyle Score: {lifestyle_score_sum}")