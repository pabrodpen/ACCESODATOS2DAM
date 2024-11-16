from pymongo import MongoClient, errors
# Datos de conexión
usuario = "usuario"
clave = "usuario"
base_datos = "1dam"
host = "localhost"
puerto = 27017
try:
    # Intentar conectarse al servidor MongoDB
    client = MongoClient( f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}",
    serverSelectionTimeoutMS=5000)
    # Seleccionar la base de datos
    db = client["1dam"]
    coleccion_plantas = db["Plantas"]


    # 1. Consultar plantas cuyo clima sea "Templado"
    print("Plantas con clima 'Templado':")
    consulta = {"clima": "Templado"}
    plantas = coleccion_plantas.find(consulta)
    for planta in plantas:
        print(planta)

    # 2. Proyección de campos específicos
    print("\nMostrar solo 'nombre' y 'clima':")
    proyeccion = {"nombre": 1, "clima": 1, "_id": 0}
    plantas = coleccion_plantas.find(consulta, proyeccion)
    for planta in plantas:
        print(planta)

    # 3. Limitar y ordenar resultados
    print("\n2 plantas ordenadas alfabéticamente por 'nombre':")
    plantas = coleccion_plantas.find(consulta, proyeccion).sort("nombre", 1).limit(2)
    for planta in plantas:
        print(planta)

    # 4. Consultas con expresiones regulares
    print("\n4. Plantas cuyos nombres comienzan con la letra 'P':")
    consulta = {"nombre": {"$regex": "^P"}}
    plantas = coleccion_plantas.find(consulta)
    for planta in plantas:
        print(planta)

    # 5. Contar documentos con una condición
    print("\nContar plantas con clima 'Templado':")
    total = coleccion_plantas.count_documents({"clima": "Templado"})
    print(f"Total de plantas con clima templado: {total}")

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