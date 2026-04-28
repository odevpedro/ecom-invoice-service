import pytest

from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco
from core.value_objects.imposto import Imposto


class TestCnpjCpf:
    def test_valid_cnpj_stores_only_digits(self):
        c = CnpjCpf("12345678000199")
        assert c.numero == "12345678000199"

    def test_valid_cpf_stores_only_digits(self):
        c = CnpjCpf("12345678901")
        assert c.numero == "12345678901"

    def test_strips_formatting_from_cnpj(self):
        c = CnpjCpf("12.345.678/0001-99")
        assert c.numero == "12345678000199"

    def test_strips_formatting_from_cpf(self):
        c = CnpjCpf("123.456.789-01")
        assert c.numero == "12345678901"

    def test_too_short_raises_value_error(self):
        with pytest.raises(ValueError):
            CnpjCpf("123456")

    def test_too_long_raises_value_error(self):
        with pytest.raises(ValueError):
            CnpjCpf("123456789012345")

    def test_twelve_digits_raises_value_error(self):
        with pytest.raises(ValueError):
            CnpjCpf("123456789012")

    def test_is_immutable(self):
        c = CnpjCpf("12345678000199")
        with pytest.raises((AttributeError, TypeError)):
            c.numero = "99999999000199"


class TestEndereco:
    def _make(self, **kwargs):
        defaults = dict(
            logradouro="Av. Brasil",
            numero="100",
            municipio="Sao Paulo",
            uf="SP",
            cep="01001000",
        )
        defaults.update(kwargs)
        return Endereco(**defaults)

    def test_valid_address_stores_normalized_fields(self):
        e = self._make()
        assert e.cep == "01001000"
        assert e.uf == "SP"

    def test_normalizes_uf_to_uppercase(self):
        e = self._make(uf="sp")
        assert e.uf == "SP"

    def test_strips_cep_punctuation(self):
        e = self._make(cep="01001-000")
        assert e.cep == "01001000"

    def test_invalid_cep_too_short_raises(self):
        with pytest.raises(ValueError):
            self._make(cep="9999")

    def test_invalid_cep_too_long_raises(self):
        with pytest.raises(ValueError):
            self._make(cep="010010000")

    def test_invalid_uf_raises(self):
        with pytest.raises(ValueError):
            self._make(uf="XX")

    def test_is_immutable(self):
        e = self._make()
        with pytest.raises((AttributeError, TypeError)):
            e.cep = "99999999"

    def test_all_valid_ufs_accepted(self):
        valid_ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                     "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
                     "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        for uf in valid_ufs:
            e = self._make(uf=uf)
            assert e.uf == uf


class TestImposto:
    def test_stores_all_tax_fields(self):
        imp = Imposto(icms=10.0, ipi=5.0, pis=2.0, cofins=1.0)
        assert imp.icms == 10.0
        assert imp.ipi == 5.0
        assert imp.pis == 2.0
        assert imp.cofins == 1.0

    def test_total_geral_sums_all_taxes(self):
        imp = Imposto(icms=10.0, ipi=5.0, pis=2.0, cofins=1.0)
        assert imp.total_geral == 18.0

    def test_total_geral_with_zero_taxes(self):
        imp = Imposto(icms=0.0, ipi=0.0, pis=0.0, cofins=0.0)
        assert imp.total_geral == 0.0

    def test_total_geral_fractional_values(self):
        imp = Imposto(icms=1.1, ipi=2.2, pis=3.3, cofins=4.4)
        assert abs(imp.total_geral - 11.0) < 1e-9

    def test_is_immutable(self):
        imp = Imposto(icms=10.0, ipi=5.0, pis=0.0, cofins=0.0)
        with pytest.raises((AttributeError, TypeError)):
            imp.icms = 99.0
