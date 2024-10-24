from peewee import MySQLDatabase, Model, CharField, IntegrityError


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


# Comprobar si la tabla existe antes de crearla
if tabla_existe("Plantas"):
    print(f"La tabla 'Plantas' existe.")
    db.drop_tables(
        [Plantas], cascade=True
    )  # Asegúrate de pasar la clase, no el objeto db
    print(f"Tabla 'Plantas' eliminada con éxito.")

# Crear la tabla nuevamente
db.create_tables([Plantas])
print(f"Tabla 'Plantas' creada con éxito.")

try:
    # Iniciar una transacción utilizando db.atomic()
    with db.atomic():
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
        # Este registro fallará porque 'nombre' es None
        Plantas.create(
            nombre=None,
            familia="Hydrangeaceae",
            tamaño="Mediano",
            clima="Templado",
            tipo_suelo="Fértil",
        )
        print("Plantas insertadas en la base de datos.")
except IntegrityError as e:
    print(f"Error al insertar plantas: {e}")

# select para ver que se han deshecho los cambios
print("REGISTROS")
for planta in Plantas.select():
    print(
        f"Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.tamaño}, Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
    )
