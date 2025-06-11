# app/interfaces/controllers/invoice_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from core.entities.nota_fiscal import NotaFiscal, ItemDaNota
from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco
from core.value_objects.imposto import Imposto
from core.exceptions.domain_exceptions import DomainException
from application.use_cases.emit_invoice import EmitInvoiceUseCase

router = APIRouter(prefix="/invoices", tags=["invoices"])

class ItemSchema(BaseModel):
    sku: str
    descricao: str
    quantidade: int
    valor_unitario: float
    cfop: str
    ncm: str
    cst: str
    impostos: dict

class InvoiceCreateSchema(BaseModel):
    emitente_cnpj: str
    destinatario_cnpj: str
    emitente_endereco: dict
    destinatario_endereco: dict
    itens: List[ItemSchema]

class ItemResponseSchema(BaseModel):
    sku: str
    descricao: str
    quantidade: int
    valor_unitario: float
    cfop: str
    ncm: str
    cst: str
    impostos: dict
    total: float

class InvoiceResponseSchema(BaseModel):
    id: UUID
    chave_acesso: Optional[str]
    status: str
    data_emissao: datetime
    protocolo_autorizacao: Optional[str]
    emitente_cnpj: str
    destinatario_cnpj: str
    emitente_endereco: dict
    destinatario_endereco: dict
    impostos_totais: Optional[dict]
    itens: List[ItemResponseSchema]


def get_emit_invoice_use_case():
    from infrastructure.external_services.sefaz_client import SefazClient
    from infrastructure.external_services.signer import Signer
    from infrastructure.adapters.emissao_nota_adapter import NotaFiscalEmissaoAdapter
    from infrastructure.adapters.nota_fiscal_sqlalchemy import NotaFiscalSqlAlchemyAdapter
    from infrastructure.persistence.db import SessionLocal

    session = SessionLocal()
    repo = NotaFiscalSqlAlchemyAdapter(session)
    sefaz_client = SefazClient()
    signer = Signer()
    emissor = NotaFiscalEmissaoAdapter(sefaz_client, signer)
    return EmitInvoiceUseCase(emissor, repo)

@router.post("/", response_model=InvoiceResponseSchema, status_code=status.HTTP_201_CREATED)
async def emit_invoice(
    payload: InvoiceCreateSchema,
    use_case: EmitInvoiceUseCase = Depends(get_emit_invoice_use_case)
) -> InvoiceResponseSchema:
    # Monta entidade de domínio
    nota = NotaFiscal(
        emitente_cnpj=CnpjCpf(payload.emitente_cnpj),
        destinatario_cnpj=CnpjCpf(payload.destinatario_cnpj),
        emitente_endereco=Endereco(**payload.emitente_endereco),
        destinatario_endereco=Endereco(**payload.destinatario_endereco)
    )
    for item_payload in payload.itens:
        nota.adicionar_item(ItemDaNota(
            sku=item_payload.sku,
            descricao=item_payload.descricao,
            quantidade=item_payload.quantidade,
            valor_unitario=item_payload.valor_unitario,
            cfop=item_payload.cfop,
            ncm=item_payload.ncm,
            cst=item_payload.cst,
            impostos=Imposto(**item_payload.impostos)
        ))
    # Executa use case
    try:
        nota_emitida = use_case.execute(nota)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Converte para schema de resposta explicitamente
    itens_resp = []
    for it in nota_emitida.itens:
        itens_resp.append(ItemResponseSchema(
            sku=it.sku,
            descricao=it.descricao,
            quantidade=it.quantidade,
            valor_unitario=it.valor_unitario,
            cfop=it.cfop,
            ncm=it.ncm,
            cst=it.cst,
            impostos=it.impostos.__dict__,
            total=it.total
        ))

    resp = InvoiceResponseSchema(
        id=nota_emitida.id,
        chave_acesso=nota_emitida.chave_acesso,
        status=nota_emitida.status.value,
        data_emissao=nota_emitida.data_emissao,
        protocolo_autorizacao=nota_emitida.protocolo_autorizacao,
        emitente_cnpj=nota_emitida.emitente_cnpj.numero,
        destinatario_cnpj=nota_emitida.destinatario_cnpj.numero,
        emitente_endereco=nota_emitida.emitente_endereco.__dict__,
        destinatario_endereco=nota_emitida.destinatario_endereco.__dict__,
        impostos_totais=(nota_emitida.impostos_totais.__dict__ if nota_emitida.impostos_totais else None),
        itens=itens_resp
    )
    return resp
