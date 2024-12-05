from database_manager import DatabaseManager

# Instanciar y conectar con la base de datos
db_manager = DatabaseManager("localhost", "root", "password", "plantas_db")
db_manager.conectar()

# Crear registros
db_manager.iniciar_transaccion()
db_manager.crear_registro(
    "Plantas",
    {
        "nombre": "Rosa",
        "familia": "Rosaceae",
        "tamaño": "Pequeña",
        "clima": "Templado",
        "tipo_suelo": "Arcilloso",
    },
)
db_manager.crear_registro(
    "Plantas",
    {
        "nombre": "Cactus",
        "familia": "Cactaceae",
        "tamaño": "Mediana",
        "clima": "Árido",
        "tipo_suelo": "Arenoso",
    },
)
db_manager.confirmar_transaccion()

# Leer registros
plantas = db_manager.leer_registros("Plantas")
print(plantas)

# Actualizar un registro
db_manager.iniciar_transaccion()
db_manager.actualizar_registro("Plantas", {"nombre": "Rosa"}, {"clima": "Cálido"})
db_manager.confirmar_transaccion()

# Eliminar un registro
db_manager.iniciar_transaccion()
db_manager.eliminar_registro("Plantas", {"nombre": "Cactus"})
db_manager.confirmar_transaccion()

# Desconectar
db_manager.desconectar()
