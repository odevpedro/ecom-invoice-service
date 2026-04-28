import pytest

from core.entities.nota_fiscal import ItemDaNota, NotaFiscal
from core.enum.status_nota import StatusNota
from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco
from core.value_objects.imposto import Imposto


def _make_endereco(uf="SP", cep="01001000"):
    return Endereco(logradouro="Rua X", numero="1", municipio="SP", uf=uf, cep=cep)


def _make_imposto():
    return Imposto(icms=10.0, ipi=5.0, pis=0.0, cofins=0.0)


def _make_item(**kwargs):
    defaults = dict(
        sku="ABC123",
        descricao="Produto Teste",
        quantidade=2,
        valor_unitario=50.0,
        cfop="5102",
        ncm="12345678",
        cst="102",
        impostos=_make_imposto(),
    )
    defaults.update(kwargs)
    return ItemDaNota(**defaults)


def _make_nota():
    return NotaFiscal(
        emitente_cnpj=CnpjCpf("12345678000199"),
        destinatario_cnpj=CnpjCpf("98765432000100"),
        emitente_endereco=_make_endereco("SP", "01001000"),
        destinatario_endereco=_make_endereco("RJ", "20020000"),
    )


class TestItemDaNota:
    def test_total_is_quantidade_times_valor_unitario(self):
        item = _make_item(quantidade=3, valor_unitario=20.0)
        assert item.total == 60.0

    def test_total_with_fractional_values(self):
        item = _make_item(quantidade=1, valor_unitario=9.99)
        assert abs(item.total - 9.99) < 1e-9

    def test_to_dict_contains_required_keys(self):
        item = _make_item()
        d = item.to_dict()
        for key in ("sku", "descricao", "quantidade", "valor_unitario", "cfop", "ncm", "cst", "impostos", "total"):
            assert key in d

    def test_to_dict_total_matches_property(self):
        item = _make_item(quantidade=2, valor_unitario=50.0)
        d = item.to_dict()
        assert d["total"] == item.total

    def test_to_dict_impostos_is_dict(self):
        item = _make_item()
        assert isinstance(item.to_dict()["impostos"], dict)


class TestNotaFiscal:
    def test_initial_status_is_em_processamento(self):
        nota = _make_nota()
        assert nota.status == StatusNota.EM_PROCESSAMENTO

    def test_initial_chave_acesso_is_none(self):
        nota = _make_nota()
        assert nota.chave_acesso is None

    def test_initial_itens_list_is_empty(self):
        nota = _make_nota()
        assert nota.itens == []

    def test_adicionar_item_appends_to_itens(self):
        nota = _make_nota()
        nota.adicionar_item(_make_item())
        assert len(nota.itens) == 1

    def test_adicionar_multiple_items(self):
        nota = _make_nota()
        nota.adicionar_item(_make_item(sku="ABC123"))
        nota.adicionar_item(_make_item(sku="DEF456"))
        assert len(nota.itens) == 2

    def test_to_dict_contains_required_keys(self):
        nota = _make_nota()
        d = nota.to_dict()
        for key in ("id", "chave_acesso", "status", "data_emissao", "emitente_cnpj",
                    "destinatario_cnpj", "itens", "impostos_totais"):
            assert key in d

    def test_to_dict_status_is_string_value(self):
        nota = _make_nota()
        assert nota.to_dict()["status"] == "EM_PROCESSAMENTO"

    def test_to_dict_emitente_cnpj_is_string(self):
        nota = _make_nota()
        assert nota.to_dict()["emitente_cnpj"] == "12345678000199"

    def test_to_dict_itens_reflects_added_items(self):
        nota = _make_nota()
        nota.adicionar_item(_make_item())
        assert len(nota.to_dict()["itens"]) == 1

    def test_id_is_unique_per_instance(self):
        nota1 = _make_nota()
        nota2 = _make_nota()
        assert nota1.id != nota2.id
