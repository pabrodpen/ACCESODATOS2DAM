
#### Ejemplo
class FileHandler:
    def read_file(self, file_path, mode='r'):
        try:
            with open(file_path, mode) as f:
                content = f.read()
                return content
        except Exception as e:
            print(f"Error leyendo el archivo: {e}")
            
    def write_file(self, file_path, content, mode='w'):
        try:
            with open(file_path, mode) as f:
                f.write(content)
        except Exception as e:
            print(f"Error escribiendo en el archivo: {e}")

file_handler=FileHandler()
contenido="29/08/2002"
ruta="78137123.txt"
file_handler.write_file(ruta,contenido)
contenidoLeido=file_handler.read_file(ruta)
print("Contenido del fichero", ruta,":",contenidoLeido)
