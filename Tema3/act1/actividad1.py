from peewee import MySQLDatabase, Model, CharField


def tabla_existe(nombre_tabla):
    consulta = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"
    cursor = db.execute_sql(consulta, ("1dam", nombre_tabla))
    resultado = cursor.fetchone()
    return resultado[0] > 0


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

    # Eliminamos la tabla si ya existe para empezar a trabajar desde cero
    if tabla_existe(db._meta.Plantas):
        print(f"La tabla '{db._meta.Plantas}' existe.")
        db.drop_tables([db], cascade=True)
        print(f"Tabla '{db._meta.Plantas}' eliminada con éxito.")
    else:
        print(f"La tabla '{db._meta.Plantas}' no existe.")


# Insertar varias plantas
Plantas.create(
    nombre="Lirio",
    familia="Iridaceae",
    tamaño="Pequeño",
    clima="Templado",
    tipo_suelo="Arenoso",
)
Plantas.create(
    nombre="Sauce",
    familia="Salicaceae",
    tamaño="Grande",
    clima="Húmedo",
    tipo_suelo="Húmico",
)
Plantas.create(
    nombre="Orquídea",
    familia="Orchidaceae",
    tamaño="Mediano",
    clima="Tropical",
    tipo_suelo="Orgánico",
)
Plantas.create(
    nombre="Césped",
    familia="Poaceae",
    tamaño="Bajo",
    clima="Templado",
    tipo_suelo="Arenoso",
)
Plantas.create(
    nombre="Hortensia",
    familia="Hydrangeaceae",
    tamaño="Mediano",
    clima="Templado",
    tipo_suelo="Fértil",
)
print("Plantas insertadas en la base de datos.")