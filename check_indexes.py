import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the indexes on a table
query = '''
SELECT i.name AS index_name, 
       i.type_desc AS index_type, 
       col.name AS column_name, 
       ic.index_column_id,
       i.is_unique, 
       i.is_primary_key
FROM sys.indexes AS i
INNER JOIN sys.index_columns AS ic 
    ON i.object_id = ic.object_id AND i.index_id = ic.index_id
INNER JOIN sys.columns AS col 
    ON ic.object_id = col.object_id AND ic.column_id = col.column_id
WHERE i.object_id = OBJECT_ID('table_name')
'''
cursor.execute(query)
results = cursor.fetchall()

# Print the indexes on the table
print('Indexes on table:')
for row in results:
    print(row[0], '-', row[1], '-', row[2])

# Close the cursor and connection
cursor.close()
conn.close()
