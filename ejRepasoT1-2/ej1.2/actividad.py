class Escribir_leer_archivo:

    def convertirAdecimal(self, file_path, mode='r'):
        numeros=[]
        try:
            with open(file_path, mode) as f:
                for linea in f:
                    linea=linea.strip()
                    if linea.startswith('0b'):
                        num=int(linea,2)
                    elif linea.startswith('0x'):
                        num=int(linea,16)
                    else:
                        num=int(linea)
                    
                    numeros.append(num)

            return numeros

        except Exception as e:
            print(f"Error leyendo el archivo: {e}")
            
    def escribirDecimales(self, file_path, content, mode='w'):
        try:
            with open(file_path, mode) as f:
                for n in content:
                    #PASAMOS A STRING PARA ESCRIBIR
                    f.write(str(n)+"\n")
        except Exception as e:
            print(f"Error escribiendo en el archivo: {e}")

escribir_leer_archivo=Escribir_leer_archivo()

ruta='entrada.txt'

numerosDecimales=escribir_leer_archivo.convertirAdecimal(ruta)

escribir_leer_archivo.escribirDecimales('salida.txt',numerosDecimales)






