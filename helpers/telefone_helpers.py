import re


class Telefone:
    # Expressão regular para validação de telefones, incluindo o 9 para celulares
    PADRAO_FORMATADO = r"^(\+?[1-9]{1,2})?([1-9][0-9])([0-9]{4,5})([0-9]{4})$"

    def __init__(self, telefone):
        telefone = telefone.strip()
        self.telefone_original = telefone  # Manter o número original para referência

        # Limpa e normaliza o número removendo caracteres especiais
        telefone = self.limpa_telefone(telefone)

        if self.valida_telefone(telefone):
            telefone = self.adiciona_codigo_pais(telefone)
            self.numero = telefone
        else:
            raise ValueError(f"Número incorreto: {telefone}")

    def __str__(self):
        return self.numero

    def limpa_telefone(self, telefone):
        return re.sub(r'\D', '', telefone)

    def adiciona_codigo_pais(self, telefone):
        resposta = re.fullmatch(self.PADRAO_FORMATADO, telefone)

        if resposta:
            codigo_pais = resposta.group(1) or '55'  # Padrão Brasil (55)
            ddd = resposta.group(2)
            parte1 = resposta.group(3)
            parte2 = resposta.group(4)

            # Remove o '+' do código do país, se presente
            if codigo_pais:
                codigo_pais = codigo_pais.replace('+', '')
            else:
                codigo_pais = '55'  # Se não houver código do país, usa 55 como padrão

            return f"{codigo_pais}({ddd}){parte1}-{parte2}"
        else:
            return telefone  # Retorna o telefone sem alteração se não corresponder ao padrão

    def valida_telefone(self, telefone):
        return bool(re.fullmatch(self.PADRAO_FORMATADO, telefone))

