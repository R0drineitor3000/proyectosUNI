import sqlite3

conn = None

def connect():
    global conn
    if conn is None:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
    
def disconnect():
    global conn
    if conn is not None:
        conn.close()
        conn = None

def addEmployee(given_name, last_name, idcard, birthdate=None, hiredate=None, position=None, salary=None):
    connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employees (given_name, last_name, birthdate, hiredate, idcard, position, salary)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (given_name, last_name, birthdate, hiredate, idcard, position, salary))
    conn.commit()

def deleteEmployee(ID):
    connect()
    if employeeExists(ID):
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM employees
            WHERE idcard = ?''',
            (ID,))
        conn.commit()
        return True
    return False

def updateEmployee(ID, field, data):
    valid_fields = ['id', 'given_name', 'last_name', 'birthdate',
                    'hiredate', 'idcard', 'position', 'salary']
    if field not in valid_fields:
        return False
    
    connect()

    if employeeExists(ID):
        try:
            cursor = conn.cursor()
            # Construcción dinámica de la consulta
            query = f"UPDATE employees SET {field} = ? WHERE idcard = ?"
            cursor.execute(query, (data, ID))
            conn.commit()  # Asegúrate de hacer commit después de la ejecución
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Error al actualizar el empleado: {e}")
            return False
    else:
        return False

def employeeExists(ID):
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM employees WHERE idcard = ?
    ''', (ID,))
    return cursor.fetchone() is not None

def getEmployees():
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM employees
    ''')
    data = cursor.fetchall()
    return data

def getAllEmployees():
    users = []
    for i in getEmployees():
        users.append(dict(i))
    return users

def getEmployee(ID):
    connect()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM employees WHERE id = ?''', (ID,))
    data = cursor.fetchone()
    if data is not None:
        return dict(data)
    return None

###############################################
###############################################
############# DEBUG FUNCTIONS #################
########### DELETE WHEN RELEASING #############
###############################################
###############################################
def clearEmployees():
    connect()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM employees''')  # Eliminar los registros
    cursor.execute('''DELETE FROM sqlite_sequence WHERE name='employees' ''')  # Reiniciar contador de autoincremento
    conn.commit()  # Cometer la transacción
    cursor.execute('''VACUUM''')  # Ejecutar VACUUM fuera de la transacción
    conn.commit()  # Cometer la transacción de VACUUM

def createTable():
    connect()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        given_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birthdate TEXT,
        hiredate TEXT,
        idcard TEXT UNIQUE NOT NULL,
        position TEXT,
        salary REAL
    );
    ''')
    conn.commit()

def deleteTable():
    connect()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE employees''')
    conn.commit()
    disconnect()
    

def getStructure():
    connect()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(employees)")
    columns = cursor.fetchall()
    for column in columns:
        print(f"{column[1]}: {column[2]}")
