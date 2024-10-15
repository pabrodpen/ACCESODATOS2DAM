import pymysql
import time

start_time = time.time()


# Datos de conexión
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


  
    cursor.execute("DELETE FROM Plantas WHERE nombre = %s", ('Rosa'))
    conexion.commit()
    print(cursor.rowcount, "registro(s) actualizado(s)")



    

except pymysql.MySQLError as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar la conexión
    if 'conexion' in locals() and conexion:
        conexion.close()
        print("Conexión cerrada")

end_time = time.time()
print(f"Tiempo de creacion y modificacion con PyMySQL: {end_time - start_time} segundos")