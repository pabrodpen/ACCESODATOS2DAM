# Implementar componentes reutilizables:
import logging
import pymongo
from pymongo import MongoClient, errors
import json
import sqlite3
# Desarrolla un componente en Python para la conexión a MongoDB (deberá manejar credenciales y 
# controlar excepciones).
# Crea un componente para realizar consultas genéricas a la base de datos. Este componente debe 
# admitir condiciones dinámicas.
# CRUD sobre la base de datos:
# Componente para CRUD y gestión de colecciones
# Desarrolla un componente que permita:
# Añadir documentos representando libros. Cada libro debe tener un título, autor, género, y un campo opcional como "resumen".
# Modificar la información de un libro específico (por ejemplo, cambiar el resumen o actualizar el género).
# Eliminar libros de la base de datos según condiciones específicas (por ejemplo, todos los libros de un género dado).
# Consultar libros con filtros dinámicos y una proyección que solo muestre ciertos campos (por ejemplo, título y autor).
# Gestión de colecciones:

# Implementa un componente que permita crear y eliminar colecciones.
# Mapeo objeto-relacional:

# Diseña un modelo de clase para representar libros en Python y transforma los documentos de MongoDB a instancias de esta clase utilizando un componente específico.
# Pruebas y documentación:

# Prueba todos los componentes y documenta los resultados. Asegúrate de manejar errores de conexión, operaciones fallidas, y mostrar mensajes adecuados al usuario.
# Escribe un manual breve para explicar cómo integrar estos componentes en otras aplicaciones.
# Componente para gestionar información almacenada en ficheros

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def leer_fichero(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                logging.info(f"Datos leídos del fichero {self.file_path}")
                return data
        except FileNotFoundError:
            logging.error(f"El fichero {self.file_path} no existe.")
            return None
        except json.JSONDecodeError:
            logging.error(f"Error al decodificar el fichero {self.file_path}.")
            return None

    def escribir_fichero(self, data):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)
                logging.info(f"Datos escritos en el fichero {self.file_path}")
        except Exception as e:
            logging.error(f"Error al escribir en el fichero {self.file_path}: {e}")

# Componente para gestionar información en bases de datos objeto-relacionales y orientadas a objetos

class SQLiteManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            logging.info(f"Conexión a SQLite en {self.db_path} establecida.")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a SQLite: {e}")

    def desconectar(self):
        if hasattr(self, 'conn'):
            self.conn.close()
            logging.info("Conexión a SQLite cerrada.")

    def crear_tabla_libros(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    titulo TEXT NOT NULL,
                                    autor TEXT NOT NULL,
                                    genero TEXT NOT NULL,
                                    resumen TEXT)''')
            self.conn.commit()
            logging.info("Tabla 'libros' creada en SQLite.")
        except sqlite3.Error as e:
            logging.error(f"Error al crear la tabla 'libros': {e}")

    def insertar_libro(self, libro):
        try:
            self.cursor.execute('''INSERT INTO libros (titulo, autor, genero, resumen)
                                   VALUES (?, ?, ?, ?)''', (libro.titulo, libro.autor, libro.genero, libro.resumen))
            self.conn.commit()
            logging.info(f"Libro '{libro.titulo}' insertado en SQLite.")
        except sqlite3.Error as e:
            logging.error(f"Error al insertar el libro en SQLite: {e}")

    def consultar_libros(self):
        try:
            self.cursor.execute("SELECT titulo, autor FROM libros")
            libros = self.cursor.fetchall()
            logging.info("Consulta de libros en SQLite realizada exitosamente.")
            return libros
        except sqlite3.Error as e:
            logging.error(f"Error al consultar libros en SQLite: {e}")
            return []

# Componente para gestionar información en una base de datos documental nativa
# (ya implementado en el código original con MongoDB)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log_biblioteca.log"), logging.StreamHandler()],
)
class MongoDBConexion:
    def __init__(self,usuario,clave,base_datos,host,puerto):
        self.usuario = usuario
        self.clave = clave
        self.base_datos = base_datos
        self.host = host
        self.puerto = puerto
    def conectar(self):

        try:
            # Intentar conectarse al servidor MongoDB
            self.client = MongoClient(
                f"mongodb://{self.usuario}:{self.clave}@{self.host}:{self.puerto}/{self.base_datos}",
                serverSelectionTimeoutMS=5000,
            )

            # Seleccionar la base de datos
            db = self.client[self.base_datos]

            # Eliminar la colección "Productos" si existe
            if "Libros" in db.list_collection_names():
                db.Productos.drop()
                print("Colección 'Libros' eliminada.")
            logging.info("Conexión exitosa")
        except errors.ServerSelectionTimeoutError as err:
            # Este error ocurre si el servidor no está disponible o no se puede conectar
            print(f"No se pudo conectar a MongoDB: {err}")
            logging.error(f"No se pudo conectar a MongoDB: {err}")
        except errors.OperationFailure as err:
            # Este error ocurre si las credenciales son incorrectas o no se tienen los permisos necesarios
            print(f"Fallo en la autenticación o permisos insuficientes: {err}")
            logging.error(f"Fallo en la autenticación o permisos insuficientes: {err}")
        except Exception as err:
            # Manejar cualquier otro error inesperado
            print(f"Ocurrió un error inesperado: {err}")
            logging.error(f"Ocurrió un error inesperado: {err}")
        
    def desconectar(self):
        if hasattr(self, 'client'):
            self.client.close()
            logging.info("Conexión a MongoDB cerrada.")


class BibliotecaManager:
    def __init__(self, db):
        self.db = db

    def crear_coleccion(self, nombre_coleccion):
        try:
            self.db.create_collection(nombre_coleccion)
            logging.info(f"Colección '{nombre_coleccion}' creada exitosamente.")
        except errors.CollectionInvalid:
            logging.warning(f"La colección '{nombre_coleccion}' ya existe.")

    def eliminar_coleccion(self, nombre_coleccion):
        if nombre_coleccion in self.db.list_collection_names():
            self.db.drop_collection(nombre_coleccion)
            logging.info(f"Colección '{nombre_coleccion}' eliminada.")
        else:
            logging.warning(f"La colección '{nombre_coleccion}' no existe.")

    def insertar_libro(self, coleccion, libro):
        try:
            result = self.db[coleccion].insert_one(libro)
            logging.info(f"Libro insertado con ID: {result.inserted_id}")
        except Exception as e:
            logging.error(f"Error al insertar el libro: {e}")
    
    def eliminar_libro(self, coleccion, titulo):
        try:
            result = self.db[coleccion].delete_one({"titulo": titulo})
            if result.deleted_count > 0:
                logging.info(f"Libro '{titulo}' eliminado.")
            else:
                logging.warning("No se encontró un libro con ese título.")
        except Exception as e:
            logging.error(f"Error al eliminar el libro: {e}")

    def consultar_libros(self, coleccion, filtro=None, proyeccion=None):
        try:
            filtro = filtro or {}
            libros = self.db[coleccion].find(filtro, proyeccion)
            logging.info("Consulta realizada exitosamente.")
            return list(libros)
        except Exception as e:
            logging.error(f"Error al consultar libros: {e}")
            return []

    def actualizar_libro(self, coleccion, filtro, actualizacion):
        try:
            result = self.db[coleccion].update_one(filtro, {"$set": actualizacion})
            if result.modified_count > 0:
                logging.info("Libro actualizado exitosamente.")
            else:
                logging.warning("No se encontró un libro que coincida con el filtro.")
        except Exception as e:
            logging.error(f"Error al actualizar el libro: {e}")

    def eliminar_libros(self, coleccion, filtro):
        try:
            result = self.db[coleccion].delete_many(filtro)
            logging.info(f"{result.deleted_count} libros eliminados.")
        except Exception as e:
            logging.error(f"Error al eliminar libros: {e}")


# Componente para mapeo objeto-relacional
class Libro:
    def __init__(self, titulo, autor, genero, resumen=None):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.resumen = resumen

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "resumen": self.resumen,
        }
# Pruebas e integración de los componentes
if __name__ == "__main__":
    # Conexión a MongoDB
    # def __init__(self,usuario,clave,base_datos,host,puerto):
    conexion = MongoDBConexion("usuario","usuario","1dam","localhost",27017)
    conexion.conectar()
    db = MongoClient("localhost", 27017)["1dam"]

    # Gestión de la colección
    manager = BibliotecaManager(db)
    coleccion = "libros"
    manager.crear_coleccion(coleccion)

    # Insertar libros
    libro1 = Libro("1984", "George Orwell", "Distopía", "Una novela sobre un régimen totalitario.")
    libro2 = Libro("Cien años de soledad", "Gabriel García Márquez", "Realismo mágico")
    libro3 = Libro("El principito", "Antoine de Saint-Exupéry", "Fábula", "Un niño que vive en un asteroide.")
    
    manager.insertar_libro(coleccion, libro1.to_dict())
    manager.insertar_libro(coleccion, libro2.to_dict())
    manager.insertar_libro(coleccion, libro3.to_dict())

    # Consultar libros
    libros = manager.consultar_libros(coleccion, proyeccion={"_id": 0, "titulo": 1, "autor": 1})
    print("Libros en la colección:")
    for libro in libros:
        print(libro)

    # Actualizar un libro
    manager.actualizar_libro(coleccion, {"titulo": "1984"}, {"resumen": "Actualización del resumen."})

    # Eliminar libros por género
    manager.eliminar_libros(coleccion, {"genero": "Realismo mágico"})

    # Verificar cambios
    libros_actualizados = manager.consultar_libros(coleccion)
    print("Libros después de las operaciones:")
    for libro in libros_actualizados:
        print(libro)

    # Eliminar colección
    manager.eliminar_coleccion(coleccion)

    # Cerrar conexión
    conexion.desconectar()


