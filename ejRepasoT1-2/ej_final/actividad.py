import pymysql
import csv
import json
host = 'localhost' 
user = 'root'       
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

    #creamos tabla

    cursor.execute("DROP TABLE IF EXISTS empleados;")
    cursor.execute("DROP TABLE IF EXISTS departamentos;")
    conexion.commit()
          
   # Crear tabla Departamentos primero
    cursor.execute('''CREATE TABLE departamentos(
                        ID INT PRIMARY KEY, 
                        Nombre VARCHAR(30)
                      );''')

    # Crear tabla Empleados después, con clave externa a Departamentos
    cursor.execute('''CREATE TABLE empleados(
                        ID INT PRIMARY KEY,
                        Nombre VARCHAR(30), 
                        Edad INT,
                        Salario FLOAT,
                        DepartamentoID INT,
                        CONSTRAINT fk_departamento
                        FOREIGN KEY (DepartamentoID) REFERENCES departamentos(ID)
                      );''')




    #cogemos los datos de los csv
    with open('departamentos.csv',encoding='utf-8',mode='r') as f:
        reader=csv.DictReader(f)
        #no hace falta que hagamos el list xq no lo convertimos en dicc
        for filas in reader:
            cursor.execute('''INSERT INTO departamentos(ID, Nombre) VALUES
                           (%s,%s)''',(filas['ID'],filas['Nombre']))

        conexion.commit()

     #cogemos los datos de los csv
    with open('empleados.csv',encoding='utf-8',mode='r') as f:
        reader=csv.DictReader(f)
        #no hace falta que hagamos el list xq no lo convertimos en dicc
        for filas in reader:
            cursor.execute('''INSERT INTO empleados(ID, Nombre,Edad, Salario, DepartamentoID) VALUES
                           (%s,%s,%s,%s,%s)''',(filas['ID'],filas['Nombre'],filas['Edad'],filas['Salario'],
                                                filas['DepartamentoID']))
            
        conexion.commit()

    #todos los empleados y departamentos


    print("\nEMPLEADOS")
    cursor.execute('''SELECT * FROM empleados;''')

    resultadosEmpleados=cursor.fetchall()
    for empleado in resultadosEmpleados:
        print(empleado)

    print("\nDEPARTAMENTOS")
    cursor.execute('''SELECT * FROM departamentos;''')

    resultadosDptos=cursor.fetchall()
    for departamento in resultadosDptos:
        print(departamento)

    # escribir en el json los empleados del Departamento 3
    departamentoID=3
    cursor.execute('''SELECT * FROM empleados WHERE DepartamentoID=%s;''',(departamentoID,))

    #los cursores nos devuelven una lista de tuplas, mientras que los JSON en listas 
    # de diccionarios
    empleadosConDpto=cursor.fetchall()

    # 2. Convertir las tuplas en diccionarios
    empleados_lista = []
    for empleado in empleadosConDpto:
        empleados_lista.append({
            "ID": empleado[0],
            "Nombre": empleado[1],
            "Edad": empleado[2],
            "Salario": empleado[3],
            "DepartamentoID": empleado[4]
    })
        
    #escribimos los dicc en el json

    with open('salida.json',encoding='utf-8',mode='w') as f:
        json.dump(empleados_lista,f,ensure_ascii='False',indent=4)

    #leer el json y mostrarlos
    print("\nEMPLEADOS DEL DEPARTAMENTO 3")
   

    with open('salida.json',encoding='utf-8',mode='r') as f:
        reader=json.load(f)
        for empleado in reader:
            print(empleado)

except pymysql.MySQLError as e:
    print(e)