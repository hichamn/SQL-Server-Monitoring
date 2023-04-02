import pyodbc

def get_column_tables(conn, column_name):
    """
    Get all the tables in a specified SQL Server database that use a specified column.

    Args:
        conn (pyodbc.Connection): The connection object to the SQL Server database.
        column_name (str): The name of the column.

    Returns:
        A list of tuples containing the names of the tables that use the column.
    """
    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query to get all the tables that use the column
    query = f"""
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE COLUMN_NAME = '{column_name}'
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Return the list of tables that use the column
    return results

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Get the column name as input
column_name = input('Enter the name of the column: ')

# Get all the tables that use the specified column
tables = get_column_tables(conn, column_name)

# Print the tables that use the column
print(f'Tables that use column {column_name}:')
for row in tables:
    print(row[0])

# Close the connection
conn.close()
