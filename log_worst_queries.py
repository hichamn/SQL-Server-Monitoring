import pyodbc
import logging

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the worst performing queries
query = '''
SELECT TOP 10 query_text, execution_count, total_worker_time, last_execution_time 
FROM sys.dm_exec_query_stats AS qs 
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS st
ORDER BY total_worker_time DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Write the results to a log file
logging.basicConfig(filename='worst_queries.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Worst performing queries:')
for row in results:
    logging.debug('Query: %s, Execution count: %s, Total worker time: %s, Last execution time: %s', row[0], row[1], row[2], row[3])

# Close the cursor and connection
cursor.close()
conn.close()
