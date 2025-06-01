#Identifique se uma palavra e palindromo ou nao
#%%
def palindromo(texto:str) -> str:
    texto = texto.lower().replace(" ", "").replace(",", "").replace(".", "")
    invertido = texto[::-1]
    
    if texto == invertido:
        return True
    else:
        return False
    

palavra = input("Digite uma palavra, frase ou número: ")
palavra = str(palavra)
    
if palindromo(palavra):
    print("A palavra é um palíndromo")
else:
    print("A entrada não é um palíndromo")
# %%
