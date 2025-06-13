from abc import ABC, abstractmethod
from typing import Optional, List

from application.mappers.nota_fiscal_mapper import NotaFiscalMapper
from core.entities.nota_fiscal import NotaFiscal
from core.services.persistence.nota_fiscal_model import NotaFiscalModel


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

    def list_all(self) -> List[NotaFiscal]:
        models = self.session.query(NotaFiscalModel).all()
        return [NotaFiscalMapper.to_entity(m) for m in models]