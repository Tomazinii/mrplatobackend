list_of_problems = ['1 - p → q , p ⊢ q', '2 - p → q , ~q ⊢ ~p', '3 - p → q , q → s ⊢ p → s']

new_line = ["zzz"]

# Substituir a string na posição 1 pela nova string "zzz⊢"
for element in new_line:
    list_of_problems[1] = list_of_problems[1].replace("⊢", f", {element} ⊢", 1)

print(list_of_problems)