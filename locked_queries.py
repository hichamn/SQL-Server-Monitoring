import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the locked queries and their locking processes
query = '''
SELECT 
    L.request_session_id AS [Request Session ID], 
    DB_NAME(L.resource_database_id) AS [Database Name], 
    O.Name AS [Locked Object Name], 
    P.spid AS [Process ID], 
    P.program_name AS [Process Name], 
    L.blocking_session_id AS [Blocking Session ID], 
    L.resource_type AS [Locked Resource Type], 
    L.request_mode AS [Lock Type Requested], 
    L.request_type AS [Lock Request Type], 
    L.request_status AS [Lock Request Status], 
    L.request_mode AS [Lock Request Mode], 
    L.resource_description AS [Locked Resource Description]
FROM sys.dm_tran_locks L
INNER JOIN sys.partitions P ON P.hobt_id = L.resource_associated_entity_id
INNER JOIN sys.objects O ON O.object_id = P.object_id
WHERE L.request_status = 'WAIT'
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the locked queries and their locking processes
print('Locked queries:')
for row in results:
    print('Request session ID:', row[0], 'Database name:', row[1], 'Locked object name:', row[2], 'Process ID:', row[3], 'Process name:', row[4], 'Blocking session ID:', row[5], 'Locked resource type:', row[6], 'Lock type requested:', row[7], 'Lock request type:', row[8], 'Lock request status:', row[9], 'Lock request mode:', row[10], 'Locked resource description:', row[11])

# Close the cursor and connection
cursor.close()
conn.close()
