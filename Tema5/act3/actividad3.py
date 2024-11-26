from pymongo import MongoClient,errors

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
    # Seleccionar la base de datos y la colección "Plantas"
    db = client[base_datos]
    coleccion_plantas = db["Plantas"]


    # 1. Añadir tres documentos a la colección "Plantas"
    documentos = [
        {
            "nombre": "Rosa",
            "familia": "Rosáceas",
            "tamaño": "Mediana",
            "clima": "Templado",
            "tipo_suelo": "Arenoso",
        },
        {
            "nombre": "Cactus",
            "familia": "Cactaceae",
            "tamaño": "Pequeño",
            "clima": "Seco",
            "tipo_suelo": "Pedregoso",
        },
        {
            "nombre": "Tulipán",
            "familia": "Liliáceas",
            "tamaño": "Grande",
            "clima": "Frío",
            "tipo_suelo": "Bien drenado",
        },
    ]

    # Insertar los documentos
    resultados = coleccion_plantas.insert_many(documentos)
    print("Documentos añadidos a la colección:")

    # Mostrar los documentos añadidos
    for planta in coleccion_plantas.find():
        print(planta)

    # 2. Actualizar un campo de un solo documento
    # Actualizamos el tamaño de la planta "Cactus"
    resultado_actualizacion = coleccion_plantas.update_one(
        {"nombre": "Cactus"},  # Filtro para encontrar el documento
        {"$set": {"tamaño": "Mediano"}}, 
    )
    if resultado_actualizacion.modified_count > 0:
        print("\nDocumento actualizado con éxito.")
    else:
        print("\nNo se encontró el documento o no hubo cambios.")

    # 3. Eliminar uno de los documentos
    # Supongamos que queremos eliminar el documento de "Rosa"
    consulta_eliminar = {"nombre": "Rosa"}

    resultado_eliminacion = coleccion_plantas.delete_one(consulta_eliminar)
    if resultado_eliminacion.deleted_count > 0:
        print("\nDocumento eliminado con éxito.")
    else:
        print("\nNo se encontró el documento para eliminar.")

    # Mostrar los documentos restantes
    print("\nDocumentos restantes en la colección:")
    for planta in coleccion_plantas.find():
        print(planta)

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
    if 'client' in locals():
        client.close()
        print("Conexión cerrada.")
