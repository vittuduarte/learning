# %%
#Fazendo um tabuada com While
numero = 2
count = 0
while count <= 10:
    print(f"{numero} X {count} = ", numero * count)
    count += 1
print("Acabou a tabuada!")
    
# %%
#Numeros divisiveis por 4 entre 0 e 100

count = 4
while count <= 100:
    div4 = count % 4
    if div4 == 0:
        print(f"Os numeros divisiveis por 4 =", count)
    
    count += 1
print("Acabou")
# %%
