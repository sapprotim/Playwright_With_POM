import csv

CSV_PATH = r"D:\Playwright_HPB-POM\user data.csv"

data_list = []

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)  # Automatically uses first row as keys
    for row in reader:
        data_list.append(row)

# Example: print all data
for item in data_list:
    print(item)

# Example: access 2nd row, 1st column (assuming column name is from first row)
if data_list:
    first_column_name = list(data_list[0].keys())[0]  # first column header
    print("2nd row, 1st column:", data_list[0][first_column_name])






