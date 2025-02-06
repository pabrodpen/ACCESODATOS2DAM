# Implementa un programa en Python que realice las siguientes tareas:

# Parte 1: Manejo de Archivos con DataManager
# Implementa un componente DataManager que:

# Cree y administre un archivo plantas.json y plantas.csv.
# Permita insertar, leer, actualizar y eliminar registros.
# Controle transacciones (inicio, confirmación, reversión).
# Registre logs de cada operación en log_datos.log.
# Prueba DataManager con JSON y CSV:

# Inserta tres registros de plantas con los atributos:
# nombre, familia, tamaño, clima, tipo_suelo.
# Convierte los datos de JSON a CSV.
# Elimina un registro y verifica los cambios.
# Parte 4: Uso de ZODB con DatabaseManagerObject
# Crea una base de datos orientada a objetos en plantas.fs con los atributos:

# nombre, familia, tamaño, clima, tipo_suelo.
# Implementa operaciones CRUD en ZODB:

# Insertar nuevas plantas.
# Consultar todas las plantas.
# Actualizar el tipo de suelo de una planta.
# Eliminar una planta por su clave.
# Prueba DatabaseManagerObject en ZODB:

# Inserta tres plantas.
# Consulta todas las plantas.
# Modifica el tipo de suelo de una planta.
# Intenta eliminar una planta que no existe.
# Parte 5: Implementación de Logs
# Configura logs para cada operación en los archivos:

# log_datos.log → JSON y CSV.
# log_mysql.log → MySQL.
# log_mongo.log → MongoDB.
# log_zodb.log → ZODB.
# Verifica que cada operación esté registrada en los logs.

# Configuración de logging

#PARTE 1: JSON y CSV

import json
import csv
import logging
import os
from copy import Error, deepcopy
import mysql.connector
from pymongo import MongoClient,PyMongoError
import transaction

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log_datos.log"), logging.StreamHandler()],
)
class DataManager:
    #ESCRIBIR DATO
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.transaccion_activa = False
        self.copia_datos = None
        self.tipo_archivo=self.determinar_tipo_archivo()#amtes de leer el archivo se determina el tipo

    def _determinar_tipo_archivo(self):
        if self.ruta_archivo.endswith(".json"):
            return "json"
        elif self.ruta_archivo.endswith(".csv"):
            return "csv"
        else:
            raise ValueError("Tipo de archivo no soportado.")


        
    def _leer_archivo(self):
        if self.tipo_archivo == "json":
            with open(self.ruta_archivo, "r") as archivo:
                datos=json.load(archivo)
                return datos
        elif self.tipo_archivo == "csv":
            with open(self.ruta_archivo, mode="r") as archivo:
                datos=list(csv.DictReader(archivo))
                return datos
        else:
            raise ValueError("Tipo de archivo no soportado.")

    def _guardar_archivo(self):
        if self.tipo_archivo == "json":
            with open(self.ruta_archivo, "w") as archivo:
                json.dump(self.datos, archivo, indent=4)
        elif self.tipo_archivo == "csv":
            if self.datos:
                with open(self.ruta_archivo, mode="w", newline="") as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=self.datos[0].keys())
                    escritor.writeheader()
                    escritor.writerows(self.datos)
        logging.info(f"Archivo {self.tipo_archivo.upper()} guardado.")

    def iniciar_transaccion(self):
        self.transaccion_activa = True
        self.copia_datos = deepcopy(self.datos)
        logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        self.transaccion_activa = False
        self.copia_datos = None
        self._guardar_archivo()
        logging.info("Transacción confirmada.")

    def revertir_transaccion(self):
        self.datos = self.copia_datos
        self.transaccion_activa = False
        self.copia_datos = None
        logging.warning("Transacción revertida.")

    def eliminar_dato(self, clave, valor):
        """Elimina un registro basado en un valor de clave"""
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de eliminar datos.")
        self.datos = [dato for dato in self.datos if dato.get(clave) != valor]
        logging.info(f"Registro eliminado donde {clave} = {valor}")

    #data_json.eliminar_dato("nombre", "Orquídea")

    def actualizar_dato(self, clave, valor, campo_actualizar, nuevo_valor):
        """Actualiza un campo de un registro en base a una condición"""
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de actualizar datos.")
        for dato in self.datos:
            if dato.get(clave) == valor:
                dato[campo_actualizar] = nuevo_valor
                logging.info(f"Registro actualizado: {dato}")
    #data_json.actualizar_dato("nombre", "Rosa", "clima", "Cálido")

