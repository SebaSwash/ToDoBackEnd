# Utility functions

# Función para convertir los resultados del cursor a diccionarios dentro de una lista
def cursor_to_dict(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
