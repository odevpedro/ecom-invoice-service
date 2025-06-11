from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from core.services.persistence.status_nota_model import StatusNotaModel
from core.services.persistence.base import Base




class NotaFiscalModel(Base):
    __tablename__ = "nota_fiscal"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    chave_acesso = Column(String(44), unique=True, index=True, nullable=True)
    status = Column(SQLEnum(StatusNotaModel), nullable=False, default=StatusNotaModel.EM_PROCESSAMENTO)
    data_emissao = Column(DateTime, default=datetime.utcnow, nullable=False)
    protocolo_autorizacao = Column(String, nullable=True)

    emitente_cnpj = Column(String(14), nullable=False)
    destinatario_cnpj = Column(String(14), nullable=False)
    emitente_endereco = Column(JSON, nullable=False)
    destinatario_endereco = Column(JSON, nullable=False)
    impostos_totais = Column(JSON, nullable=True)

    items = relationship("ItemDaNotaModel", back_populates="nota", cascade="all, delete-orphan")

