import random
lista=[]
for i in range(1,11):
    num=random.randint(1,50)
    lista.append(num)

buscado=int(input("Dime un numero a buscar:"))

#si el numero esta en la lista imprimimos Bingo
#para ellos usamos un booleano que sirve como flag en el caso de que encontremos
#el numero
encontrado=False
while not encontrado:
    
    if buscado in lista:
                print("Bingo!")
                encontrado=True
    else:
        print("Intentalo otra vez")
        buscado=int(input("Dime un numero a buscar:"))
