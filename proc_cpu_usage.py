import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the most expensive stored procedures by CPU usage
query = '''
SELECT TOP 10
  p.name AS proc_name,
  qs.total_worker_time/qs.execution_count AS avg_cpu_time,
  qs.execution_count,
  st.text
FROM sys.dm_exec_query_stats AS qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS st
INNER JOIN sys.procedures AS p ON st.objectid = p.object_id
WHERE qs.total_worker_time > 100000 -- change 100000 to the desired threshold
ORDER BY avg_cpu_time DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the most expensive stored procedures by CPU usage
print('Most expensive stored procedures by CPU usage:')
for row in results:
    print('Proc name:', row[0], 'Avg. CPU time:', row[1], 'ms, Execution count:', row[2], 'Proc text:', row[3])

# Close the cursor and connection
cursor.close()
conn.close()
