from peewee import MySQLDatabase, Model, CharField

# Configurar la base de datos
db = MySQLDatabase(
    "1dam",  # Nombre de la base de datos
    user="usuario",  # Usuario de MySQL
    password="usuario",  # Contraseña de MySQL
    host="localhost",  # Host
    port=3306,  # Puerto por defecto de MySQL
)

# Conectar a la base de datos
db.connect()
print("Conexión exitosa a la base de datos.")


# Definir el mapeo de la tabla Plantas
class Plantas(Model):
    nombre = CharField()
    familia = CharField()
    tamaño = CharField()
    clima = CharField()
    tipo_suelo = CharField()

    class Meta:
        database = db  # Base de datos
        table_name = "Plantas"  # Nombre de la tabla en la base de datos


print("Tarea1...")
# Buscar todas las herramientas de tipo 'Manual'
plantas_climas_templados = Plantas.select().where(Plantas.clima == "Templado")
for planta in plantas_climas_templados:
    print(
        f"Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.tamaño}, Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
    )
