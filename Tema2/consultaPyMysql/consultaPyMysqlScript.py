import pymysql 
import time
start_time = time.time()
#Hacemos operaciones

host = 'localhost' 
user = 'usuario'       
password = 'usuario'  
database = '1dam'  

try:
    conexion = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    print("Conexión a la base de datos exitosa")

    
    cursor = conexion.cursor()
    query = """
    SELECT * FROM Plantas
    """            
    cursor.execute(query)
    # Recuperar y mostrar los resultados
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)


except pymysql.MySQLError as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar la conexión
    if 'conexion' in locals() and conexion:
        conexion.close()
        print("Conexión cerrada")

end_time = time.time()
print(f"Tiempo de inserción con PyMySQL: {end_time - start_time} segundos")