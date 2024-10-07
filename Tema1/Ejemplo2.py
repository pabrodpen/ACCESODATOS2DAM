#### Ejemplo Práctico: Leer un archivo JSON
import json
class JSONFileHandler:
    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo JSON: {e}")
                
# Uso
json_handler = JSONFileHandler()
data = json_handler.read_json('data.json')
print(data)
