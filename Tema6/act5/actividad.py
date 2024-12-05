import transaction
from ZODB import DB, FileStorage
from persistent import Persistent


# Clase Planta
class Planta(Persistent):
    def __init__(self, nombre, familia, tamaño, clima, tipo_suelo):
        self.nombre = nombre
        self.familia = familia
        self.tamaño = tamaño
        self.clima = clima
        self.tipo_suelo = tipo_suelo


# Configurar base de datos
storage = FileStorage.FileStorage("plantas.fs")
db = DB(storage)
connection = db.open()
root = connection.root()

# Crear contenedor si no existe
if "plantas" not in root:
    root["plantas"] = {}

# Operaciones con transacciones
try:
    # Insertar registros
    transaction.begin()
    root["plantas"]["1"] = Planta(
        "Rosa", "Rosaceae", "Pequeña", "Templado", "Arcilloso"
    )
    root["plantas"]["2"] = Planta("Cactus", "Cactaceae", "Mediana", "Árido", "Arenoso")
    root["plantas"]["3"] = Planta("Pino", "Pinaceae", "Grande", "Frío", "Ácido")
    transaction.commit()

    # Leer registros
    for id, planta in root["plantas"].items():
        print(f"ID: {id}, Nombre: {planta.nombre}, Clima: {planta.clima}")

    # Actualizar un registro
    transaction.begin()
    root["plantas"]["1"].clima = "Cálido"
    transaction.commit()

    # Eliminar un registro no existente
    transaction.begin()
    if "99" in root["plantas"]:
        del root["plantas"]["99"]
    else:
        print("Registro con ID 99 no encontrado.")
    transaction.abort()
except Exception as e:
    print(f"Error: {e}")
    transaction.abort()
finally:
    connection.close()
    db.close()
