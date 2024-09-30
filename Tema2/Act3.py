import json
class JSONFileHandler:
    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo JSON: {e}")

    def write_json(self,file_path,content):
        try:
            with open(file_path,'w') as f:
                json.dump(content,f)
        except Exception as e:
            print(f"Error escribiendo JSON: {e}")
                
# Uso
json_handler = JSONFileHandler()
data={'DNI' : '78137123M', 'Fecha_Nac' : '29/08/2002'}
ruta="DatosAct3.json"
json_handler.write_json(ruta,data)

#comprobamos leyendo de nuevo el json
print(json_handler.read_json(ruta))


