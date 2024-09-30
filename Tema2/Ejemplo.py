#### Ejemplo Práctico
from pathlib import Path
class FileManager:
    def __init__(self, path):
        self.path = Path(path)
        
    def create_directory(self):
        if not self.path.exists():
            self.path.mkdir()
            print(f'Directorio {self.path} creado.')
        
        else:
            print(f'El directorio {self.path} ya existe.')
        
    def list_files(self):
        if self.path.exists() and self.path.is_dir():
            return list(self.path.iterdir())
        return []
    
    def delete_directory(self):
        if self.path.exists() and self.path.is_dir():
            self.path.rmdir()
            print(f'Directorio {self.path} eliminado.')
# Uso
file_manager = FileManager('test_directory')
file_manager.create_directory()


print(file_manager.list_files())
file_manager.delete_directory()
