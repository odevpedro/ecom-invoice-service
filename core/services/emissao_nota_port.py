from abc import ABC, abstractmethod

from core.entities.nota_fiscal import NotaFiscal


class EmissaoNotaPort(ABC):
    @abstractmethod
    def emitir(self, nota: NotaFiscal) -> NotaFiscal:
        """
        Gera o XML, assina e envia para a SEFAZ com base nos dados da NotaFiscal.
        Retorna a NotaFiscal atualizada com chave de acesso e protocolo preenchidos.
        """
        pass
