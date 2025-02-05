from pymongo import MongoClient, errors

# Datos de conexión
usuario = "usuario"
clave = "usuario"
base_datos = "1dam"
host = "localhost"
puerto = 27017

try:
    # Intentar conectarse al servidor MongoDB
    client = MongoClient(
        f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}",
        serverSelectionTimeoutMS=5000,
    )

    # Seleccionar la base de datos
    db = client[base_datos]

    # Eliminar la colección "Productos" si existe
    if "Productos" in db.list_collection_names():
        db.Productos.drop()
        print("Colección 'Productos' eliminada.")

    # Intentar acceder a la base de datos para verificar la conexión
    colecciones = db.list_collection_names()
    print("Conexión exitosa. Colecciones en la base de datos:")
    print(colecciones)
except errors.ServerSelectionTimeoutError as err:
    # Este error ocurre si el servidor no está disponible o no se puede conectar
    print(f"No se pudo conectar a MongoDB: {err}")
except errors.OperationFailure as err:
    # Este error ocurre si las credenciales son incorrectas o no se tienen los permisos necesarios
    print(f"Fallo en la autenticación o permisos insuficientes: {err}")
except Exception as err:
    # Manejar cualquier otro error inesperado
    print(f"Ocurrió un error inesperado: {err}")

try:
    coleccion_productos = db.create_collection("Productos")
    # Intentar acceder a la base de datos para verificar la conexión
    colecciones = db.list_collection_names()
    print(
        "Conexión exitosa. Colecciones en la base de datos después de la creación de productos:"
    )
    print(colecciones)

    # Creación de 3 productos
    coleccion_productos.insert_many(
        [
            {
                "nombre": "Laptop Lenovo",
                "precio": 799.99,
                "categoria": "Electrónica",
                "stock": 15,
                "descuento": 10.0,
            },
            {
                "nombre": "Mesa",
                "precio": 299.99,
                "categoria": "Mueble",
                "stock": 25,
                "descuento": 9.0,
            },
            {
                "nombre": "Lavadora",
                "precio": 399.99,
                "categoria": "Electrodoméstico",
                "stock": 8,
                "descuento": 50.0,
            },
        ]
    )

    print("Productos:")
    productos = coleccion_productos.find()
    for producto in productos:
        print(producto)

    print("Productos cuyo precio es mayor a 300:")
    # Limita los resultados a dos productos y ordénalos en orden descendente por precio.
    productos = (
        coleccion_productos.find({"precio": {"$gt": 300}}).limit(2).sort("precio", -1)
    )
    for producto in productos:
        print(producto)

    # Selecciona un producto por su nombre y actualiza su precio y stock con update_one().
    coleccion_productos.update_one(
        {"nombre": "Laptop Lenovo"},
        {"$set": {"nombre": "Portátil Lenovo", "stock": 20}},
    )
    print("Productos después de la actualización de nombre y stock:")
    productos = coleccion_productos.find()
    for producto in productos:
        print(producto)

    # Aumenta el stock de todos los productos de la categoría "Electrónica" en 10 unidades usando update_many().
    coleccion_productos.update_many(
        {"categoria": "Electrónica"}, {"$inc": {"stock": 10}}
    )
    print("Productos después de la actualización del stock:")
    productos = coleccion_productos.find()
    for producto in productos:
        print(producto)

    # Elimina un producto que tenga stock igual a 0 con delete_one().
    coleccion_productos.delete_one({"stock": 0})
    print("Productos después de la eliminación de stock 0:")
    productos = coleccion_productos.find()
    for producto in productos:
        print(producto)

    # Elimina todos los productos de la categoría "Electrónica" con delete_many().
    coleccion_productos.delete_many({"categoria": "Electrónica"})
    print("Productos después de la eliminación de la categoría Electrónica:")
    productos = coleccion_productos.find()
    for producto in productos:
        print(producto)

except errors.ServerSelectionTimeoutError as err:
    # Este error ocurre si el servidor no está disponible o no se puede conectar
    print(f"No se pudo conectar a MongoDB: {err}")
except errors.OperationFailure as err:
    # Este error ocurre si las credenciales son incorrectas o no se tienen los permisos necesarios
    print(f"Fallo en la autenticación o permisos insuficientes: {err}")
except Exception as err:
    # Manejar cualquier otro error inesperado
    print(f"Ocurrió un error inesperado: {err}")
finally:
    # Cerrar la conexión si se estableció correctamente
    if "client" in locals():
        client.close()
        print("Conexión cerrada.")
