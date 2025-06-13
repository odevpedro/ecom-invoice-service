from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, Optional

from core.enum.status_nota import StatusNota
from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco
from core.value_objects.imposto import Imposto
from core.exceptions.domain_exceptions import (
    NotaJaEmitidaException,
    NotaNaoEncontradaException
)

@dataclass
class ItemDaNota:
    sku: str
    descricao: str
    quantidade: int
    valor_unitario: float
    cfop: str
    ncm: str
    cst: str
    impostos: Imposto

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

@dataclass
class NotaFiscal:

    emitente_cnpj: CnpjCpf
    destinatario_cnpj: CnpjCpf
    emitente_endereco: Endereco
    destinatario_endereco: Endereco

    # Campos opcionais/com default seguem após
    id: UUID = field(default_factory=uuid4)
    chave_acesso: Optional[str] = None
    status: StatusNota = StatusNota.EM_PROCESSAMENTO
    data_emissao: datetime = field(default_factory=datetime.utcnow)
    protocolo_autorizacao: Optional[str] = None
    itens: List[ItemDaNota] = field(default_factory=list)
    impostos_totais: Optional[Imposto] = None

    def adicionar_item(self, item: ItemDaNota):
        if self.status is not StatusNota.EM_PROCESSAMENTO:
            raise NotaJaEmitidaException("Não é possível adicionar itens após emissão.")
        self.itens.append(item)

    def calcular_totais(self) -> float:
        if not self.itens:
            raise NotaNaoEncontradaException("Nenhum item para calcular.")
        total_produtos = sum(item.total for item in self.itens)
        total_icms = sum(item.impostos.icms for item in self.itens)
        total_ipi = sum(item.impostos.ipi for item in self.itens)
        total_pis = sum(item.impostos.pis for item in self.itens)
        total_cofins = sum(item.impostos.cofins for item in self.itens)
        self.impostos_totais = Imposto(
            icms=total_icms,
            ipi=total_ipi,
            pis=total_pis,
            cofins=total_cofins
        )
        return total_produtos + self.impostos_totais.total_geral

    def emitir(self):
        if self.status is not StatusNota.EM_PROCESSAMENTO:
            raise NotaJaEmitidaException("Nota já foi emitida ou está em estado inválido.")
        _ = self.calcular_totais()
        # A lógica de comunicação com SEFAZ e preenchimento de chave/protocolo
        # será implementada no Application Service
        self.status = StatusNota.AUTORIZADA
        return self.impostos_totais

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "chave_acesso": self.chave_acesso,
            "status": self.status.value,
            "data_emissao": self.data_emissao.isoformat(),
            "protocolo_autorizacao": self.protocolo_autorizacao,
            "emitente_cnpj": self.emitente_cnpj.numero,
            "destinatario_cnpj": self.destinatario_cnpj.numero,
            "emitente_endereco": self.emitente_endereco.__dict__,
            "destinatario_endereco": self.destinatario_endereco.__dict__,
            "impostos_totais": (self.impostos_totais.__dict__ if self.impostos_totais else None),
            "itens": [item.to_dict() for item in self.itens],
        }
