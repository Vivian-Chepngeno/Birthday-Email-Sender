import smtplib
import pandas as pd
import random
from datetime import datetime

my_email = "chepngenovivian55@gmail.com"
password = "wins bmzu pscn ppyl"

# Get today's date
today = datetime.now()
today_tuple = (today.month, today.day)

# Debug: Print today's date tuple
print(f"Today's date tuple: {today_tuple} (Month: {today.month}, Day: {today.day})")

# Read the CSV file containing birthdays
data = pd.read_csv("birthdays.csv")

# Debug: Print CSV content to ensure it's read correctly
print("CSV Data:")
print(data)

# Check for missing values in 'month' and 'day' columns
print("Checking for missing values:")
print(data.isnull().sum())

# Option 1: Drop rows with NaN values in 'month' or 'day'
data = data.dropna(subset=['month', 'day', 'name', 'email'])

# Convert month and day to integers
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Create a dictionary to map (month, day) to the person's info
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

# Debug: Print the birthdays dictionary
print("Birthdays Dictionary:")
for key, value in birthdays_dict.items():
    print(f"Key: {key}, Value: {value['name']} (Month: {value['month']}, Day: {value['day']})")

# Check if today is someone's birthday
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]

    # Debug: Print the birthday person's details
    print(f"Birthday person found: {birthday_person['name']}")

    # Pick a random letter template
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    
    with open(file_path) as letter_file:
        contents = letter_file.read()
        # Replace [NAME] with the actual name of the birthday person
        contents = contents.replace("[NAME]", birthday_person["name"])

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()  # Secure the connection
        connection.login(user=my_email, password=password)  # Log in
        
        # Send the email with the birthday message
        connection.sendmail(
            from_addr=my_email,
            to_addrs=birthday_person["email"],
            msg=f"Subject: Happy Birthday!\n\n{contents}"  # f-string to insert the letter contents
        )


    print(f"Birthday email sent successfully to {birthday_person['name']}!")
else:
    print("No birthdays today.")
   

