from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["plantas_db"]
collection = db["plantas"]

# Insertar datos con transacciones
with client.start_session() as session:
    with session.start_transaction():
        collection.insert_one(
            {
                "nombre": "Rosa",
                "familia": "Rosaceae",
                "tamaño": "Pequeña",
                "clima": "Templado",
                "tipo_suelo": "Arcilloso",
            },
            session=session,
        )
        collection.insert_one(
            {
                "nombre": "Cactus",
                "familia": "Cactaceae",
                "tamaño": "Mediana",
                "clima": "Árido",
                "tipo_suelo": "Arenoso",
            },
            session=session,
        )

# Leer datos
for planta in collection.find():
    print(planta)

# Actualizar un registro
collection.update_one({"nombre": "Rosa"}, {"$set": {"clima": "Cálido"}})

# Eliminar un registro
collection.delete_one({"nombre": "Cactus"})

client.close()
