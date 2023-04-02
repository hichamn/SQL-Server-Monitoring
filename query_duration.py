import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the average duration of SQL queries
query = '''
SELECT TOP 10
    total_elapsed_time / execution_count AS avg_duration_ms,
    execution_count,
    st.text
FROM sys.dm_exec_query_stats AS qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS st
ORDER BY avg_duration_ms DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the average duration of SQL queries
print('Average duration of SQL queries:')
for row in results:
    print('Avg. duration:', row[0], 'ms, Execution count:', row[1], 'Query text:', row[2])

# Close the cursor and connection
cursor.close()
conn.close()
