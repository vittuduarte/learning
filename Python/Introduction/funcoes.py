def f(x):
    return 1 + x


def juros_compostos(aporte:int, taxa:float, anos:int) -> float:
    """
    Juros compostos serve para calcular o retorno financeiro a partir de um aporte. Deve-se considerar o valor,
    a taxa de juros atual e o tempo (em anos) para calculo
    

    Args:
        aporte (int): Um numero inteiro, que represente o valor em R$.
        taxa (float): Um numero float entre 0 e 1 que represente o valor taxa de juros.
        anos (int): Um numero >= 1 que representa o tempo que o invertimento tera liquidez.

    Returns:
        float: retorna o juros compostos
    """
    return aporte * taxa ** anos


def ola_mundo():
    print("Boas vindas!")


#Funcao usando *args
def soma(a:float, b:float, *args)->float:
    valores = [a, b] + list(args)
    return sum(valores)

def media(a:float, b:float, *args) -> float:
    return soma(a, b, *args) / (len(args)+2)


#funcao utilizando **kwargs
def calc_imposto(preco:float, tx_base:float, **kwargs)->float:
    imposto = preco * tx_base
    
    for i in kwargs:
        print(i, kwargs[i])
        imposto += preco * kwargs[i]
    return imposto