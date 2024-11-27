#Clases Definidas
#    Producto:
#        Atributos: nombre, precio, cantidad, id_proveedor.
#        Relación con Proveedor mediante id_proveedor.
 #   Proveedor:
#        Atributos: nombre, telefono, direccion.
    #Almacena una lista de categorías de productos simples, como: ["Herramientas", "Electrónica", "Muebles"].
   # Modifica esta lista para añadir nuevas categorías relacionadas con los productos.

#Gestión de Objetos Estructurados:

 #   Relaciona los productos con una categoría de la lista lista_categorias, añadiendo un nuevo atributo categoria en la clase Producto.
#Persistencia
#    Almacenar al menos tres proveedores y diez productos relacionados.
#Consultas
#    Encuentra todos los productos suministrados por un proveedor específico. listando su nombre y categoria
#    Filtra los productos cuyo precio sea mayor a 50.
#   Consulta los productos agrupados por categorías de la lista lista_categorias.
#Modificaciones
#    Cambia el precio de un producto específico.
#   Incrementyar el rprecio de los produtos deuna categoria.
#Eliminaciones
#    Elimina un proveedor y actualiza los productos relacionados para que tengan un id_proveedor vacío.
#    Al eliminar un rol (nuevo requerimiento), asigna un rol predeterminado a los usuarios relacionados.
#Al eliminar una categoría de lista_categorias, actualiza los productos relacionados para que su categoría quede en None (sin categoría).
#Validación de Teléfono
#    Implementa una función que verifique si un teléfono ya está registrado antes de almacenar un nuevo proveedor.
#Transacciones y Rollbacks
#    Realiza una transacción donde se actualicen:
#        Dos productos.
#        Un proveedor.
#    Realiza un rollback en caso de error.
import ZODB,ZODB.FileStorage,transaction
from persistent import Persistent
storage = ZODB.FileStorage.FileStorage('tienda.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

class Producto(Persistent):
    def__init__(self,nombre,precio,cantidad,categoria,id_proveedor):
        self.nombre=nombre
        self.precio=precio
        self.cantidad=cantidad
        self.categoria=categoria
        self.id_proveedor=id_proveedor

class Proveedor(Persistent):
    def__init__(self,nombre,telefono,direccion):
        self.nombre=nombre
        self.telefono=telefono
        self.direccion=direccion
    

# Verificar y crear colecciones en root si no existen
    if "productos" not in root:
        root["plantas"] = {}

    if "categorias_productos" not in root:
        root["categorias_productos"] = {}

    if "proveedores" not in root:
        root["proveedores"]={}
    
    # Almacenar una lista simple en la base de datos
    root["categorias_productos"] = ["Herramientas", "Electronica", "Muebles","Juguetes"]

    root["proveedores"][1]=Proveedor("Proveedor 1",122345,"Calle 123")
    root["proveedores"][2]=Proveedor("Proveedor 2",467881,"Calle 456")
    root["proveedores"][3]=Proveedor("Proveedor 3",973246,"Av Sol")

    root["productos"]["Pala"]=Producto("Pala",23,21,"Herramientas",1)
    root["productos"]["Ordenador"]=Producto("Ordenador",200,30,"Electronica",3)
    root["productos"]["Mesa"]=Producto("Mesa",70,15,"Muebles",2)
    root["productos"]["Martillo"]=Producto("Martillo",15,11,"Herramientas",1)
    root["productos"]["Tablet"]=Producto("Tablet",80,14,"Electronica",2)
    root["productos"]["Balon"]=Producto("Balon",18,31,"Juguetes",3)
    root["productos"]["Carretilla"]=Producto("Carretilla",53,5,"Herramientas",1)
    root["productos"]["Movil"]=Producto("Movil",103,7,"Electronica",3)
    root["productos"]["Muñeca"]=Producto("Muñeca",10,40,"Juguetes",2)
    root["productos"]["Tijeras"]=Producto("Tijeras",20,30,"Herramientas",1)

    transaction.commit()
    print("Transaccion completada")

try:

    print("todos los productos suministrados por el proveedor 2. listando su nombre y categoria")
    #clave-valor
    for(nombre,producto) in root["productos"].items():
        if producto.id_proveedor == 2:
            print(f"Nombre: {producto.nombre}, Categoria: {producto.categoria}")
           
    print("Filtra los productos cuyo precio sea mayor a 50")
    for(nombre,producto) in root["productos"].items():
        if producto.precio > 50:
            print(f"Nombre: {producto.nombre}, Precio: {producto.precio}, Cantidad: {producto.cantidad},
                   Categoria: {producto.categoria}, ID Proceedor: {producto.id_proveedor}")
            
    print("Consulta los productos agrupados por categorías de la lista lista_categorias")
    for(categoria) in root["categorias_productos"]:
        print("Productos de {categoria}")
        for(nombre,producto) in root["productos"].items():
            if(producto.categoria==categoria):
                print(f"Nombre:{producto.nombre}")

    print("Cambia el precio de un producto específico")
    nuevoPrecio=100
    nombreProducto="Balon"
    print(f"Nombre: {producto.nombre}, Precio: {producto.precio}")
    producto=root.get[nombreProducto]
    producto.precio=nuevoPrecio
    print(f"Nombre: {producto.nombre}, Precio: {producto.precio}")


    print("Incrementar el precio de los productos de la Categoria Electronica")
    incremento=200
    print("Productos electronicos antes de la modificacion")
    for(nombre,producto) in root["productos"].items():
        if(producto.categoria==categoria):
            print(f"Nombre:{producto.nombre}, Precio:{producto.precio}")

    for(nombre,producto) in root["productos"].items():
        if(producto.categoria==categoria):
            producto.precio+=incremento

    print("Productos electronicos despues de la modificacion")
    for(nombre,producto) in root["productos"].items():
        if(producto.categoria==categoria):
            print(f"Nombre:{producto.nombre}, Precio:{producto.precio}")



    print("Elimina un proveedor y actualiza los productos relacionados para que tengan un id_proveedor vacío")
    proveedorEliminado=3
    root["proveedores"].remove(proveedorEliminado)
    for(nombre,producto)

#    Al eliminar un rol (nuevo requerimiento), asigna un rol predeterminado a los usuarios relacionados.
#Al eliminar una categoría de lista_categorias, actualiza los productos relacionados para que su categoría quede en None (sin categoría).

except Exception as e:
    transaction.abort
    print("Error durante la transaccion: {e}")

finally:
    connection.close()
    db.close()
    print("Conexion cerrada")