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
# Creacion de los objetos
root["planta1"] = Planta(1, "Jazmín", "Oleaceae", "Mediano", "Templado", "Orgánico")
root["planta2"] = Planta(2, "Rosa", "Rosaceae", "Pequeño", "Húmedo", "Húmico")
root["planta3"] = Planta(
    3, "Aloe vera", "Asphodelaceae", "Mediano", "Templado", "Orgánico"
)
transaction.commit

# Recuperar y modificar un objeto
planta = root.get("planta3")  # Recuperar la planta almacenada con id planta3
if planta:
    print("Antes de la modificación:")
    print(
        f"ID: {planta.id}, Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.tamaño},Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
    )
    # Modificar el atributo 'tamaño'
    planta.tamaño = "Pequeño"
    transaction.commit()  # Confirmar los cambios en la base de datos
    print("Después de la modificación:")
    print(
        f"ID: {planta.id}, Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.tamaño},Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
    )
else:
    print("La herramienta no se encontró en la base de datos.")
# Cerrar la conexión
connection.close()
db.close()
