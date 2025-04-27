import sqlite3
"""
import accounts
import addresses
import phones
import employees
import products
import categories
import orders
import order_details
import movements
"""

#Conexión a la base de datos SQLite
def connect():
    conn = sqlite3.connect('database/database.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

#Desconexión de la base de datos SQLite
def disconnect(conn):
    if conn is not None:
        conn.close()
        conn = None

# Función para obtener todas las tablas de la base de datos
def get_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    disconnect(conn)
    return [table[0] for table in tables]

# Función para obtener la estructura de la tabla en la base de datos
def get_table_structure(table_name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    disconnect(conn)
    return columns

# Función para imprimir la estructura de la tabla en la base de datos
def print_table_structure(table_name):
    columns = get_table_structure(table_name)
    print(f"Estructura de la tabla {table_name}:")
    for column in columns:
        print(f"Nombre: {column[1]}, Tipo: {column[2]}, Nulo: {column[3]}, Predeterminado: {column[4]}")
