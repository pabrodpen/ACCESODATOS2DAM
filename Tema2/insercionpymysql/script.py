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

    familia = ['Asteraceae', 'Oleaceae', 'Rosaceae', 'Poaceae']
    tamaño = ['Pequeña', 'Mediana', 'Grande']
    clima = ['Tropical', 'Mediterráneo', 'Desértico', 'Árido']
    tipo_suelo = ['Arenoso', 'Arcilloso', 'Franco', 'Rocoso']

    cursor = conexion.cursor()

    for i in range(10000):
        nombreV = f"Planta {i + 1}"
        familiaV = random.choice(familia)
        tamañoV = random.choice(tamaño)
        climaV = random.choice(clima)
        tipo_sueloV = random.choice(tipo_suelo)

        # Construcción y ejecución de la consulta SQL
        query = """
        INSERT INTO Plantas (nombre, familia, tamaño, clima, tipo_suelo)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombreV, familiaV, tamañoV, climaV, tipo_sueloV)
        
        cursor.execute(query, valores)

    # Confirmar cambios en la base de datos
    conexion.commit()

except pymysql.MySQLError as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar la conexión
    if 'conexion' in locals() and conexion:
        conexion.close()
        print("Conexión cerrada")

end_time = time.time()
print(f"Tiempo de inserción con PyMySQL: {end_time - start_time} segundos")
