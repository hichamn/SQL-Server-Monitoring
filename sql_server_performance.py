import pyodbc

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the average response time of a query
query = 'SELECT AVG(DATEDIFF(ms, StartTime, EndTime)) AS ResponseTime FROM dbo.QueryLog'
cursor.execute(query)
result = cursor.fetchone()

# Print the average response time
print('Average response time:', result[0], 'ms')

# Execute a query to get the top 10 slowest queries
query = 'SELECT TOP 10 QueryText, DATEDIFF(ms, StartTime, EndTime) AS ResponseTime FROM dbo.QueryLog ORDER BY ResponseTime DESC'
cursor.execute(query)
results = cursor.fetchall()

# Print the top 10 slowest queries
print('Top 10 slowest queries:')
for row in results:
    print(row[0], '-', row[1], 'ms')

# Close the cursor and connection
cursor.close()
conn.close()
