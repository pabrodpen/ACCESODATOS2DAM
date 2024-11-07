#En este caso, vamos a crear un procedimiento llamado total_salario_por_departamento 
# en MySQL que calcule el salario total por cada departamento y guarde el resultado 
# en una tabla temporal.
'''
Paso 1: Crear el Procedimiento Almacenado en MySQL

En este caso, vamos a crear un procedimiento llamado total_salario_por_departamento en MySQL que calcule el salario total por cada departamento y guarde el resultado en una tabla temporal.
SQL para Crear el Procedimiento

DELIMITER $$

CREATE PROCEDURE total_salario_por_departamento()
BEGIN
    -- Crear tabla temporal para almacenar resultados
    CREATE TEMPORARY TABLE IF NOT EXISTS SalarioPorDepartamento (
        DepartamentoID INT,
        NombreDepartamento VARCHAR(30),
        TotalSalario FLOAT
    );

    -- Limpiar la tabla temporal si ya tiene datos
    TRUNCATE TABLE SalarioPorDepartamento;

    -- Calcular el salario total por cada departamento
    INSERT INTO SalarioPorDepartamento (DepartamentoID, NombreDepartamento, TotalSalario)
    SELECT d.ID, d.Nombre, SUM(e.Salario)
    FROM departamentos d
    JOIN empleados e ON d.ID = e.DepartamentoID
    GROUP BY d.ID, d.Nombre;
END $$

DELIMITER ;

    Crear tabla temporal: El procedimiento primero crea una tabla temporal llamada SalarioPorDepartamento que contiene tres columnas: DepartamentoID, NombreDepartamento, y TotalSalario.
    Calcular salarios agregados: Realiza un JOIN entre departamentos y empleados, agrupa por DepartamentoID y Nombre, y calcula el salario total (SUM(e.Salario)) por departamento.
    Guardar el resultado en la tabla temporal: Inserta el resultado en la tabla temporal SalarioPorDepartamento.

Paso 2: Ejecutar el Procedimiento Almacenado en Python y Obtener los Resultados

Ahora, vamos a crear un script en Python que ejecuta el procedimiento y usa stored_results() para obtener los resultados.
Script Python para Llamar al Procedimiento
'''


import pymysql
import json

host = 'localhost' 
user = 'root'       
password = 'usuario'  
database = '1dam'  

try:
    # Conectar a la base de datos
    conexion = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    print("Conexión a la base de datos exitosa")
    cursor = conexion.cursor()

    # Ejecutar el procedimiento almacenado
    cursor.callproc('total_salario_por_departamento')

    # Obtener los resultados desde la tabla temporal
    print("\nSALARIO TOTAL POR DEPARTAMENTO")
    for result in cursor.stored_results():
        salario_departamento = result.fetchall()
        
        # Mostrar resultados y también guardarlos en JSON
        lista_resultados = []
        for departamento in salario_departamento:
            # Convertir a diccionario para un JSON más claro
            departamento_dict = {
                "DepartamentoID": departamento[0],
                "NombreDepartamento": departamento[1],
                "TotalSalario": departamento[2]
            }
            lista_resultados.append(departamento_dict)
            print(departamento_dict)  # Mostrar en pantalla

        # Guardar en JSON
        with open('salario_departamento.json', 'w', encoding='utf-8') as f:
            json.dump(lista_resultados, f, ensure_ascii=False, indent=4)

except pymysql.MySQLError as e:
    print("Error al conectar o ejecutar la consulta:", e)

finally:
    if conexion:
        cursor.close()
        conexion.close()