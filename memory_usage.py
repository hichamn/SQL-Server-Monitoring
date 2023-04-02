import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the memory usage of SQL Server
query = '''
SELECT (physical_memory_in_use_kb / 1024) AS memory_usage_mb
FROM sys.dm_os_process_memory
'''
cursor.execute(query)
results = cursor.fetchone()

# Print the memory usage of SQL Server
print('Memory usage of SQL Server (MB):', results[0])

# Close the cursor and connection
cursor.close()
conn.close()
