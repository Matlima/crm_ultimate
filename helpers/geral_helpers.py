import re

def apenas_numeros(string):
    # Utiliza expressões regulares para substituir tudo que não é número por uma string vazia
    return re.sub(r'\D', '', string)


# - Teste app
if __name__ == "__main__":
    cpf = "862.227.659-69"
    resultado = apenas_numeros(cpf)
    print(resultado)