import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the fragmentation level of indexes
query = '''
SELECT t.name AS table_name, i.name AS index_name, ips.avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, NULL) AS ips
INNER JOIN sys.tables AS t ON ips.object_id = t.object_id
INNER JOIN sys.indexes AS i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 30 -- change 30 to the desired threshold
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the indexes with high fragmentation levels
print('Indexes with high fragmentation levels:')
for row in results:
    print('Table name:', row[0], 'Index name:', row[1], 'Fragmentation level:', row[2])

# Close the cursor and connection
cursor.close()
conn.close()
