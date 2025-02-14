import re
valor=input("Digite um valor: ")
def validar_decimal(numero):
    padrao = r"^-?\d+(?:[.,]\d+)?$"
    return bool(re.match(padrao, numero)), numero
ver = validar_decimal(valor)
print(ver[1])

if ver[0]:
    print(f"O valor digitado é um número decimal válido.{ver[1]}")
else:
    print(f"O valor digitado não é um número decimal válido.{ver[1]}")