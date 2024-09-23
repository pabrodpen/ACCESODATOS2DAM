#importamos la libreria random
import random
#inicializamos lista
lista=[]

for i in range(1,11):
    #con el método randint, vamos rellenando la lista con numeros aleatorios del 1 al 50
    numAleatorio=random.randint(1,50)
    #lo añadimos al final de la lista
    lista.append(numAleatorio)
#imprimimos
print(lista)
