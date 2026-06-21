# Login Info
import pandas as pd
df = pd.read_excel("data.xlsx", sheet_name="Login", header=None)
Org_Admin_email = df.iloc[1, 1]
Org_Admin_password = df.iloc[1, 2]
Org_Admin_otp = df.iloc[1, 3]

FA_Admin_email = df.iloc[2, 1]
FA_Admin_password = df.iloc[2, 2]
FA_Admin_otp = df.iloc[2, 3]

Clinic_Admin_email = df.iloc[3, 1]
Clinic_Admin_password = df.iloc[3, 2]
Clinic_Admin_otp = df.iloc[3, 3]

Doctor_Admin_email = df.iloc[4, 1]
Doctor_Admin_password = df.iloc[4, 2]
Doctor_Admin_otp = df.iloc[4, 3]

search = pd.read_excel("data.xlsx", sheet_name="Search", header=None)
doctor_name = search.iloc[1, 1]
user_name = search.iloc[2, 1]
search_user = search.iloc[3, 1]
clinic_admin = search.iloc[4,1]
fh_admin = search.iloc[5,1]
search_item = search.iloc[6,1]
withdrawn_user = search.iloc[7,1]
clinic = search.iloc[8,1]
fullerton_health = search.iloc[9,1]



link = pd.read_excel("data.xlsx", sheet_name="Link", header=None)
dashboard_link = link.iloc[1, 0]






