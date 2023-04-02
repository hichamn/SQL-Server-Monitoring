import pyodbc

def get_dependencies(conn, object_name, object_type):
    """
    Get the dependencies of a specified SQL Server object.

    Args:
        conn (pyodbc.Connection): The connection object to the SQL Server database.
        object_name (str): The name of the SQL Server object.
        object_type (str): The type of the SQL Server object.

    Returns:
        A list of tuples containing the names and types of the dependent objects.
    """
    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query to get the dependencies of the object
    query = f"""
    SELECT referenced_entity_name, referenced_minor_name, referenced_entity_type_desc
    FROM sys.sql_expression_dependencies
    WHERE referencing_id = OBJECT_ID('{object_name}', '{object_type}')
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Return the list of dependent objects
    return [(row[0], row[1], row[2]) for row in results]

# Connect to SQL Server database
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;Trusted_Connection=yes;')

# Get the table name as input
table_name = input('Enter the name of the table: ')

# Get the dependencies of the specified table
object_type = 'USER_TABLE'
dependencies = get_dependencies(conn, table_name, object_type)

# Print the dependencies of the table
print(f'Dependencies of {object_type} {table_name}:')
for row in dependencies:
    print(row[2], row[0], row[1])

# Close the connection
conn.close()
