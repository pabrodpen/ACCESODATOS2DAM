from peewee import MySQLDatabase, Model, CharField, DateField, DoubleField, ForeignKeyField, IntegrityError


#get es para un solo dato
#select para varios y se itera con for

# Configurar la base de datos
db = MySQLDatabase(
    "1dam",
    user="root",
    password="usuario",
    host="localhost",
    port=3306,
)

# Conectar a la base de datos
db.connect()
print("Conexión exitosa a la base de datos.")

# Modelos
class Cliente(Model):
    nombre = CharField(unique=True)
    email = CharField()
    direccion = CharField()

    class Meta:
        database = db
        table_name = "Cliente"

class Pedido(Model):
    fecha = DateField()
    monto_total = DoubleField()
    nombre_cliente = ForeignKeyField(Cliente, backref="pedidos", on_delete="CASCADE")

    class Meta:
        database = db
        table_name = "Pedido"

# Crear tablas
db.create_tables([Cliente, Pedido])

# Limpiar tablas existentes
Cliente.delete().execute()
Pedido.delete().execute()

# Insertar datos
try:
    with db.atomic():
        Cliente.create(nombre="Juan", email="hola@gmail.com", direccion="calle 123")
        Cliente.create(nombre="Pablo", email="adios@gmail.com", direccion="calle 456")
        Cliente.create(nombre="Maria", email="123@gmail.com", direccion="av 123")
        Cliente.create(nombre="Carlos", email="abcd@gmail.com", direccion="av 456")
        Cliente.create(nombre="Manuel", email="456@gmail.com", direccion="plaza 123")

        Pedido.create(fecha="2024-01-01", monto_total=325, nombre_cliente=Cliente.get(Cliente.nombre == "Pablo"))
        Pedido.create(fecha="2024-02-02", monto_total=235.78, nombre_cliente=Cliente.get(Cliente.nombre == "Juan"))
        Pedido.create(fecha="2024-03-03", monto_total=117, nombre_cliente=Cliente.get(Cliente.nombre == "Maria"))
        Pedido.create(fecha="2024-04-04", monto_total=234.90, nombre_cliente=Cliente.get(Cliente.nombre == "Maria"))
        Pedido.create(fecha="2024-05-05", monto_total=21.78, nombre_cliente=Cliente.get(Cliente.nombre == "Manuel"))
        Pedido.create(fecha="2024-06-06", monto_total=78.23, nombre_cliente=Cliente.get(Cliente.nombre == "Pablo"))
        Pedido.create(fecha="2024-07-07", monto_total=98.78, nombre_cliente=Cliente.get(Cliente.nombre == "Pablo"))
        Pedido.create(fecha="2024-08-08", monto_total=432.12, nombre_cliente=Cliente.get(Cliente.nombre == "Carlos"))
        Pedido.create(fecha="2024-09-09", monto_total=400, nombre_cliente=Cliente.get(Cliente.nombre == "Juan"))
        Pedido.create(fecha="2024-10-10", monto_total=23.12, nombre_cliente=Cliente.get(Cliente.nombre == "Carlos"))
except IntegrityError as e:
    print(f"Error al insertar datos: {e}")

# Pedidos realizados por un cliente
cliente_seleccionado = "Pablo"
pedidos = Pedido.select().join(Cliente).where(Cliente.nombre == cliente_seleccionado)
print(f"Pedidos realizados por {cliente_seleccionado}:")
for pedido in pedidos:
    print(pedido.fecha, pedido.monto_total)

# Clientes con pedidos con un monto superior a 100
clientes_monto = Cliente.select().join(Pedido).where(Pedido.monto_total > 100).distinct()
print("Clientes con pedidos superiores a 100:")
for cliente in clientes_monto:
    print(cliente.nombre)

# Todos los pedidos
print("Todos los pedidos:")
for pedido in Pedido.select():
    print(pedido.fecha, pedido.monto_total, pedido.nombre_cliente.nombre)

# Actualizar la dirección de un cliente
print("Antes de la modificación:")
cliente_editado = Cliente.get(Cliente.nombre == "Manuel")
print(cliente_editado.nombre, cliente_editado.email, cliente_editado.direccion)

Cliente.update(direccion="Barriada 123").where(Cliente.nombre == "Manuel").execute()

print("Después de la modificación:")
cliente_modificado = Cliente.get(Cliente.nombre == "Manuel")
print(cliente_modificado.nombre, cliente_modificado.email, cliente_modificado.direccion)

# Incrementar el monto de todos los pedidos antes de una fecha específica
fecha = "2024-06-06"
incremento = 200
print("Antes del incremento:")
for pedido in Pedido.select().where(Pedido.fecha < fecha):
    print(pedido.fecha, pedido.monto_total)

Pedido.update(monto_total=Pedido.monto_total + incremento).where(Pedido.fecha < fecha).execute()

print("Después del incremento:")
for pedido in Pedido.select().where(Pedido.fecha < fecha):
    print(pedido.fecha, pedido.monto_total)

# Eliminar un cliente y sus pedidos (ON DELETE CASCADE)
Cliente.delete().where(Cliente.nombre == "Maria").execute()

print("Clientes y pedidos después de eliminar a 'Maria':")
for cliente in Cliente.select():
    print(cliente.nombre, cliente.email, cliente.direccion)
for pedido in Pedido.select():
    print(pedido.fecha, pedido.monto_total, pedido.nombre_cliente.nombre)

# Eliminar todos los pedidos cuyo monto sea inferior a 50
print("Antes de la eliminación:")
for pedido in Pedido.select():
    print(pedido.fecha, pedido.monto_total, pedido.nombre_cliente.nombre)

Pedido.delete().where(Pedido.monto_total < 50).execute()

print("Después de la eliminación:")
for pedido in Pedido.select():
    print(pedido.fecha, pedido.monto_total, pedido.nombre_cliente.nombre)
