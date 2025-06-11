from abc import ABC, abstractmethod

from core.entities.nota_fiscal import NotaFiscal


class CartaCorrecaoPort(ABC):
    @abstractmethod
    def corrigir(self, chave_acesso: str, texto_correcao: str) -> NotaFiscal:
        """
        Emite uma Carta de Correcao Eletronica (CC-e) para a NF-e especificada.
        Retorna a NotaFiscal após processamento da CC-e.
        """
        pass