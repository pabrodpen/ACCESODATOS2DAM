#Ejercicio: Gestión Integral de Datos con Múltiples Sistemas de Almacenamiento


#JSON y CSV con DataManager.
#Base de datos relacional MySQL con DatabaseManager.
#MongoDB para bases de datos NoSQL con DatabaseManagerDocumental.
#ZODB para bases de datos orientadas a objetos con DatabaseManagerObject.
#Cada tipo de almacenamiento se usará para gestionar información sobre plantas, aplicando operaciones CRUD y transacciones.

import json
import csv
import logging
import os
import transaction
import mysql.connector
from pymongo import MongoClient
from ZODB import DB, FileStorage
from persistent import Persistent
from copy import deepcopy

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("datamanager.log"), logging.StreamHandler()],
)

# --------------------------
# 📌 PARTE 1: JSON y CSV
# --------------------------
class DataManager:
    def __init__(self, ruta_archivo, tipo_archivo="json"):
        self.ruta_archivo = ruta_archivo
        self.tipo_archivo = tipo_archivo
        self.transaccion_activa = False
        self.copia_datos = None

        if os.path.exists(ruta_archivo):
            self.datos = self._leer_archivo()
        else:
            self.datos = []
            self._guardar_archivo()

    def _leer_archivo(self):
        with open(self.ruta_archivo, "r") as archivo:
            return json.load(archivo) if self.tipo_archivo == "json" else list(csv.DictReader(archivo))

    def _guardar_archivo(self):
        with open(self.ruta_archivo, "w") as archivo:
            if self.tipo_archivo == "json":
                json.dump(self.datos, archivo, indent=4)
            else:
                escritor = csv.DictWriter(archivo, fieldnames=self.datos[0].keys())
                escritor.writeheader()
                escritor.writerows(self.datos)

    def iniciar_transaccion(self):
        self.transaccion_activa = True
        self.copia_datos = deepcopy(self.datos)

    def confirmar_transaccion(self):
        self.transaccion_activa = False
        self.copia_datos = None
        self._guardar_archivo()

# --------------------------
# 📌 PARTE 2: MySQL
# --------------------------
class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost", user="root", password="usuario", database="gestion_plantas"
        )
        self.cursor = self.connection.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
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

    def obtener_plantas(self):
        self.cursor.execute("SELECT * FROM Plantas")
        return self.cursor.fetchall()

# --------------------------
# 📌 PARTE 3: MongoDB
# --------------------------
class DatabaseManagerDocumental:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["plantas_db"]
        self.coleccion = self.db["plantas"]

    def insertar_planta(self, planta):
        self.coleccion.insert_one(planta)

    def obtener_plantas(self):
        return list(self.coleccion.find({}, {"_id": 0}))

# --------------------------
# 📌 PARTE 4: ZODB (BD Orientada a Objetos)
# --------------------------
class Planta(Persistent):
    def __init__(self, nombre, familia, clima):
        self.nombre = nombre
        self.familia = familia
        self.clima = clima

class DatabaseManagerObject:
    def __init__(self):
        self.storage = FileStorage.FileStorage("plantas.fs")
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()
        if "plantas" not in self.root:
            self.root["plantas"] = {}

    def insertar_planta(self, id, planta):
        self.root["plantas"][id] = planta
        transaction.commit()

    def obtener_plantas(self):
        return self.root["plantas"]

# --------------------------
# 📌 PRUEBA DE FUNCIONALIDAD
# --------------------------
if __name__ == "__main__":
    # 1️⃣ 📂 JSON y CSV
    data_manager = DataManager("plantas.json", "json")
    data_manager.iniciar_transaccion()
    data_manager.datos.append({"nombre": "Orquídea", "familia": "Orchidaceae", "clima": "Tropical"})
    data_manager.confirmar_transaccion()

    # 2️⃣ 🗄️ MySQL
    db_mysql = DatabaseManager()
    db_mysql.insertar_planta("Rosa", "Rosaceae", "Templado")
    print("Plantas en MySQL:", db_mysql.obtener_plantas())

    # 3️⃣ 🗃️ MongoDB
    db_mongo = DatabaseManagerDocumental()
    db_mongo.insertar_planta({"nombre": "Cactus", "familia": "Cactaceae", "clima": "Árido"})
    print("Plantas en MongoDB:", db_mongo.obtener_plantas())

    # 4️⃣ 🏗️ ZODB
    db_zodb = DatabaseManagerObject()
    db_zodb.insertar_planta("1", Planta("Pino", "Pinaceae", "Frío"))
    print("Plantas en ZODB:")
    for key, planta in db_zodb.obtener_plantas().items():
        print(f"{key}: {planta.nombre}, {planta.familia}, {planta.clima}")
