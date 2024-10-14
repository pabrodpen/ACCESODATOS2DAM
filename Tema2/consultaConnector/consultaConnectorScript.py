import mysql.connector 
import time
start_time = time.time()
#Hacemos operaciones

from mysql.connector import Error
try:
    conexion = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='1dam'
    )
    if conexion.is_connected():
        print("Conexion exitosa")
        cursor = conexion.cursor()
        query = """
        SELECT * FROM Plantas
        """            
        cursor.execute(query)
         # Recuperar y mostrar los resultados
        resultados = cursor.fetchall()
        for fila in resultados:
            print(fila)


except Error as e:
    print(f"Error de conexión: {e}")
finally:
    if conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")

        
end_time = time.time()
print(f"Tiempo de inserción con mysql-connector: {end_time - start_time} segundos")