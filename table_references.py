import pyodbc

def get_table_references(conn, table_name):
    """
    Get all the stored procedures in a SQL Server database that reference a specified table.

    Args:
        conn (pyodbc.Connection): The connection object to the SQL Server database.
        table_name (str): The name of the SQL Server table.

    Returns:
        A list of tuples containing the names of the stored procedures that reference the table.
    """
    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query to get all the stored procedures that reference the table
    query = f"""
    SELECT OBJECT_NAME(referencing_id), referenced_entity_name
    FROM sys.sql_expression_dependencies
    WHERE referenced_id = OBJECT_ID('{table_name}')
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Return the list of stored procedures that reference the table
    return results

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Get the table name as input
table_name = input('Enter the name of the table: ')

# Get all the stored procedures that reference the specified table
stored_procedures = get_table_references(conn, table_name)

# Print the stored procedures that reference the table
print(f'Stored procedures that reference table {table_name}:')
for row in stored_procedures:
    print(row[0])

# Close the connection
conn.close()
