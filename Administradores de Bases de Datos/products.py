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

def addProduct(name, price, details, stock, picture=None, idPoster=1):
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (
            name,
            price,
            stock,
            picture,
            idPoster
        )
        VALUES (?, ?, ?, ?, ?)
    ''', (name, price, stock, picture, idPoster))
    conn.commit()

def updateProduct(ID, field, data):
    connect()
    cursor = conn.cursor()
    query = f"UPDATE accounts SET {field} = ? WHERE email = ?"
    cursor.execute(query, (data, ID))

def deleteProduct(ID):
    connect()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM products WHERE id = ?''', (ID,))
    conn.commit()

def getProducts():
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM products
    ''')
    data = cursor.fetchall()
    return data

def getProduct(ID):
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM products WHERE id = ?
    ''', (ID,))
    data = cursor.fetchone()
    if data:
        return dict(data)
    return None

def getAllProducts():
    products = []
    for i in getProducts():
        products.append(dict(i))
    return products

def getLastID():
    connect()
    cursor = conn.cursor()
    # Consulta para obtener el último valor autoincremental
    cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='products'")
    last_id = cursor.fetchone()
    next_id = None

    # Si la tabla ya tiene al menos una fila, obtenemos el próximo id
    if last_id:
        next_id = last_id[0] + 1
    else:
        # Si la tabla está vacía, el primer ID será 1
        next_id = 1

    return next_id

###############################################
###############################################
############# DEBUG FUNCTIONS #################
########### DELETE WHEN RELEASING #############
###############################################
###############################################
def clearProducts():
    connect()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM products''')  # Eliminar los registros
    cursor.execute('''DELETE FROM sqlite_sequence WHERE name='products' ''')  # Reiniciar contador de autoincremento
    conn.commit()  # Cometer la transacción
    cursor.execute('''VACUUM''')  # Ejecutar VACUUM fuera de la transacción
    conn.commit()  # Cometer la transacción de VACUUM

def createTable():
    connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            details TEXT,
            price REAL NOT NULL,
            stock INTEGER,
            picture TEXT,
            idPoster INTEGER DEFAULT 0,
            FOREIGN KEY(idPoster) REFERENCES accounts(id)
        );
    ''')
    conn.commit()
    disconnect()


def getStructure():
    connect()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(products)")
    columns = cursor.fetchall()
    for column in columns:
        print(f"{column[1]}: {column[2]}")

def deleteTable():
    connect()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE products''')
    conn.commit()
    disconnect()
