import random
import pandas as pd
from datetime import datetime, timedelta
import os.path

# Generate random attendance data for the month of May
attendance_status = [0, 1]

start_date = datetime(2023, 5, 1)
end_date = datetime(2023, 5, 31)
dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

data = {
    'student_id': ['CS10'] * len(dates),
    'date': [date.strftime('%Y-%m-%d') for date in dates],
    'attendance_status': random.choices(attendance_status, k=len(dates))
}
df = pd.DataFrame(data)

# Check if the Excel file already exists
excel_file = 'attendance_data.xlsx'
if os.path.isfile(excel_file):
    # Read the existing data from the Excel file
    existing_df = pd.read_excel(excel_file, engine='openpyxl')
    
    # Append the new data to the existing data
    updated_df = pd.concat([existing_df, df], ignore_index=True)
else:
    # Create a new DataFrame with the data
    updated_df = df

# Save the updated DataFrame to the Excel file
updated_df.to_excel(excel_file, index=False)
