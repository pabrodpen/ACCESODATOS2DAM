from peewee import MySQLDatabase, Model, CharField, DateField, DoubleField, ForeignKeyField
import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent

# ==================== PARTE 1: GESTIÓN CON PEEWEE ====================
# Conexión a la base de datos MySQL
db = MySQLDatabase(
    "1dam",
    user="root",
    password="usuario",
    host="localhost",
    port=3306,
)

db.connect()

# Modelos
class Cliente(Model):
    nombre = CharField(unique=True)
    email = CharField()
    direccion = CharField()

    class Meta:
        database = db

class Pedido(Model):
    fecha = DateField()
    monto_total = DoubleField()
    cliente = ForeignKeyField(
        Cliente,
        backref="pedidos",
        on_delete="CASCADE",
        constraint_name="fk_pedido_cliente"  # Nombre personalizado
    )

    class Meta:
        database = db

# Eliminar tablas si ya existen y recrearlas
db.drop_tables([Pedido, Cliente], safe=True)
db.create_tables([Cliente, Pedido], safe=True)

# Insertar datos iniciales
Cliente.create(nombre="Juan", email="juan@gmail.com", direccion="Calle 123")
Cliente.create(nombre="Maria", email="maria@gmail.com", direccion="Avenida 456")
Cliente.create(nombre="Pablo", email="pablo@gmail.com", direccion="Plaza 789")
Cliente.create(nombre="Carlos", email="pablo@gmail.com", direccion="sffg")


Pedido.create(fecha="2024-01-01", monto_total=300, cliente=Cliente.get(Cliente.nombre == "Juan"))
Pedido.create(fecha="2024-02-01", monto_total=400, cliente=Cliente.get(Cliente.nombre == "Maria"))
Pedido.create(fecha="2024-03-01", monto_total=150, cliente=Cliente.get(Cliente.nombre == "Pablo"))
Pedido.create(fecha="2024-03-01", monto_total=250, cliente=Cliente.get(Cliente.nombre == "Juan"))

# Consultar pedidos de un cliente
pedidos = Pedido.select().join(Cliente).where(Cliente.nombre == "Maria")
print("\nPedidos de Maria:")
for pedido in pedidos:
    print(f"Fecha: {pedido.fecha}, Monto Total: {pedido.monto_total}")

# Incrementar monto de pedidos antes de una fecha específica
Pedido.update(monto_total=Pedido.monto_total + 100).where(Pedido.fecha < "2024-02-01").execute()

print("\nPedidos después del incremento:")
for pedido in Pedido.select():
    print(f"Fecha: {pedido.fecha}, Monto Total: {pedido.monto_total}")

# ==================== PARTE 2: GESTIÓN CON ZODB ====================
# Clases para ZODB
class Producto(Persistent):
    def __init__(self, nombre, precio, categoria, id_proveedor):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.id_proveedor = id_proveedor

class Proveedor(Persistent):
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

# Conexión a ZODB
storage = ZODB.FileStorage.FileStorage('tienda.fs')
zodb_db = ZODB.DB(storage)
connection = zodb_db.open()
root = connection.root()

# Verificar y crear colecciones
if "productos" not in root:
    root["productos"] = {}
if "proveedores" not in root:
    root["proveedores"] = {}

# Insertar datos iniciales
root["proveedores"][1] = Proveedor("Proveedor A", 123456, "Calle 123")
root["proveedores"][2] = Proveedor("Proveedor B", 789012, "Avenida 456")

root["productos"]["Martillo"] = Producto("Martillo", 50, "Herramientas", 1)
root["productos"]["Sierra"] = Producto("Sierra", 100, "Herramientas", 2)
root["productos"]["Taladro"] = Producto("Taladro", 200, "Electrónica", 1)

transaction.commit()
print("\nProductos iniciales en ZODB:")
for nombre, producto in root["productos"].items():
    print(f"Nombre: {producto.nombre}, Precio: {producto.precio}, Categoría: {producto.categoria}")

# Incrementar precios de una categoría
categoria_a_incrementar = "Herramientas"
for nombre, producto in root["productos"].items():
    if producto.categoria == categoria_a_incrementar:
        producto.precio += 50

transaction.commit()
print("\nProductos después del incremento de precios en 'Herramientas':")
for nombre, producto in root["productos"].items():
    print(f"Nombre: {producto.nombre}, Precio: {producto.precio}, Categoría: {producto.categoria}")
# ==================== PARTE 3: CONSULTAS CRUZADAS ====================
# Consultar pedidos de Peewee y listar productos relacionados de ZODB
#Vamos a mostrar los pedidos hechos por Maria, y a su vez, por cada pedido
#vamos a mostrar los productos que vienen deñ proveedor 2
pedidos_cliente = Pedido.select().join(Cliente).where(Cliente.nombre == "Maria")
print("\nPedidos de Maria y productos relacionados:")
for pedido in pedidos_cliente:
    print(f"Pedido: {pedido.fecha}, Monto Total: {pedido.monto_total}")
    for nombre, producto in root["productos"].items():
        if producto.id_proveedor == 2:  # Proveedor B
            print(f" - Producto relacionado: {producto.nombre}, Precio: {producto.precio}")


#Objetivo: Obtener la lista de clientes que han realizado pedidos y, para cada cliente:

#Mostrar el total acumulado de sus pedidos.
#Listar los productos relacionados suministrados por los proveedores que coincidan
#en direccion con el cliente

#primero obtenemos con peewee los clientes que han realizado pedidos
#ponemos distinct ya que, si un cliente tiene varios pedidos(Juan), saldra mas de une vez
clientes_con_pedidos=Cliente.select().join(Pedido).where(Pedido.cliente!=None).distinct()
for cliente in clientes_con_pedidos:
    print(f"Datos de {cliente.nombre}")
    total=0
    pedidos_cliente=Pedido.select().where(Pedido.cliente==cliente)
    for pedido in pedidos_cliente:
        total+=pedido.monto_total
    print(f"\nTotal acumulado de pedidos:{total}")
    print("\nProductos de proveedores con la misma direccion")
    #cogemos los productos con ZODB
    for(nombre,producto) in root["productos"].items():
        proveedorID=producto.id_proveedor
        proveedor=root["proveedores"].get(proveedorID)
        if proveedor.direccion==cliente.direccion:
            print(f"Nombre: {producto.nombre}, Proveedor: {proveedor.nombre}")

# ==================== FINALIZACIÓN ====================
# Cerrar conexiones
connection.close()
zodb_db.close()
db.close()
print("\nConexiones cerradas.")
