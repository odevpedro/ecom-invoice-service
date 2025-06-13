# app/interfaces/controllers/invoice_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, constr, conint, confloat
from typing import List, Optional, Dict, TypeAlias
from uuid import UUID
from datetime import datetime

# Type aliases for readability (Pydantic v2 uses 'pattern' instead of 'regex')
CNPJType: TypeAlias = constr(pattern=r'^\d{14}$')
UFType: TypeAlias = constr(pattern=r'^[A-Z]{2}$')
CEPType: TypeAlias = constr(pattern=r'^\d{8}$')
CFOPType: TypeAlias = constr(pattern=r'^\d{4}$')
NCMType: TypeAlias = constr(pattern=r'^\d{8}$')
CSTType: TypeAlias = constr(pattern=r'^\d{3}$')

from core.entities.nota_fiscal import NotaFiscal, ItemDaNota
from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco
from core.value_objects.imposto import Imposto
from core.exceptions.domain_exceptions import DomainException, NotaNaoEncontradaException
from core.services.ports.nota_fiscal_repository_port import NotaFiscalRepository
from application.use_cases.emit_invoice import EmitInvoiceUseCase
from application.use_cases.cancel_invoice import CancelInvoiceUseCase
from infrastructure.adapters.emissao_nota_adapter import NotaFiscalEmissaoAdapter
from infrastructure.adapters.cancelamento_nota_adapter import NotaFiscalCancelamentoAdapter
from infrastructure.adapters.nota_fiscal_sqlalchemy import NotaFiscalSqlAlchemyAdapter
from infrastructure.external_services.sefaz_client import SefazClient
from infrastructure.external_services.signer import Signer
from infrastructure.persistence.db import SessionLocal

router = APIRouter(prefix="/invoices", tags=["invoices"])

# DTOs com validações Pydantic v2
class ItemSchema(BaseModel):
    sku: constr(pattern=r'^[A-Z0-9]{3,10}$') = Field(...)
    descricao: constr(min_length=3, max_length=100) = Field(...)
    quantidade: conint(gt=0) = Field(...)
    valor_unitario: confloat(gt=0.0) = Field(...)
    cfop: CFOPType = Field(...)
    ncm: NCMType = Field(...)
    cst: CSTType = Field(...)
    impostos: Dict[str, confloat(ge=0.0)] = Field(...)

class AddressSchema(BaseModel):
    logradouro: constr(min_length=3) = Field(...)
    numero: constr(min_length=1) = Field(...)
    municipio: constr(min_length=3) = Field(...)
    uf: UFType = Field(...)
    cep: CEPType = Field(...)
    complemento: Optional[str] = None
    bairro: Optional[str] = None

class InvoiceCreateSchema(BaseModel):
    emitente_cnpj: CNPJType = Field(...)
    destinatario_cnpj: CNPJType = Field(...)
    emitente_endereco: AddressSchema
    destinatario_endereco: AddressSchema
    itens: List[ItemSchema] = Field(..., min_items=1)

# Response DTOs
class ItemResponseSchema(ItemSchema):
    total: float

class InvoiceResponseSchema(BaseModel):
    id: UUID
    chave_acesso: Optional[str]
    status: str
    data_emissao: datetime
    protocolo_autorizacao: Optional[str]
    emitente_cnpj: str
    destinatario_cnpj: str
    emitente_endereco: Dict[str, str]
    destinatario_endereco: Dict[str, str]
    impostos_totais: Optional[Dict[str, float]]
    itens: List[ItemResponseSchema]

# Providers de dependência

def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_emit_use_case(session=Depends(get_db_session)) -> EmitInvoiceUseCase:
    repo = NotaFiscalSqlAlchemyAdapter(session)
    client = SefazClient()
    signer = Signer()
    adapter = NotaFiscalEmissaoAdapter(client, signer)
    return EmitInvoiceUseCase(adapter, repo)


def get_cancel_use_case(session=Depends(get_db_session)) -> CancelInvoiceUseCase:
    repo = NotaFiscalSqlAlchemyAdapter(session)
    client = SefazClient()
    signer = Signer()
    adapter = NotaFiscalCancelamentoAdapter(client, signer)
    return CancelInvoiceUseCase(adapter, repo)


def get_repository(session=Depends(get_db_session)) -> NotaFiscalRepository:
    return NotaFiscalSqlAlchemyAdapter(session)

# Rotas
@router.post("/", response_model=InvoiceResponseSchema, status_code=status.HTTP_201_CREATED)
def emit_invoice(
    payload: InvoiceCreateSchema,
    use_case: EmitInvoiceUseCase = Depends(get_emit_use_case)
) -> InvoiceResponseSchema:
    nota = NotaFiscal(
        emitente_cnpj=CnpjCpf(payload.emitente_cnpj),
        destinatario_cnpj=CnpjCpf(payload.destinatario_cnpj),
        emitente_endereco=Endereco(**payload.emitente_endereco.dict()),
        destinatario_endereco=Endereco(**payload.destinatario_endereco.dict())
    )
    # Corrige criação dos itens evitando conflitos de kwargs
    for item in payload.itens:
        item_data = item.dict()
        impostos_dict = item_data.pop('impostos')
        nota.adicionar_item(
            ItemDaNota(
                **item_data,
                impostos=Imposto(**impostos_dict)
            )
        )
    try:
        resultado = use_case.execute(nota)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    # Prepara resposta
    resp = resultado.to_dict()
    resp['itens'] = [
        {**it, 'total': it['quantidade'] * it['valor_unitario']} for it in resp['itens']
    ]
    return InvoiceResponseSchema(**resp)

@router.get("/", response_model=List[InvoiceResponseSchema])
def list_invoices(repo: NotaFiscalRepository = Depends(get_repository)) -> List[InvoiceResponseSchema]:
    results = []
    for nf in repo.list_all():
        data = nf.to_dict()
        data['itens'] = [
            {**it, 'total': it['quantidade'] * it['valor_unitario']} for it in data['itens']
        ]
        results.append(InvoiceResponseSchema(**data))
    return results

@router.get("/{chave_acesso}", response_model=InvoiceResponseSchema)
def get_invoice(chave_acesso: str, repo: NotaFiscalRepository = Depends(get_repository)) -> InvoiceResponseSchema:
    nf = repo.get_by_chave(chave_acesso)
    if not nf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data = nf.to_dict()
    data['itens'] = [
        {**it, 'total': it['quantidade'] * it['valor_unitario']} for it in data['itens']
    ]
    return InvoiceResponseSchema(**data)

@router.post("/{chave_acesso}/cancel", response_model=InvoiceResponseSchema)
def cancel_invoice(chave_acesso: str, use_case: CancelInvoiceUseCase = Depends(get_cancel_use_case)) -> InvoiceResponseSchema:
    try:
        nf = use_case.execute(chave_acesso)
    except NotaNaoEncontradaException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data = nf.to_dict()
    data['itens'] = [
        {**it, 'total': it['quantidade'] * it['valor_unitario']} for it in data['itens']
    ]
    return InvoiceResponseSchema(**data)
