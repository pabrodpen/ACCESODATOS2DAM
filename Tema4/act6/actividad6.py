import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent
import copy

# Clase Planta
class Planta(Persistent):
    def __init__(self, id, nombre, familia, tamaño, clima, tipo_suelo, nombre_detalles):
        self.id = id
        self.nombre = nombre
        self.familia = familia
        self.tamaño = tamaño
        self.clima = clima
        self.tipo_suelo = tipo_suelo
        self.nombre_detalles = nombre_detalles  # Referencia a un objeto de DetallesPlanta

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

    # Plantas que tengan los detalles 'Detalles2'
    print("Plantas con detalles Detalles1:")
    for nombre, planta in root["plantas"].items():
        # Crear una copia independiente de la planta usando deepcopy
        planta_copia = copy.deepcopy(planta)
        
        if planta_copia.nombre_detalles == "Detalles1":
            print(f"ID: {planta_copia.id}, Nombre: {planta_copia.nombre}, Familia: {planta_copia.familia}, "
                  f"Tamaño: {planta_copia.tamaño}, Clima: {planta_copia.clima}, Tipo de suelo: {planta_copia.tipo_suelo}")

except Exception as e:
    # Si ocurre un error, revertimos la transacción
    transaction.abort()
    print(f"Error durante la transacción: {e}. Transacción revertida.")

finally:
    # Cerrar la conexión a la base de datos
    connection.close()
    db.close()
