import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to find missing indexes
query = '''
SELECT
    DB_NAME(database_id) AS DatabaseName,
    OBJECT_NAME(object_id) AS TableName,
    'CREATE NONCLUSTERED INDEX IX_' + OBJECT_NAME(object_id) + '_' + REPLACE(REPLACE(REPLACE(ISNULL(equality_columns, ''), ', ', '_'), '[', ''), ']', '') + COALESCE('_' + REPLACE(REPLACE(REPLACE(ISNULL(included_columns, ''), ', ', '_'), '[', ''), ']', ''), '') +
        ' ON ' + OBJECT_SCHEMA_NAME(object_id) + '.' + OBJECT_NAME(object_id) + ' (' + ISNULL(equality_columns, '') +
        CASE WHEN equality_columns IS NOT NULL AND inequality_columns IS NOT NULL THEN ', ' ELSE '' END + ISNULL(inequality_columns, '') +
        ') ' + COALESCE('INCLUDE (' + included_columns + ')', '') AS CreateIndexStatement,
    user_seeks + user_scans + user_lookups AS Reads,
    user_updates AS Writes,
    last_user_seek AS LastRead,
    last_user_scan AS LastScan,
    last_user_lookup AS LastLookup,
    last_user_update AS LastWrite,
    system_seeks + system_scans + system_lookups AS SystemReads,
    system_updates AS SystemWrites,
    last_system_seek AS LastSystemRead,
    last_system_scan AS LastSystemScan,
    last_system_lookup AS LastSystemLookup,
    last_system_update AS LastSystemWrite,
    s.*
FROM sys.dm_db_missing_index_details AS s
WHERE database_id = DB_ID()
ORDER BY (user_seeks + user_scans + user_lookups) DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the missing indexes
print('Missing indexes:')
for row in results:
    print('Database name:', row[0], 'Table name:', row[1], 'Create index statement:', row[2], 'Reads:', row[3], 'Writes:', row[4], 'Last read:', row[5], 'Last scan:', row[6], 'Last lookup:', row[7], 'Last write:', row[8], 'System reads:', row[9], 'System writes:', row[10], 'Last system read:', row[11], 'Last system scan:', row[12], 'Last system lookup:', row[13], 'Last system write:', row[14])

# Close the cursor and connection
cursor.close()
conn.close()
