from datamanager import DataManager

# Crear instancia de DataManager para JSON
data_manager_json = DataManager("plantas.json", "json")

# Insertar datos en el archivo JSON
data_manager_json.iniciar_transaccion()
data_manager_json.escribir_dato(
    {
        "nombre": "Rosa",
        "familia": "Rosaceae",
        "tamaño": "Pequeña",
        "clima": "Templado",
        "tipo_suelo": "Arcilloso",
    }
)
data_manager_json.escribir_dato(
    {
        "nombre": "Cactus",
        "familia": "Cactaceae",
        "tamaño": "Mediana",
        "clima": "Árido",
        "tipo_suelo": "Arenoso",
    }
)
data_manager_json.escribir_dato(
    {
        "nombre": "Pino",
        "familia": "Pinaceae",
        "tamaño": "Grande",
        "clima": "Frío",
        "tipo_suelo": "Ácido",
    }
)
data_manager_json.confirmar_transaccion()

#
# Cambiar a CSV
data_manager_csv = DataManager("plantas.csv", "csv")

# Transferir datos del JSON al CSV
data_manager_csv.iniciar_transaccion()
for planta in data_manager_json.datos:
    data_manager_csv.escribir_dato(planta)
data_manager_csv.confirmar_transaccion()
