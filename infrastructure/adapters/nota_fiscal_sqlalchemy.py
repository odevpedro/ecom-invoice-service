from typing import Optional
from sqlalchemy.orm import Session

from core.entities.nota_fiscal import NotaFiscal
from core.services.ports.nota_fiscal_repository_port import NotaFiscalRepository
from core.services.persistence.nota_fiscal_model import NotaFiscalModel
from application.mappers.nota_fiscal_mapper import NotaFiscalMapper

class NotaFiscalSqlAlchemyAdapter(NotaFiscalRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, nota: NotaFiscal) -> None:
        """
        Persiste ou atualiza a NotaFiscal e seus itens no banco de dados.
        """
        model = NotaFiscalMapper.to_model(nota)
        self.session.merge(model)
        self.session.commit()

    def get_by_chave(self, chave_acesso: str) -> Optional[NotaFiscal]:
        """
        Busca o modelo no banco e delega a conversão Model → Entity ao mapper.
        """
        model = (
            self.session
                .query(NotaFiscalModel)
                .filter_by(chave_acesso=chave_acesso)
                .one_or_none()
        )
        if not model:
            return None
        return NotaFiscalMapper.to_entity(model)
