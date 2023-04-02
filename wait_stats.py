import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the wait stats
query = '''
SELECT wait_type, wait_time_ms, wait_time_ms / CAST(SUM(wait_time_ms) OVER() AS FLOAT) AS pct
FROM sys.dm_os_wait_stats
WHERE wait_type NOT LIKE '%SLEEP%'
ORDER BY wait_time_ms DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the wait stats
print('Wait stats:')
for row in results:
    print('Wait type:', row[0], 'Wait time (ms):', row[1], 'Percentage:', row[2])

# Close the cursor and connection
cursor.close()
conn.close()
