import pandas as pd
import sqlite3

# Read the Excel file into a pandas DataFrame
df = pd.read_excel('attendance.xlsx')

# Establish a connection to the database
conn = sqlite3.connect('database.db')

# Write the DataFrame to a database table
df.to_sql('your_table_name', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()
