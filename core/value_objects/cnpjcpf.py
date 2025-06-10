import re
from dataclasses import dataclass

@dataclass(frozen=True)
class CnpjCpf:
    """
    Value Object representing a Brazilian CNPJ (14 digits) or CPF (11 digits).

    Attributes:
        numero (str): Only digits, validated length of 11 (CPF) or 14 (CNPJ).
    """
    numero: str

    def __post_init__(self):
        # Remove any non-digit characters
        limpo = re.sub(r"\D", "", self.numero)
        if len(limpo) not in (11, 14):
            raise ValueError(f"CNPJ/CPF inválido: {self.numero}")
        # Optionally, could add checksum validation here
        object.__setattr__(self, 'numero', limpo)
