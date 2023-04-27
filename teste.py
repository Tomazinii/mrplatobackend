
def teste():

    lista = [1,2,3,4,5]
    new_lista = []
    for l in lista:
        if not l == 3:
            print("OKOK")
            new_lista.append(l)
        
    return new_lista


print(teste())

