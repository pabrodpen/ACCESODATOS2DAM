import pymysql

# Datos de conexión
host = 'localhost' 
user = 'usuario'       
password = 'usuario'  
database = '1dam'  

try:
    # Crear la conexión
    conexion = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Conexión a la base de datos exitosa")

    # Realizar alguna operación, como consultar la versión de MySQL
    with conexion.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Versión de MySQL: {version[0]}")

except pymysql.MySQLError as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar la conexión
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")

