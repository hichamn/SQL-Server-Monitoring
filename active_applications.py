import pyodbc

# Connect to SQL Server instance
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the active applications and their connection counts
query = '''
SELECT program_name, COUNT(*) AS connection_count
FROM sys.dm_exec_sessions
WHERE is_user_process = 1
GROUP BY program_name
ORDER BY connection_count DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Close the cursor and connection
cursor.close()
conn.close()

# Print the active applications and their connection counts
print('Active applications:')
for row in results:
    print(row[0], row[1])
