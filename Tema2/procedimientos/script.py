import pymysql

# Conexión a la base de datos MySQL
conexion = pymysql.connect(
    host="localhost",
    user="usuario",     
    password="usuario",  
    database="1dam"    
)

# Crear el cursor
cursor = conexion.cursor()

# Insertar datos en la tabla
query ='''INSERT INTO Plantas (nombre, familia, tamaño, clima, tipo_suelo) VALUES
('Magnolia', 'Liliaceae', 'Mediana', 'Templado', 'Franco')
'''
cursor.execute(query)


# Confirmar los cambios
conexion.commit()

# Realizar una consulta para recuperar los datos
cursor.execute("SELECT * FROM Plantas")

# Imprimir todos los registros
for fila in cursor.fetchall():
    print(fila)

# Cerrar la conexión
conexion.close()
