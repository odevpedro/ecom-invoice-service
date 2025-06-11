from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ItemDaNotaModel(Base):
    __tablename__ = "item_da_nota"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nota_id = Column(PGUUID(as_uuid=True), ForeignKey("nota_fiscal.id"), nullable=False)
    sku = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    cfop = Column(String, nullable=False)
    ncm = Column(String, nullable=False)
    cst = Column(String, nullable=False)
    impostos = Column(JSON, nullable=False)

    nota = relationship("NotaFiscalModel", back_populates="items")