import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Endereco:
    logradouro: str
    numero: str
    municipio: str
    uf: str
    cep: str
    complemento: str = ""
    bairro: str = ""

    def __post_init__(self):
        # Valida e limpa o cep
        cep_limpo = re.sub(r"\D", "", self.cep)
        if not re.fullmatch(r"\d{8}", cep_limpo):
            raise ValueError(f"CEP inválido: {self.cep}")
        # Normaliza o uf
        uf_up = self.uf.strip().upper()
        estados = {
            "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
            "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
            "RS","RO","RR","SC","SP","SE","TO"
        }
        if uf_up not in estados:
            raise ValueError(f"UF inválido: {self.uf}")
        object.__setattr__(self, 'cep', cep_limpo)
        object.__setattr__(self, 'uf', uf_up)
