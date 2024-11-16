import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent


# Definir clase Planta
class Planta(Persistent):
    def __init__(self, id, nombre, familia, tamaño, clima, tipo_suelo):
        self.id = id
        self.nombre = nombre
        self.familia = familia
        self.tamaño = tamaño
        self.clima = clima
        self.tipo_suelo = tipo_suelo


# Establecer conexión
storage = ZODB.FileStorage.FileStorage("1dam.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()
# Almacenar 3 plantas
root["planta1"] = Planta(1, "Jazmín", "Oleaceae", "Mediano", "Templado", "Orgánico")
root["planta2"] = Planta(2, "Rosa", "Rosaceae", "Pequeño", "Húmedo", "Húmico")
root["planta3"] = Planta(
    3, "Aloe vera", "Asphodelaceae", "Mediano", "Templado", "Orgánico"
)

transaction.commit()


# Filtrar plantas por clima
tipo_deseado = "Templado"
print("Plantas de clima Templado")
for clave, planta in root.items():
    if hasattr(planta, "clima") and planta.clima == tipo_deseado:
        print(
            f"ID: {planta.id}, Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.
tamaño }, Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
        )
# Cerrar conexión
connection.close()
db.close()
