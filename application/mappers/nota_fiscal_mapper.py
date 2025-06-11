# application/mappers/nota_fiscal_mapper.py
"""
Mapper utilities to convert between domain entities and persistence models.
"""
from core.entities.nota_fiscal import NotaFiscal, ItemDaNota
from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco
from core.value_objects.imposto import Imposto

# Import persistence models and enums
from core.services.persistence.nota_fiscal_model import NotaFiscalModel
from core.services.persistence.item_da_nota_model import ItemDaNotaModel
from core.services.persistence.status_nota_model import StatusNotaModel

# Import domain enum
from core.enum.status_nota import StatusNota

class NotaFiscalMapper:
    @staticmethod
    def to_model(nota: NotaFiscal) -> NotaFiscalModel:
        """Converte entidade de domínio para modelo SQLAlchemy."""
        # Map domain status to persistence enum
        persistence_status = StatusNotaModel[nota.status.name]

        model = NotaFiscalModel(
            id=nota.id,
            chave_acesso=nota.chave_acesso,
            status=persistence_status,
            data_emissao=nota.data_emissao,
            protocolo_autorizacao=nota.protocolo_autorizacao,
            emitente_cnpj=nota.emitente_cnpj.numero,
            destinatario_cnpj=nota.destinatario_cnpj.numero,
            emitente_endereco=nota.emitente_endereco.__dict__,
            destinatario_endereco=nota.destinatario_endereco.__dict__,
            impostos_totais=(nota.impostos_totais.__dict__ if nota.impostos_totais else None)
        )
        # Mapeia itens
        model.items = [
            ItemDaNotaModel(
                nota_id=nota.id,
                sku=item.sku,
                descricao=item.descricao,
                quantidade=item.quantidade,
                valor_unitario=item.valor_unitario,
                cfop=item.cfop,
                ncm=item.ncm,
                cst=item.cst,
                impostos=item.impostos.__dict__
            ) for item in nota.itens
        ]
        return model

    @staticmethod
    def to_entity(model: NotaFiscalModel) -> NotaFiscal:
        """Converte modelo SQLAlchemy para entidade de domínio."""
        # Reconstruct domain entity
        nota = NotaFiscal(
            emitente_cnpj=CnpjCpf(model.emitente_cnpj),
            destinatario_cnpj=CnpjCpf(model.destinatario_cnpj),
            emitente_endereco=Endereco(**model.emitente_endereco),
            destinatario_endereco=Endereco(**model.destinatario_endereco)
        )
        nota.id = model.id
        nota.chave_acesso = model.chave_acesso
        # Map persistence enum to domain enum
        nota.status = StatusNota[model.status.name]
        nota.data_emissao = model.data_emissao
        nota.protocolo_autorizacao = model.protocolo_autorizacao
        if model.impostos_totais:
            nota.impostos_totais = Imposto(**model.impostos_totais)
        # Reconstruct items
        for item_m in model.items:
            item = ItemDaNota(
                sku=item_m.sku,
                descricao=item_m.descricao,
                quantidade=item_m.quantidade,
                valor_unitario=item_m.valor_unitario,
                cfop=item_m.cfop,
                ncm=item_m.ncm,
                cst=item_m.cst,
                impostos=Imposto(**item_m.impostos)
            )
            nota.itens.append(item)
        return nota
