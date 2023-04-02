import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the SQL Server configuration options
query = '''
EXEC sp_configure
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the SQL Server configuration options
print('SQL Server configuration options:')
for row in results:
    print(row[0], '=', row[1])

# Close the cursor and connection
cursor.close()
conn.close()
