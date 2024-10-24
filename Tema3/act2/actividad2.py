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
# Buscar todas las Plantas de clima 'Templado'
print("Plantas de clima templado")
plantas_climas_templados = Plantas.select().where(Plantas.clima == "Templado")
for planta in plantas_climas_templados:
    print(
        f"Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.tamaño}, Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
    )

print("Tarea2 ...")
# Eliminamos una planta cuyo tamaño sea Mediano y cuyo clima sea Templado(operador &)
Plantas.delete().where(
    (Plantas.tamaño == "Mediano") & (Plantas.clima == "Templado")
).execute()
print("Planta con tamaño Mediano y clima Templado eliminada.")

# mostramos los registros restantes
# Mostrar los registros restantes después de la eliminación
print("REGISTROS DESPUÉS DE LA ELIMINACIÓN:")
for planta in Plantas.select():
    print(
        f"Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.tamaño}, Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
    )

print("Tarea3 ...")

# Eliminamos una serie de registros
Plantas.delete().where(Plantas.tipo_suelo == "Arenoso").execute()
print("Plantas de tipo Arenoso eliminadas")
# Mostrar los registros restantes después de la eliminación
print("REGISTROS DESPUÉS DE LA ELIMINACIÓN:")
for planta in Plantas.select():
    print(
        f"Nombre: {planta.nombre}, Familia: {planta.familia}, Tamaño: {planta.tamaño}, Clima: {planta.clima}, Tipo de suelo: {planta.tipo_suelo}"
    )
