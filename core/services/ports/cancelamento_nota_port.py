from abc import ABC, abstractmethod

from core.entities.nota_fiscal import NotaFiscal


class CancelamentoNotaPort(ABC):
    @abstractmethod
    def cancelar(self, chave_acesso: str) -> NotaFiscal:
        """
        Solicita o cancelamento de uma NF-e já autorizada.
        Retorna a NotaFiscal com status cancelado.
        """
        pass