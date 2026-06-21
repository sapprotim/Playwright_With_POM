# # Extract values from both panels
# clinical_labels = page.locator("//div[@class='dashboard-body-wrap']//ul//li/div/span").all_text_contents()
# clinical_values = page.locator("//div[@class='dashboard-body-wrap']//ul//li/div/p").all_text_contents()
#
# results = {}
#
# for label, value in zip(clinical_labels, clinical_values):
#     label = label.strip()
#     value = value.strip()
#
#     cleaned = clean_value(label, value)
#
#     if isinstance(cleaned, dict):  # For blood pressure, store both values
#         results.update(cleaned)
#     else:
#         results[label] = cleaned
#
#
#
# print("Clinical_results", results)
#
# for key in ['HDL Cholesterol', 'Total Cholesterol']:
#     results.pop(key, None)  # Safely remove even if key doesn't exist





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

for key, value in life_results.items():
    if value == '--':
        life_results[key] = None

lifestyle_score = calculate_lifestyle_score(
    gender="male",
    step=safe_get_str(life_results, "Steps"),
    sedentary_time=safe_get_str(life_results, "Sedentary Time"),
    unhealthy_fats=safe_get_str(life_results, "Unhealthy Oil & Fat"),
    limit_sugar=safe_get_str(life_results, "Limit Sugar"),
    whole_grain=safe_get_str(life_results, "Wholegrains"),
    stress=safe_get_str(life_results, "Stress"),
    processed_food=safe_get_str(life_results, "Processed Food"),
    fruit_veg=safe_get_str(life_results, "Fruit & Vegetables"),
    mvpa=safe_get_str(life_results, "MVPA"),
    sleep=safe_get_str(life_results, "Sleep"),
    alcohol=safe_get_str(life_results, "Alcohol"),
    smoking=safe_get_str(life_results, "Smoking")
)
dashboard_lifestyle_Score = page.locator("//span[@class='highcharts-title']//div").text_content()
dashboard_lifestyle_Score = re.findall(r"\d+\.?\d*", dashboard_lifestyle_Score)
dashboard_lifestyle_Score = int(dashboard_lifestyle_Score[0])
print("Python code calculation Lifestyle score:", lifestyle_score)
print("Dashboard_lifestyle_Score:", dashboard_lifestyle_Score)
assert dashboard_lifestyle_Score == lifestyle_score, "Lifestyle score mismatch!"
print("✅ Lifestyle score matched!")