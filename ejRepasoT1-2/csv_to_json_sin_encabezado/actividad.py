#ID,Nombre,Edad,Departamento,Salario
import csv
import json
class Convertidor():
    def csv_to_json(self,file_csv,file_json,fieldnames):
        try:
            with open(file_csv, encoding='utf-8',mode='r') as f:
                reader=csv.DictReader(f,fieldnames,delimiter=':')
                rows=list(reader)# convierte cada fila del csv en elemento de lista para el json
        #ahora lo escribimos en el json
            with open(file_json,encoding='utf-8' ,mode='w') as f:
                json.dump(rows, f, ensure_ascii=False, indent=4)        
        except Exception as e:
            print("Error en la conversion")
        

convertidor=Convertidor()
columnas=['ID','Nombre','Edad','Departamento','Salario']

rutaEntrada='entrada.csv'
rutaSalida='salida.json'

convertidor.csv_to_json(rutaEntrada,rutaSalida,columnas)
