import logging
import mysql.connector

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager.log"),
        logging.StreamHandler(),
    ],
)


class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def conectar(self):
        """Establece conexión con la base de datos."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(
                    """
                CREATE TABLE IF NOT EXISTS Proveedores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    contacto VARCHAR(255) NOT NULL
                );
                CREATE TABLE IF NOT EXISTS Herramientas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    tipo VARCHAR(255) NOT NULL,
                    proveedor_id INT,
                    FOREIGN KEY (proveedor_id) REFERENCES Proveedores(id)
                );
                """
                )
                logging.info("Conexión establecida y tablas creadas.")
        except mysql.connector.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Conexión cerrada.")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        if self.connection:
            self.connection.start_transaction()
            logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        """Confirma una transacción."""
        if self.connection:
            self.connection.commit()
            logging.info("Transacción confirmada.")

    def ejecutar(self, query, params=None):
        """Ejecuta una consulta SQL."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except mysql.connector.Error as e:
            logging.error(f"Error al ejecutar la consulta: {e}")
            self.connection.rollback()


# Instanciar el gestor de base de datos
db_manager = DatabaseManager("localhost", "root", "password", "1dam")
db_manager.conectar()

try:
    # Gestión de Proveedores
    db_manager.iniciar_transaccion()
    db_manager.ejecutar(
        "INSERT INTO Proveedores (nombre, contacto) VALUES (%s, %s)",
        ("Proveedor A", "123-456-789"),
    )
    db_manager.ejecutar(
        "INSERT INTO Proveedores (nombre, contacto) VALUES (%s, %s)",
        ("Proveedor B", "987-654-321"),
    )
    db_manager.confirmar_transaccion()

    # Actualizar contacto del Proveedor A con DNI
    db_manager.iniciar_transaccion()
    db_manager.ejecutar(
        "UPDATE Proveedores SET contacto = %s WHERE nombre = %s",
        ("12345678A", "Proveedor A"),
    )
    db_manager.confirmar_transaccion()

    # Eliminar Proveedor B
    db_manager.iniciar_transaccion()
    db_manager.ejecutar("DELETE FROM Proveedores WHERE nombre = %s", ("Proveedor B",))
    db_manager.confirmar_transaccion()

    # Gestión de Herramientas
    # Asociar herramientas al Proveedor A (id=1)
    db_manager.iniciar_transaccion()
    db_manager.ejecutar(
        "INSERT INTO Herramientas (nombre, tipo, proveedor_id) VALUES (%s, %s, %s)",
        ("Martillo", "Manual", 1),
    )
    db_manager.ejecutar(
        "INSERT INTO Herramientas (nombre, tipo, proveedor_id) VALUES (%s, %s, %s)",
        ("Taladro", "Eléctrico", 1),
    )
    db_manager.confirmar_transaccion()

    # Consultar Herramientas del Proveedor A
    cursor = db_manager.ejecutar(
        "SELECT * FROM Herramientas WHERE proveedor_id = %s", (1,)
    )
    herramientas = cursor.fetchall()
    logging.info("Herramientas asociadas al Proveedor A:")
    for herramienta in herramientas:
        logging.info(f"{herramienta[1]} - {herramienta[2]}")

    # Actualizar herramienta Martillo a tipo reforzado
    db_manager.iniciar_transaccion()
    db_manager.ejecutar(
        "UPDATE Herramientas SET tipo = %s WHERE nombre = %s", ("Reforzado", "Martillo")
    )
    db_manager.confirmar_transaccion()

    # Eliminar herramienta Taladro
    db_manager.iniciar_transaccion()
    db_manager.ejecutar("DELETE FROM Herramientas WHERE nombre = %s", ("Taladro",))
    db_manager.confirmar_transaccion()

except Exception as e:
    logging.error(f"Se produjo un error general: {e}")
finally:
    db_manager.desconectar()
