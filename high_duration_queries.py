import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the queries with high duration
query = '''
SELECT TOP 10
  qs.total_elapsed_time/qs.execution_count AS avg_duration,
  qs.execution_count,
  st.text
FROM sys.dm_exec_query_stats AS qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS st
WHERE qs.total_elapsed_time/qs.execution_count > 10000 -- change 10000 to the desired threshold
ORDER BY avg_duration DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the queries with high duration
print('Queries with high duration:')
for row in results:
    print('Avg. duration:', row[0], 'ms, Execution count:', row[1], 'Query text:', row[2])

# Close the cursor and connection
cursor.close()
conn.close()
