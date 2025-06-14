# core/entities/nota_fiscal.py
"""
Domínio da Nota Fiscal eletrônica e ItemDaNota.
"""
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional

from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco
from core.value_objects.imposto import Imposto
from core.enum.status_nota import StatusNota

class ItemDaNota:
    def __init__(
        self,
        sku: str,
        descricao: str,
        quantidade: int,
        valor_unitario: float,
        cfop: str,
        ncm: str,
        cst: str,
        impostos: Imposto
    ):
        self.sku = sku
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.cfop = cfop
        self.ncm = ncm
        self.cst = cst
        self.impostos = impostos

    @property
    def total(self) -> float:
        return self.quantidade * self.valor_unitario

    def to_dict(self) -> dict:
        return {
            "sku": self.sku,
            "descricao": self.descricao,
            "quantidade": self.quantidade,
            "valor_unitario": self.valor_unitario,
            "cfop": self.cfop,
            "ncm": self.ncm,
            "cst": self.cst,
            "impostos": self.impostos.__dict__,
            "total": self.total,
        }

class NotaFiscal:
    """
    Entidade de domínio representando uma NF-e.
    """
    def __init__(
        self,
        emitente_cnpj: CnpjCpf,
        destinatario_cnpj: CnpjCpf,
        emitente_endereco: Endereco,
        destinatario_endereco: Endereco
    ):
        self.emitente_cnpj = emitente_cnpj
        self.destinatario_cnpj = destinatario_cnpj
        self.emitente_endereco = emitente_endereco
        self.destinatario_endereco = destinatario_endereco
        self.itens: List[ItemDaNota] = []
        self.id: UUID = uuid4()
        self.chave_acesso: Optional[str] = None
        self.status: StatusNota = StatusNota.EM_PROCESSAMENTO
        self.data_emissao: datetime = datetime.utcnow()
        self.protocolo_autorizacao: Optional[str] = None
        self.impostos_totais: Optional[Imposto] = None
        self.protocolo_cce: Optional[str] = None

    def adicionar_item(self, item: ItemDaNota) -> None:
        self.itens.append(item)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "chave_acesso": self.chave_acesso,
            "status": self.status.value,
            "data_emissao": self.data_emissao.isoformat(),
            "protocolo_autorizacao": self.protocolo_autorizacao,
            "protocolo_cce": self.protocolo_cce,
            "emitente_cnpj": self.emitente_cnpj.numero,
            "destinatario_cnpj": self.destinatario_cnpj.numero,
            "emitente_endereco": self.emitente_endereco.__dict__,
            "destinatario_endereco": self.destinatario_endereco.__dict__,
            "impostos_totais": (self.impostos_totais.__dict__ if self.impostos_totais else None),
            "itens": [item.to_dict() for item in self.itens],
        }