class DataBaseManager:#controlar bd mysql
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.connection.cursor()

    def conectar(self):
        """Conectar a la base de datos MongoDB"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            logging.info(
                f"Conectado a MongoDB: {self.database_name}.{self.collection_name}"
            )
        except PyMongoError as e:
            logging.error(f"Error al conectar a MongoDB: {e}")

    def desconectar(self):
        """Cerrar la conexión a MongoDB"""
        if self.client:
            self.client.close()
            logging.info("Conexión a MongoDB cerrada.")

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Plantas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                familia VARCHAR(255),
                clima VARCHAR(255)
            )
        """)
        self.connection.commit()

    def insertar_planta(self, nombre, familia, clima):
        self.cursor.execute("INSERT INTO Plantas (nombre, familia, clima) VALUES (%s, %s, %s)", (nombre, familia, clima))
        self.connection.commit()

    def consultar_plantas(self):
        self.cursor.execute("SELECT * FROM Plantas")
        return self.cursor.fetchall()
    
    def eliminar_planta(self, nombre):
        self.cursor.execute("DELETE FROM Plantas WHERE nombre = %s", (nombre,))
        self.connection.commit()

    def eliminar_por_condicion(self, columna, valor):
        """
        Elimina registros donde la columna numérica supere el valor dado.
        Ejemplo: eliminar_por_condicion('precio', 50) eliminará todos los registros donde precio > 50.
        """
        try:
            query = f"DELETE FROM Plantas WHERE {columna} > %s"
            self.cursor.execute(query, (valor,))
            self.connection.commit()
            logging.info(f"Registros eliminados donde {columna} > {valor}")
        except Error as e:
            logging.error(f"Error al eliminar registros: {e}")
            self.connection.rollback()

    def actualizar_planta(self, nombre, familia, clima):
        self.cursor.execute("UPDATE Plantas SET familia = %s, clima = %s WHERE nombre = %s", (familia, clima, nombre))
        self.connection.commit()

    def ejecutar_query(self, query, params=None):
        """Ejecuta una consulta SQL."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except mysql.connector.Error as e:
            logging.error(f"Error al ejecutar la consulta: {e}")
            self.connection.rollback()

class DatabaseManagerObject:
    """Componente para gestionar bases de datos orientadas a objetos con ZODB."""

    def __init__(self, filepath="1dam.fs"):
        self.filepath = filepath
        self.db = None
        self.connection = None
        self.root = None
        self.transaccion_iniciada = False

    def conectar(self):
        """Conecta a la base de datos ZODB."""
        try:
            storage = FileStorage.FileStorage(self.filepath)
            self.db = DB(storage)
            self.connection = self.db.open()
            self.root = self.connection.root()
            if "motocicletas" not in self.root:
                self.root["motocicletas"] = {}
                transaction.commit()
            logging.info("Conexión establecida con ZODB.")
        except Exception as e:
            logging.error(f"Error al conectar a ZODB: {e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        try:
            if self.connection:
                self.connection.close()
            if self.db:
                self.db.close()
            logging.info("Conexión a ZODB cerrada.")
        except Exception as e:
            logging.error(f"Error al cerrar la conexión a ZODB: {e}")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        try:
            transaction.begin()
            self.transaccion_iniciada = True
            logging.info("Transacción iniciada.")
        except Exception as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirma la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.commit()
                self.transaccion_iniciada = False
                logging.info("Transacción confirmada.")
            except Exception as e:
                logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revierte la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.abort()
                self.transaccion_iniciada = False
                logging.info("Transacción revertida.")
            except Exception as e:
                logging.error(f"Error al revertir la transacción: {e}")

    def crear_motocicleta(self, id, marca, cilindrada, precio):
        """Crea y almacena una nueva motocicleta."""
        try:
            if id in self.root["motocicletas"]:
                raise ValueError(f"Ya existe una motocicleta con ID {id}.")
            self.root["motocicletas"][id] = Motocicleta(marca, cilindrada, precio)
            logging.info(f"Motocicleta con ID {id} creada exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear la motocicleta con ID {id}: {e}")

    def leer_motocicletas(self):
        """Lee y muestra todas las motocicletas almacenadas."""
        try:
            motocicletas = self.root["motocicletas"]
            for id, motocicleta in motocicletas.items():
                logging.info(
                    f"ID: {id}, Marca: {motocicleta.marca}, Cilindrada: {motocicleta.cilindrada}, Precio: {motocicleta.precio}"
                )
            return motocicletas
        except Exception as e:
            logging.error(f"Error al leer las motocicletas: {e}")

    def actualizar_motocicleta(self, id, marca, cilindrada, precio):
        """Actualiza los atributos de una motocicleta."""
        try:
            motocicleta = self.root["motocicletas"].get(id)
            if not motocicleta:
                raise ValueError(f"No existe una motocicleta con ID {id}.")
            motocicleta.marca = marca
            motocicleta.cilindrada = cilindrada
            motocicleta.precio = precio
            logging.info(f"Motocicleta con ID {id} actualizada exitosamente.")
        except Exception as e:
            logging.error(f"Error al actualizar la motocicleta con ID {id}: {e}")

    def eliminar_motocicleta(self, id):
        """Elimina una motocicleta por su ID."""
        try:
            if id not in self.root["motocicletas"]:
                raise ValueError(f"No existe una motocicleta con ID {id}.")
            del self.root["motocicletas"][id]
            logging.info(f"Motocicleta con ID {id} eliminada exitosamente.")
        except Exception as e:
            logging.error(f"Error al eliminar la motocicleta con ID {id}: {e}")


#--------------------------USO DE DATA MANAGER--------------------------

if __name__ == "__main__":
    # Prueba DataManager con JSON
    data_json = DataManager("plantas.json")

    data_csv = DataManager("plantas.csv")
    data_json.iniciar_transaccion()
    data_csv.iniciar_transaccion()
    data_json.datos.append() = [
        {"nombre": "rosa", "familia": "Rosaceae", "tamaño": "mediano", "clima": "templado", "tipo_suelo": "arcilloso"},
        {"nombre": "girasol", "familia": "Asteraceae", "tamaño": "grande", "clima": "templado", "tipo_suelo": "arenoso"},
        {"nombre": "orquídea", "familia": "Orchidaceae", "tamaño": "pequeño", "clima": "tropical", "tipo_suelo": "arenoso"},
    ]

    data_csv.datos.append() = [
        {"nombre": "rosa", "familia": "Rosaceae", "tamaño": "mediano", "clima": "templado", "tipo_suelo": "arcilloso"},
        {"nombre": "girasol", "familia": "Asteraceae", "tamaño": "grande", "clima": "templado", "tipo_suelo": "arenoso"},
        {"nombre": "orquídea", "familia": "Orchidaceae", "tamaño": "pequeño", "clima": "tropical", "tipo_suelo": "arenoso"},
    ]
    data_json.confirmar_transaccion()
    data_csv.confirmar_transaccion()

    #leer archivo json
    data_json.confirmar_transaccion()
    data_csv.confirmar_transaccion()

    data_json._leer_archivo()
    print("ELEMENTOS DEL ARCHIVO JSON")
    for elemento in data_json.datos:
        print(elemento)
    print("ELEMENTOS DEL ARCHIVO CSV")
    for elemento in data_csv.datos:
        print(elemento)
    data_csv._leer_archivo()


#--------------------------USO DE DATABASE MANAGER--------------------------

    db_manager = DataBaseManager("localhost", "root", "usuario", "1dam")
    db_manager.crear_tabla()
    db_manager.insertar_planta("Cactus", "Cactaceae", "Árido")
    db_manager.insertar_planta("Rosa", "Rosaceae", "Templado")
    db_manager.insertar_planta("Girasol", "Asteraceae", "Templado")
    print("Plantas en MySQL:", db_manager.consultar_plantas())
    db_manager.eliminar_planta("Cactus")
    print("Plantas en MySQL:", db_manager.consultar_plantas())
    db_manager.actualizar_planta("Rosa", "Rosaceae", "Cálido")
    print("Plantas en MySQL:", db_manager.consultar_plantas())
    

#--------------------------USO DE DATABASEMANAGEROBJECT--------------------------

class DatabaseManagerObject:
    """Componente para gestionar bases de datos orientadas a objetos con ZODB."""

    def __init__(self, filepath="1dam.fs"):
        self.filepath = filepath
        self.db = None
        self.connection = None
        self.root = None
        self.transaccion_iniciada = False

    def conectar(self):
        """Conecta a la base de datos ZODB."""
        try:
            storage = FileStorage.FileStorage(self.filepath)
            self.db = DB(storage)
            self.connection = self.db.open()
            self.root = self.connection.root()
            if "motocicletas" not in self.root:
                self.root["motocicletas"] = {}
                transaction.commit()
            logging.info("Conexión establecida con ZODB.")
        except Exception as e:
            logging.error(f"Error al conectar a ZODB: {e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        try:
            if self.connection:
                self.connection.close()
            if self.db:
                self.db.close()
            logging.info("Conexión a ZODB cerrada.")
        except Exception as e:
            logging.error(f"Error al cerrar la conexión a ZODB: {e}")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        try:
            transaction.begin()
            self.transaccion_iniciada = True
            logging.info("Transacción iniciada.")
        except Exception as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirma la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.commit()
                self.transaccion_iniciada = False
                logging.info("Transacción confirmada.")
            except Exception as e:
                logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revierte la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.abort()
                self.transaccion_iniciada = False
                logging.info("Transacción revertida.")
            except Exception as e:
                logging.error(f"Error al revertir la transacción: {e}")

    def crear_motocicleta(self, id, marca, cilindrada, precio):
        """Crea y almacena una nueva motocicleta."""
        try:
            if id in self.root["motocicletas"]:
                raise ValueError(f"Ya existe una motocicleta con ID {id}.")
            self.root["motocicletas"][id] = Motocicleta(marca, cilindrada, precio)
            logging.info(f"Motocicleta con ID {id} creada exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear la motocicleta con ID {id}: {e}")

    def leer_motocicletas(self):
        """Lee y muestra todas las motocicletas almacenadas."""
        try:
            motocicletas = self.root["motocicletas"]
            for id, motocicleta in motocicletas.items():
                logging.info(
                    f"ID: {id}, Marca: {motocicleta.marca}, Cilindrada: {motocicleta.cilindrada}, Precio: {motocicleta.precio}"
                )
            return motocicletas
        except Exception as e:
            logging.error(f"Error al leer las motocicletas: {e}")

    def actualizar_motocicleta(self, id, marca, cilindrada, precio):
        """Actualiza los atributos de una motocicleta."""
        try:
            motocicleta = self.root["motocicletas"].get(id)
            if not motocicleta:
                raise ValueError(f"No existe una motocicleta con ID {id}.")
            motocicleta.marca = marca
            motocicleta.cilindrada = cilindrada
            motocicleta.precio = precio
            logging.info(f"Motocicleta con ID {id} actualizada exitosamente.")
        except Exception as e:
            logging.error(f"Error al actualizar la motocicleta con ID {id}: {e}")

    def eliminar_motocicleta(self, id):
        """Elimina una motocicleta por su ID."""
        try:
            if id not in self.root["motocicletas"]:
                raise ValueError(f"No existe una motocicleta con ID {id}.")
            del self.root["motocicletas"][id]
            logging.info(f"Motocicleta con ID {id} eliminada exitosamente.")
        except Exception as e:
            logging.error(f"Error al eliminar la motocicleta con ID {id}: {e}")
