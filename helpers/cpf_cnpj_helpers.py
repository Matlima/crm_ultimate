from validate_docbr import CPF, CNPJ

class Documento:

    @staticmethod
    def cria_documento(documento):
        if len(documento) == 11:
            return DocCpf(documento)
        elif len(documento) == 14:
            return DocCnjp(documento)
        else:
            raise ValueError("Quantidade de dígitos esta incorreta!")


class DocCpf():
    def __init__(self, documento):
        if self.valida(documento):
            self.cpf = documento
        else:
            raise ValueError("CPF Inválido!")

    def __str__(self):
        return self.format()

    def valida(self, documento):
        validador = CPF()
        return validador.validate(documento)

    # Formatando para XXX.XXX.XXX-XX
    def format(self):
        mascara = CPF()
        return mascara.mask(self.cpf)

class DocCnjp():
    def __init__(self, documento):
        if self.valida(documento):
            self.cnpj = documento
        else:
            raise ValueError("CNPJ Inválido!")

    def __str__(self):
        return self.format()

    def valida(self, documento):
        validate_cnpj = CNPJ()
        return validate_cnpj.validate(documento)


    def format(self):
        mascara = CNPJ()
        return mascara.mask(self.cnpj)
