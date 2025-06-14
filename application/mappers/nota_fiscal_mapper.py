# application/mappers/nota_fiscal_mapper.py
"""
Converte entre modelos SQLAlchemy (infrastructure.persistence.db) e entidades de domínio.
"""
from core.entities.nota_fiscal import NotaFiscal, ItemDaNota
from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco
from core.value_objects.imposto import Imposto
from core.enum.status_nota import StatusNota
from core.services.persistence.nota_fiscal_model import NotaFiscalModel
from core.services.persistence.item_da_nota_model import ItemDaNotaModel

class NotaFiscalMapper:
    @staticmethod
    def to_entity(model: NotaFiscalModel) -> NotaFiscal:
        # Obtém lista de itens
        raw_items = getattr(model, 'itens', None) or getattr(model, 'items', [])
        itens = []
        for m in raw_items:
            item = ItemDaNota(
                sku=m.sku,
                descricao=m.descricao,
                quantidade=m.quantidade,
                valor_unitario=m.valor_unitario,
                cfop=m.cfop,
                ncm=m.ncm,
                cst=m.cst,
                impostos=Imposto(**(m.impostos or {}))
            )
            itens.append(item)

        # Cria a entidade de domínio
        nf = NotaFiscal(
            CnpjCpf(model.emitente_cnpj),
            CnpjCpf(model.destinatario_cnpj),
            Endereco(**model.emitente_endereco),
            Endereco(**model.destinatario_endereco)
        )
        # Atribui campos restantes
        nf.itens = itens
        nf.id = model.id
        nf.chave_acesso = model.chave_acesso
        # Converter status corretamente, seja string ou Enum
        status_value = model.status.value if hasattr(model.status, 'value') else model.status
        nf.status = StatusNota(status_value)
        nf.data_emissao = model.data_emissao
        nf.protocolo_autorizacao = model.protocolo_autorizacao
        nf.impostos_totais = Imposto(**model.impostos_totais) if model.impostos_totais else None
        # protocolo de correção se existir
        if hasattr(model, 'protocolo_cce'):
            setattr(nf, 'protocolo_cce', model.protocolo_cce)
        return nf

    @staticmethod
    def to_model(nf: NotaFiscal) -> NotaFiscalModel:
        # Converte entidade para modelo SQLAlchemy
        model = NotaFiscalModel(
            id=nf.id,
            chave_acesso=nf.chave_acesso,
            status=nf.status.value,
            data_emissao=nf.data_emissao,
            protocolo_autorizacao=nf.protocolo_autorizacao,
            emitente_cnpj=nf.emitente_cnpj.numero,
            destinatario_cnpj=nf.destinatario_cnpj.numero,
            emitente_endereco=nf.emitente_endereco.__dict__,
            destinatario_endereco=nf.destinatario_endereco.__dict__,
            impostos_totais=(nf.impostos_totais.__dict__ if nf.impostos_totais else None)
        )
        # Ajusta protocolo de correção se existir
        if getattr(nf, 'protocolo_cce', None) is not None:
            model.protocolo_cce = nf.protocolo_cce

        # Mapear itens
        item_models = []
        for it in nf.itens:
            item_model = ItemDaNotaModel(
                nota_id=model.id,
                sku=it.sku,
                descricao=it.descricao,
                quantidade=it.quantidade,
                valor_unitario=it.valor_unitario,
                cfop=it.cfop,
                ncm=it.ncm,
                cst=it.cst,
                impostos=it.impostos.__dict__
            )
            item_models.append(item_model)
        model.itens = item_models
        return model
