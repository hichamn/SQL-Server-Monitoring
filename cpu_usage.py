import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the CPU usage of SQL Server
query = '''
SELECT TOP 1
  cpu_usage_percent
FROM sys.dm_os_performance_counters
WHERE counter_name LIKE '%processor time%' AND object_name LIKE '%sql server%'
ORDER BY cntr_value DESC
'''
cursor.execute(query)
results = cursor.fetchone()

# Print the CPU usage of SQL Server
print('CPU usage of SQL Server (%):', results[0])

# Close the cursor and connection
cursor.close()
conn.close()
