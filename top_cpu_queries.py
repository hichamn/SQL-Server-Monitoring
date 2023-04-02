import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the top queries by CPU usage
query = '''
SELECT TOP 10
  total_worker_time/execution_count AS avg_cpu_time,
  execution_count,
  st.text
FROM sys.dm_exec_query_stats AS qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS st
WHERE qs.total_worker_time > 100000 -- change 100000 to the desired threshold
ORDER BY avg_cpu_time DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the top queries by CPU usage
print('Top queries by CPU usage:')
for row in results:
    print('Avg. CPU time:', row[0], 'ms, Execution count:', row[1], 'Query text:', row[2])

# Close the cursor and connection
cursor.close()
conn.close()
