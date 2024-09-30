# Convertir CSV a JSON
import csv
import json

class FileConverter:
    def csv_to_json(self, csv_file, json_file):
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            with open(json_file, 'w') as f:
                json.dump(rows, f)
                print(f'Conversión de {csv_file} a {json_file} completada.')
        except Exception as e:
            print(f"Error en la conversión: {e}")

    def json_to_csv(self, json_file, csv_file):
        try:
            with open(json_file, 'r') as f:
                reader = json.load(f)

            #cogemos las claves del json
            claves = reader[0].keys()
            with open(csv_file, 'w', newline="") as f:
                # Definir los nombres de las columnas
                writer = csv.DictWriter(f, fieldnames=claves)
                writer.writeheader()
                #escribimos los elementos fila a fila
                for row in reader:
                    writer.writerow(row)
                
        except Exception as e:
            print("Error en la conversion")
            
# Uso
converter = FileConverter()
converter.json_to_csv('data.json', 'data.csv')
