import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent


# Definir la clase Planta
class Planta(Persistent):
    def __init__(self, id, nombre, familia, tamaño, clima, tipo_suelo):
        self.id = id
        self.nombre = nombre
        self.familia = familia
        self.tamaño = tamaño
        self.clima = clima
        self.tipo_suelo = tipo_suelo


# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage("1dam.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

try:
    # Crear una colección de plantas en root si no existe y añadir plantas a ella
    if "plantas" not in root:
        root["plantas"] = {}

    # Añadir registros de plantas
    root["plantas"]["Rosa"] = Planta(
        1, "Rosa", "Rosaceae", "Pequeño", "Húmedo", "Orgánico"
    )
    root["plantas"]["Amapola"] = Planta(
        2, "Amapola", "Papaveraceae", "Mediano", "Tropical", "Húmico"
    )
    root["plantas"]["Tulipán"] = Planta(
        3, "Tulipán", "Liliaceae", "Mediano", "Templado", "Arenoso"
    )

    transaction.commit()
    print("Transacción completada: Herramientas añadidas correctamente.")

    print(
        "REGISTROS"
    )  # si da error no mostrará ningún registro, ya que no se habrá insertado nada
    for nombre, planta in root["plantas"].items():
        print(
            print(
                f"ID: {planta.id}, Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.tamaño}, Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
            )
        )

except Exception as e:
    # Si ocurre un error, revertimos la transacción
    transaction.abort()
    print(f"Error durante la transacción: {e}. Transacción revertida.")
