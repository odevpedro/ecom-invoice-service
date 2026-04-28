from abc import ABC, abstractmethod
from typing import Optional, List

from core.entities.nota_fiscal import NotaFiscal


class NotaFiscalRepository(ABC):
    @abstractmethod
    def save(self, nota: NotaFiscal) -> None:
        """
        Persiste ou atualiza a NotaFiscal no repositório.
        """
        pass

    @abstractmethod
    def get_by_chave(self, chave_acesso: str) -> Optional[NotaFiscal]:
        """
        Recupera a NotaFiscal pela chave de acesso, ou None se não existir.
        """
        pass

    @abstractmethod
    def list_all(self) -> List[NotaFiscal]:
        pass