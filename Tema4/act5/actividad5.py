import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent  # Clases para Herramientas y Proveedores


class Planta(Persistent):
    def __init__(self, id, nombre, familia, tamaño, clima, tipo_suelo, nombre_detalles):
        self.nombre = nombre
        self.familia = familia
        self.tamaño = tamaño
        self.clima = clima
        self.tipo_suelo = tipo_suelo
        self.nombre_detalles = nombre_detalles


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

# Verificar y crear colecciones si no existen
if "plantas" not in root:
    root["plantas"] = {}
if "detalles" not in root:
    root["detalles"] = {}
    root["detalles"]["Detalles1"] = DetallesPlanta(
        "Riego moderado", "Fertilizante orgánico"
    )
    root["detalles"]["Detalles2"] = DetallesPlanta(
        "Riego semanal", "Fertilizante químico"
    )

    # Insertar datos en Planta, incluyendo id_detalles
    root["plantas"]["Cactus"] = Planta(
        "Cactus", "Cactaceae", "Pequeño", "Seco", "Arenoso", "Detalles1"
    )
    root["plantas"]["Geranio"] = Planta(
        "Geranio", "Geraniaceae", "Mediano", "Templado", "Orgánico", "Detalles2"
    )
    root["plantas"]["Tulipán"] = Planta(
        "Tulipán", "Liliaceae", "Mediano", "Templado", "Arenoso", "Detalles1"
    )
    transaction.commit()
