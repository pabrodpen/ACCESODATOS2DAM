import random
lista=[]

for i in range(1,11):
    #con el método randint, vamos rellenando la lista con numeros aleatorios del 1 al 50
    numAleatorio=random.randint(1,50)
    lista.append(numAleatorio)
print(lista)
