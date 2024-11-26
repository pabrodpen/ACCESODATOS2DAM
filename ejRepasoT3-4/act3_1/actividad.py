from peewee import MySQLDatabase, Model, CharField,DateTime,DoubleField,IntegrityError

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
class Cliente(Model):
    nombre = CharField()
    email = CharField()
    direccion = CharField()

class Meta:
    database = db  # Base de datos
    table_name = "Cliente"  # Nombre de la tabla en la base de datos

db.create_tables(["Cliente"])


class Pedido(Model):
    fecha=DateTime()
    monto_total=DoubleField()
    nombre_cliente=CharField()

class Meta:
    database = db  # Base de datos
    table_name = "Pedido"  # Nombre de la tabla en la base de datos

db.create_tables(["Pedido"])

#inserciones de 5 clientes y 10 pedidos
try:
    with db.atomic():
        Cliente.create(nombre="Juan",email="hola@gmail.com",direccion="calle 123")
        Cliente.create(nombre="Pablo",email="adios@gmail.com",direccion="calle 456")
        Cliente.create(nombre="Maria",email="123@gmail.com",direccion="av 123")
        Cliente.create(nombre="Carlos",email="abcd@gmail.com",direccion="av 456")
        Cliente.create(nombre="Manuel",email="456@gmail.com",direccion="plaza 123")

        Pedido.create(fecha="01-01-2024",monto_total= 325,nombre_cliente="Pablo")
        Pedido.create(fecha="02-02-2024",monto_total= 235.78,nombre_cliente="Juan")
        Pedido.create(fecha="03-03-2024",monto_total= 117,nombre_cliente="Maria")
        Pedido.create(fecha="04-04-2024",monto_total= 234.90,nombre_cliente=",Maria")
        Pedido.create(fecha="05-05-2024",monto_total= 21.78,nombre_cliente="Manuel")
        Pedido.create(fecha="06-06-2024",monto_total= 78.23,nombre_cliente="Pablo")
        Pedido.create(fecha="07-07-2024",monto_total= 98.78,nombre_cliente="Pablo")
        Pedido.create(fecha="08-08-2024",monto_total= 432.12,nombre_cliente="Carlos")
        Pedido.create(fecha="09-09-2024",monto_total= 400,nombre_cliente="Juan")
        Pedido.create(fecha="10-10-2024",monto_total= 23.12,nombre_cliente="Carlos")
except IntegrityError as e:
    print(f"Error al insertar plantas: {e}")


#pedidos realizados por un cliente
cliente_seleccionado="Pablo"
pedidos=Pedido.select()
for pedido in pedidos:
    if pedido.nombre_cliente=="Pablo":
        print(pedido.fecha,pedido.monto_total)

#clientes con pedidos con un monto superior a 100
clientes_monto= Cliente.select().where(Cliente.monto_superior>100)
for cliente in clientes_monto:
    print(Cliente.nombre)

#todos los pedidos
for pedido in pedidos:
    print(pedido.fecha,pedido.monto_total,pedido.nombre_cliente)

#actualizar direccion de un cliente
print("Antes de la modificacion")
cliente_editado="Manuel"
clientes=Cliente.select().where(Cliente.nombre=="Manuel")
for cliente in clientes:
    print(Cliente.nombre,Cliente.email,Cliente.direccion)

cliente_modificacion= Cliente.update(direccion="Barriada 123").where(Cliente.nombre == "Manuel")
print("Despues de la modificacion")
for cliente in cliente_modificacion:
    print(Cliente.nombre,Cliente.email,Cliente.direccion)



#incrementar el monto de todos los pedidos antes de una fecha especifica
fecha="06-06-2024"
incremento=200
print("Antes del incremento")

print("Despues del incremento")



#elimina un cliente y sus pedidos(on delete cascade)

#elimina todos los pedidos cuyo monto sea inferior a 50
