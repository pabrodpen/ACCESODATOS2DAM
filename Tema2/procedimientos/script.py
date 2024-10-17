import mysql.connector
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
        
        #Llamar al procedimiento almacenado
        cursor.callproc("procedimiento")
        #Obtener los múltiples conjuntos de resultados
        for resultado in cursor.stored_results():
            datos = resultado.fetchall() # Recuperar todas las filas del conjunto actual
            print(datos)

except Error as e:
    # Si ocurre un error, hacer rollback
    print(f"Error en el procedimeinto: {e}")
        
finally:
    # Cerrar el cursor y la conexión si están abiertos
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")

        """
        DELIMITER //
        CREATE PROCEDURE numPlantas(String tipoSuelo)
        BEGIN
        SELECT COUNT(*) AS total_Plantas FROM Plantas WHERE tamaño=tipoSuelo;
        SELECT nombre FROM Plantas WHERE tamaño=tipoSuelo;
        END //
        DELIMITER 
        """


        