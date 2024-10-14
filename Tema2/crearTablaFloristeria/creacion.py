import pymysql
import time
import random

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


    # Construcción y ejecución de la consulta SQL
    query = """
    CREATE TABLE Floristerias( nombre VARCHAR(30) PRIMARY KEY, direccion VARCHAR(30), 
    telefono VARCHAR(30));
    """        
    cursor.execute(query)


    query = """
    ALTER TABLE Plantas ADD floristeria_id VARCHAR(30),ADD CONSTRAINT fk_floristeria 
    FOREIGN KEY (floristeria_id) REFERENCES Plantas(nombre);
    """        
    cursor.execute(query)

    print("RELACION ENTRE LAS TABLAS COMPLETADA")
    

    

except pymysql.MySQLError as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar la conexión
    if 'conexion' in locals() and conexion:
        conexion.close()
        print("Conexión cerrada")

end_time = time.time()
print(f"Tiempo de creacion y modificacion con PyMySQL: {end_time - start_time} segundos")