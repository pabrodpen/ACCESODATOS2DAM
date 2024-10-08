import sqlite3

import mysql.connector
# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
host="localhost", # Cambia esto si tu base de datos está en otro servidor
user="usuario", # Tu usuario de MySQL
password="usuario", # Tu contraseña de MySQL
database="1dam" # Asegúrate de que la base de datos exista
)
cursor = conexion.cursor()

# Conexión a la base de datos SQLite (si no existe, se crea)
conexion = sqlite3.connect('datos.db')

# Crear el cursor
cursor = conexion.cursor()


# Insertar datos en la tabla
cursor.execute("""
INSERT INTO alumnos (nombre, edad) VALUES
    ('Juan', 20),
    ('Ana', 18)
""")

# Confirmar los cambios
conexion.commit()

# Realizar una consulta para recuperar los datos
cursor.execute("SELECT * FROM alumnos")

# Imprimir todos los registros
for fila in cursor.fetchall():
    print(fila)

# Cerrar la conexión
conexion.close()

