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
cursor.execute("""
INSERT INTO Plantas (nombre, familia, tamaño, clima, tipo_suelo) VALUES
('Tulipán', 'Liliaceae', 'Mediana', 'Templado', 'Franco'),
('Ficus', 'Moraceae', 'Grande', 'Tropical', 'Arcilloso');


# Confirmar los cambios
conexion.commit()

# Realizar una consulta para recuperar los datos
cursor.execute("SELECT * FROM alumnos")

# Imprimir todos los registros
for fila in cursor.fetchall():
    print(fila)

# Cerrar la conexión
conexion.close()

