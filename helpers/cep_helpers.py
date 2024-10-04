import requests

class Endereco:

    def __init__(self, cep):
        cep = str(cep)
        if self.valide_cep(cep):
            self.cep = cep
        else:
            raise ValueError("CEP Inválido!")

    def __str__(self):
        return self.format_cep()

    def valide_cep(self, cep):
        if len(cep) == 8:
            return True
        else:
            return False

    def format_cep(self):
        return "{}-{}".format(self.cep[:5], self.cep[5:])

    def acessa_via_cep(self):
        url = "https://viacep.com.br/ws/{}/json/".format(self.cep)
        request = requests.get(url)
        dados = request.json()
        return dados