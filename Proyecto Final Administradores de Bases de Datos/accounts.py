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


def addUser(email, username=None, picture=None, password=None, role="customer"): #Si se registran desde google, solo requieren el email
    connect()
    if not userExists(email):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (
                email,
                username,
                password,
                role,
                picture
            )
            VALUES (?, ?, ?, ?, ?)
        ''', (email, username, password, role, picture))
        conn.commit()
        return True
    return False

def updateUser(email, field, data):
    valid_fields = ['id', 'email', 'username', 'password', 'role', 'picture', 'biography']
    if field not in valid_fields:
        return False
    
    connect()

    if userExists(email):
        try:
            cursor = conn.cursor()
            # Construcción dinámica de la consulta
            query = f"UPDATE accounts SET {field} = ? WHERE email = ?"
            cursor.execute(query, (data, email))
            conn.commit()  # Asegúrate de hacer commit después de la ejecución
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Error al actualizar el usuario: {e}")
            return False
    else:
        return False

def deleteUser(email):
    connect()
    if userExists(email):
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM accounts
            WHERE email = ?''',
            (email,))
        conn.commit()
        return True
    return False

def isFullyIdentified(email):
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM accounts WHERE email = ?
    ''', (email,))
    data = cursor.fetchone()
    
    if data is None:
        return False  # Si no se encuentra el usuario, retornamos False

    
    for column in data.keys():  # Iteramos sobre los nombres de las columnas
        if column != 'password' and column != 'picture' and column != 'biography' and data[column] is None: #Los usuarios de google no necesitan contrasseña, así que no se busca. La imagen no es necesaria para comprobar un registro completo.
            return False

    return True

def getFromUser(email, field):
    valid_fields = ['id', 'email', 'username', 'password', 'role', 'picture', 'biography']
    if field not in valid_fields:
        return False
    
    connect()
    if userExists(email):
        try:
            cursor = conn.cursor()
            # Construcción dinámica de la consulta
            query = f"SELECT {field} FROM accounts WHERE email = ?"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener el campo del usuario: {e}")
            return None
    else:
        return None

def getUserByUsername(username):
    connect()
    try:
        cursor = conn.cursor()
        # Construcción dinámica de la consulta
        query = f"SELECT * FROM accounts WHERE username = ?"
        cursor.execute(query, (username,))
        data = cursor.fetchone()
        if data is not None:
            return dict(data)
        return None
    except sqlite3.Error as e:
        print(f"Error al obtener el campo del usuario: {e}")
        return None

def getUsers():
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM accounts
    ''')
    data = cursor.fetchall()
    return data

def getAllUsers():
    users = []
    for i in getUsers():
        users.append(dict(i))
    return users

def getUser(ID):
    connect()
    cursor = conn.cursor()
    if isinstance(ID, str):
        cursor.execute('''SELECT * FROM accounts WHERE email = ?''', (ID,))
    elif isinstance(ID, int):
        cursor.execute('''SELECT * FROM accounts WHERE id = ?''', (ID,))
    else:
        return None
    data = cursor.fetchone()
    if data is not None:
        return dict(data)
    return None

def getUserLike(username):
    connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE username LIKE ?", ('%' + username + '%',))
    data = cursor.fetchall()
    users=[]
    if data:
        for user in data:
            users.append(dict(user))
    return users
    

def userExists(email):
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM accounts WHERE email = ?
    ''', (email,))
    return cursor.fetchone() is not None

def usernameExists(username):
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM accounts WHERE username = ?
    ''', (username,))
    return cursor.fetchone() is not None

def getUserPassword(email):
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT password FROM accounts WHERE email = ?
        ''', (email,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

###############################################
###############################################
############# DEBUG FUNCTIONS #################
########### DELETE WHEN RELEASING #############
###############################################
###############################################
def clearUsers():
    connect()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM accounts''')
    conn.commit()  # Cometer la transacción antes de ejecutar VACUUM
    cursor.execute('''VACUUM''')  # Ejecutar VACUUM fuera de la transacción
    conn.commit()  # Cometer la transacción de VACUUM

def createTable():
    connect()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    picture TEXT,
    biography TEXT,
    creationdate DATE DEFAULT (CURRENT_TIMESTAMP)
    );''')
    conn.commit()

def deleteTable():
    connect()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE accounts''')
    conn.commit()
    disconnect()
    

def getStructure():
    connect()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(accounts)")
    columns = cursor.fetchall()
    for column in columns:
        print(f"{column[1]}: {column[2]}")
