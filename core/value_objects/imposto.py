from dataclasses import dataclass

@dataclass(frozen=True)
class Imposto:
    """
    Value Object representing tax values for a fiscal note.

    Attributes:
        icms (float): Valor do ICMS.
        ipi (float): Valor do IPI.
        pis (float): Valor do PIS.
        cofins (float): Valor do COFINS.
    """
    icms: float
    ipi: float
    pis: float
    cofins: float

    @property
    def total_geral(self) -> float:
        """Retorna a soma de todos os impostos."""
        return self.icms + self.ipi + self.pis + self.cofins
