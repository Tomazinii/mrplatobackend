# lista = [
#     "11 - ~ p -> ~ q , q ⊢ p\n",
#     "12 - p v q , ~ q , p -> r ^ s ⊢ s ^ r\n",
#     "13 - (r ^ ~ t ) -> ~ s , p -> s , p ^ q ⊢ ~ ( ~ t ^ r)\n",
#     "14 - (r ^ s) v p , q -> ~ p , t -> ~ p , q v t ⊢ s ^ r\n",
# ]

# lista_dict = []

# for i, texto in enumerate(lista):
#     texto = texto.strip()  # remove espaços no início e no final
#     partes = texto.split(" - ")  # separa o número da fórmula
#     num = partes[0]  # número da fórmula
#     formula = partes[1]  # fórmula lógica
#     lista_dict.append({"text": f"{num} - {formula}"})

# print(lista_dict)


lista = ['a', 'b', 'c', 'd']

for index, element in enumerate(lista):
    print(index, element)