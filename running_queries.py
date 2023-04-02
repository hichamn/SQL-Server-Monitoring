import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the currently running queries
query = '''
SELECT r.session_id,
       r.status,
       r.command,
       t.text,
       r.cpu_time,
       r.total_elapsed_time
FROM sys.dm_exec_requests AS r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) AS t
WHERE r.status = 'running'
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the currently running queries
print('Currently running queries:')
for row in results:
    print('Session ID:', row[0], 'Status:', row[1], 'Command:', row[2], 'Query text:', row[3], 'CPU time:', row[4], 'Total elapsed time:', row[5])

# Close the cursor and connection
cursor.close()
conn.close()
