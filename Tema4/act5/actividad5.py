import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent

# Clase Planta
class Planta(Persistent):
    def __init__(self, id, nombre, familia, tamaño, clima, tipo_suelo, nombre_detalles):
        self.id = id
        self.nombre = nombre
        self.familia = familia
        self.tamaño = tamaño
        self.clima = clima
        self.tipo_suelo = tipo_suelo
        self.nombre_detalles = nombre_detalles 

# Clase DetallesPlanta
class DetallesPlanta(Persistent):
    def __init__(self, nombre_detalles, cuidados, fertilizantes):
        self.nombre_detalles = nombre_detalles
        self.cuidados = cuidados
        self.fertilizantes = fertilizantes

# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage("1dam.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

try:
    # Verificar y crear colecciones en root si no existen
    if "plantas" not in root:
        root["plantas"] = {}

    if "detalles" not in root:
        root["detalles"] = {}

    # Insertar datos en la colección de DetallesPlanta
    root["detalles"]["Detalles1"] = DetallesPlanta(
        "Detalles1", "Riego moderado", "Fertilizante orgánico"
    )
    root["detalles"]["Detalles2"] = DetallesPlanta(
        "Detalles2", "Riego semanal", "Fertilizante químico"
    )

    # Insertar datos en la colección de Planta, incluyendo el nombre de los detalles
    root["plantas"]["Cactus"] = Planta(
        1, "Cactus", "Cactaceae", "Pequeño", "Seco", "Arenoso", "Detalles1"
    )
    root["plantas"]["Geranio"] = Planta(
        2, "Geranio", "Geraniaceae", "Mediano", "Templado", "Orgánico", "Detalles2"
    )
    root["plantas"]["Tulipán"] = Planta(
        3, "Tulipán", "Liliaceae", "Mediano", "Templado", "Arenoso", "Detalles1"
    )

    # Confirmar la transacción
    transaction.commit()
    print("Transacción completada: Plantas y detalles añadidos correctamente.")

    #Plantas que tengan los detalles 2
    # Mostrar plantas asociadas con "Detalles1"
    print("Plantas con detalles Detalles1:")
    for nombre, planta in root["plantas"].items():
        if planta.nombre_detalles == "Detalles1":
            print(f"ID: {planta.id}, Nombre: {planta.nombre}, Familia: {planta.familia}, "
              f"Tamaño: {planta.tamaño}, Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}")


except Exception as e:
    transaction.abort()
    print(f"Error durante la transacción: {e}. Transacción revertida.")

finally:
    connection.close()
    db.close()
