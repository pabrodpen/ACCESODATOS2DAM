import mysql.connector
from mysql.connector import Error

# Conexión a la base de datos MySQL usando el conector oficial
conexion = None
try:
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="usuario",  # tu usuario MySQL
        password="usuario",  # tu contraseña MySQL
        database="1dam",  # la base de datos donde está la tabla Herramientas
        auth_plugin="mysql_native_password"
    )
    if conexion.is_connected():
        # Crear un cursor
        cursor = conexion.cursor()
        
        # Iniciar la transacción
        print("Iniciando transacción...")
        
        # Insertar un nuevo registro en la tabla Herramientas
        sql_insert = """
        INSERT INTO Plantas (nombre, familia, tamaño, clima, tipo_suelo)
        VALUES (%s, %s, %s, %s, %s)
        """
        datos = (None, "T", "Pequeña", "Mediterráneo",'Arcilloso')#int en el campo familia
        cursor.execute(sql_insert, datos)
        
        # Hacer commit si todo va bien
        conexion.commit()
        print("Transacción exitosa: Registro insertado correctamente.")

except Error as e:
    # Si ocurre un error, hacer rollback
    print(f"Error en la transacción: {e}")
    if conexion:
        conexion.rollback()
        print("Se realizó rollback.")
        
finally:
    # Cerrar el cursor y la conexión si están abiertos
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")
