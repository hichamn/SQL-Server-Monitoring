import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the I/O usage of the database
query = '''
SELECT DB_NAME(database_id) AS database_name,
   io_stall_read_ms / (1.0 + num_of_reads) AS avg_read_stall_ms,
   io_stall_write_ms / (1.0 + num_of_writes) AS avg_write_stall_ms,
   (io_stall_read_ms + io_stall_write_ms) / (1.0 + num_of_reads + num_of_writes) AS avg_io_stall_ms
FROM sys.dm_io_virtual_file_stats(NULL, NULL) AS vfs
INNER JOIN sys.dm_io_pending_io_requests AS p
    ON p.io_handle = vfs.file_handle
WHERE database_id = DB_ID()
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the I/O usage of the database
print('I/O usage of the database:')
for row in results:
    print('Database name:', row[0], 'Avg. read stall time (ms):', row[1], 'Avg. write stall time (ms):', row[2], 'Avg. I/O stall time (ms):', row[3])

# Close the cursor and connection
cursor.close()
conn.close()
