# Librería de gestión de productos en SQLite

Esta librería proporciona métodos para interactuar con una base de datos SQLite y gestionar productos. Permite realizar operaciones como agregar, actualizar, eliminar, y obtener productos, así como algunas funciones de administración de la base de datos.

## Funciones

### `connect()`

Establece una conexión a la base de datos `database.db` si aún no se ha realizado. La conexión se mantiene globalmente en la variable `conn`. Se asegura de que la misma conexión sea utilizada en diferentes hilos.

### `disconnect()`

Cierra la conexión a la base de datos si está activa, y establece la variable `conn` a `None`.

### `addProduct(name, price, details, stock, picture=None, idPoster=1)`

Agrega un nuevo producto a la base de datos.

- **Parámetros**:
  - `name` (str): El nombre del producto (obligatorio).
  - `price` (float): El precio del producto (obligatorio).
  - `details` (str): Descripción del producto (obligatorio).
  - `stock` (int): La cantidad en stock del producto (obligatorio).
  - `picture` (str, opcional): URL o ruta a la imagen del producto (opcional).
  - `idPoster` (int, opcional): ID del usuario que ha agregado el producto (por defecto es `1`).

- **Retorna**: 
  - No retorna valor, pero el producto es agregado a la base de datos.

### `updateProduct(ID, field, data)`

Actualiza un campo de un producto en la base de datos.

- **Parámetros**:
  - `ID` (int): El ID del producto a actualizar.
  - `field` (str): El campo a actualizar (por ejemplo, `'name'`, `'price'`, `'stock'`, `'picture'`, etc.).
  - `data` (str | int | float): El nuevo valor para el campo especificado.

- **Retorna**: 
  - No retorna valor, pero el producto es actualizado en la base de datos.

### `deleteProduct(ID)`

Elimina un producto de la base de datos.

- **Parámetros**:
  - `ID` (int): El ID del producto a eliminar.

- **Retorna**: 
  - No retorna valor, pero el producto es eliminado de la base de datos.

### `getProducts()`

Obtiene todos los productos de la base de datos.

- **Retorna**: Una lista con los registros de todos los productos.

### `getAllProducts()`

Obtiene todos los productos de la base de datos y los convierte en un formato de diccionario.

- **Retorna**: Una lista de diccionarios con la información de todos los productos.

### `getLastID()`

Obtiene el siguiente ID disponible para un nuevo producto, basado en el último ID utilizado en la tabla `products`.

- **Retorna**: 
  - El próximo ID disponible (int). Si la tabla está vacía, devuelve `1`.

### Funciones de depuración (solo para desarrollo)

#### `clearProducts()`

Elimina todos los productos de la base de datos y realiza un `VACUUM` para optimizar el espacio.

#### `createTable()`

Crea la tabla `products` en la base de datos si no existe, con las columnas necesarias para almacenar la información de los productos.

#### `getStructure()`

Imprime la estructura de la tabla `products` mostrando los nombres y tipos de las columnas.

#### `deleteTable()`

Elimina la tabla `products` de la base de datos.

---

## Dependencias

- `sqlite3`: Para interactuar con la base de datos SQLite.

---

## Notas

- La conexión con la base de datos se maneja de forma global a través de la variable `conn`. 
- Asegúrate de llamar a `connect()` antes de utilizar cualquier método que interactúe con la base de datos.
- Para facilitar el desarrollo, algunas funciones de depuración están disponibles, pero deben eliminarse antes de lanzar la librería en producción.
