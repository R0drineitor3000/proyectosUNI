import sqlite3
from database.database import connect, disconnect, get_table_structure, print_table_structure

# Función para crear la tabla de cuentas
#(id, username, password, email, picture, role, creation_date, active)
def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            picture TEXT,
            role TEXT NOT NULL,
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    disconnect(conn)

# Función para eliminar la tabla de cuentas
def delete_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE accounts''')
    conn.commit()
    disconnect(conn)

# Función para insertar una cuenta
def add_account(username, email, password = None, role = 'customer'):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (username, password, email, role)
            VALUES (?, ?, ?, ?)
        ''', (username, password, email, role))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al insertar la cuenta: {e}")
        return False
    finally:
        disconnect(conn)

# Función para eliminar una cuenta
def delete_account(ID):
    conn = connect()
    cursor = conn.cursor()
    #Si ID es un número, buscar por ID, si no, buscar por username
    if isinstance(ID, int):
        cursor.execute('''
            DELETE FROM accounts WHERE id = ?
        ''', (ID,))
    elif isinstance(ID, str):
        cursor.execute('''
            DELETE FROM accounts WHERE username = ?
        ''', (ID,))
    conn.commit()
    disconnect(conn)
    
# Función para obtener una cuenta por ID o username
def get_account(ID):
    conn = connect()
    cursor = conn.cursor()
    #Si ID es un número, buscar por ID, si no, buscar por username
    if isinstance(ID, int):
        cursor.execute('''
            SELECT * FROM accounts WHERE id = ?
        ''', (ID,))
    elif isinstance(ID, str):
        cursor.execute('''
            SELECT * FROM accounts WHERE username = ?
        ''', (ID,))
    account = cursor.fetchone()
    disconnect(conn)
    return account

# Función para obtener una cuenta por email
def get_account_by_email(ID):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM accounts WHERE email = ?
    ''', (ID,))
    account = cursor.fetchone()
    disconnect(conn)
    return account

# Función para obtener la contraseña de una cuenta por ID o username
def get_password(ID):
    return get_from_account_by_email(ID, "password")

# Función para verificar si una cuenta está activa
def is_account_active(ID):
    active = get_from_account_by_email(ID, "active")
    return active == 1 if active is not None else False

# Función para verificar que un usuario exista
def account_exists(ID):
    user = get_account_by_email(ID)
    return user is not None

# Función para obtener todas las cuentas
def get_accounts():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM accounts
    ''')
    data = cursor.fetchall()
    disconnect(conn)
    return data

# Función para obtener todas las cuentas y convertirlas a diccionario
def get_all_accounts():
    return [dict(i) for i in get_accounts()]

# Función para actualizar una cuenta
def update_account(ID, field, data):
    allowed_fields = [f[1] for f in get_table_structure("accounts") if f[1] != "id"]

    if field not in allowed_fields:
        return False

    conn = connect()
    cursor = conn.cursor()

    try:
        if isinstance(ID, int):
            query = f"UPDATE accounts SET {field} = ? WHERE id = ?"
        elif isinstance(ID, str):
            query = f"UPDATE accounts SET {field} = ? WHERE username = ?"
        else:
            return False  # ID no válido

        cursor.execute(query, (data, ID))
        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Error al actualizar la cuenta: {e}")
        return False

    finally:
        disconnect(conn)

def update_account_by_email(ID, field, data):
    allowed_fields = [f[1] for f in get_table_structure("accounts") if f[1] != "id"]

    if field not in allowed_fields:
        return False

    conn = connect()
    cursor = conn.cursor()

    try:
        query = f"UPDATE accounts SET {field} = ? WHERE email = ?"

        cursor.execute(query, (data, ID))
        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Error al actualizar la cuenta: {e}")
        return False

    finally:
        disconnect(conn)

def is_fully_identified(email):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, email FROM accounts WHERE email = ?
    ''', (email,))
    data = cursor.fetchone()
    
    if data is None:
        return False

    return all(field is not None for field in data)

# Función para obtener un elemento de una cuenta en la base de datos
def get_from_account(ID, field):
    allowed_fields = [f[1] for f in get_table_structure("accounts") if f[1] != "id"]
    if field not in allowed_fields:
        return False
    
    if account_exists(ID):
        try:
            conn = connect()
            cursor = conn.cursor()
            # Construcción dinámica de la consulta
            if isinstance(ID, int):
                query = f"SELECT {field} FROM accounts WHERE id = ?"
            elif isinstance(ID, str):
                query = f"SELECT {field} FROM accounts WHERE username = ?"
            cursor.execute(query, (ID,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener el campo del usuario: {e}")
            return None
        finally:
            disconnect(conn)
    else:
        return None
    
# Función para obtener un elemento de una cuenta por medio de su email
def get_from_account_by_email(ID, field):
    allowed_fields = [f[1] for f in get_table_structure("accounts") if f[1] != "id"]
    if field not in allowed_fields:
        return False
    
    if account_exists(ID):
        try:
            conn = connect()
            cursor = conn.cursor()
            # Construcción dinámica de la consulta
            query = f"SELECT {field} FROM accounts WHERE email = ?"
            cursor.execute(query, (ID,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener el campo del usuario: {e}")
            return None
        finally:
            disconnect(conn)
    else:
        return None

# Función para buscar cuentas en la base de datos
def search_users(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE username LIKE ?", ('%' + username + '%',))
    data = cursor.fetchall()
    users=[]
    if data:
        for user in data:
            users.append(dict(user))
    disconnect(conn)
    return users