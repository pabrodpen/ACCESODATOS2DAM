import json


class Convertidor:
    def leer_json(self, file_json):
        sumaSalarios = 0
        nPersonas = 0
        maxEdad = 0
        nombreMaxEdad = ""
        with open(file_json, mode="r") as f:
            personas = json.load(
                f
            )  # Leemos el archivo JSON como una lista de diccionarios
            for persona in personas:
                salario = int(persona["Salario"])
                edad = int(persona["Edad"])
                sumaSalarios += salario
                nPersonas = nPersonas + 1
                if edad > maxEdad:
                    maxEdad = edad
                    nombreMaxEdad = persona["Nombre"]
        mediaSalarios = float(sumaSalarios / nPersonas)
        print("Media de salarios:" + str(mediaSalarios))
        print(
            "Trabajador con mayor edad:" + str(nombreMaxEdad) + " con " + str(maxEdad)
        )


convertidor = Convertidor()
convertidor.leer_json("entrada.json")
