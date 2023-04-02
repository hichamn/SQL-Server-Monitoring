import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the disk usage of tables
query = '''
SELECT t.name AS table_name, SUM(a.total_pages) * 8 AS total_size_kb
FROM sys.tables AS t
INNER JOIN sys.indexes AS i ON t.object_id = i.object_id
INNER JOIN sys.partitions AS p ON i.object_id = p.object_id AND i.index_id = p.index_id
INNER JOIN sys.allocation_units AS a ON p.partition_id = a.container_id
GROUP BY t.name
ORDER BY total_size_kb DESC
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the tables and their disk usage
print('Tables and their disk usage:')
for row in results:
    print('Table name:', row[0], 'Total size (KB):', row[1])

# Close the cursor and connection
cursor.close()
conn.close()
