import pytest
from unittest.mock import MagicMock

from application.use_cases.cancel_invoice import CancelInvoiceUseCase
from application.use_cases.correct_invoice import CorrectionInvoiceUseCase
from application.use_cases.emit_invoice import EmitInvoiceUseCase
from core.entities.nota_fiscal import NotaFiscal
from core.enum.status_nota import StatusNota
from core.exceptions.domain_exceptions import DomainException, NotaNaoEncontradaException
from core.value_objects.cnpjcpf import CnpjCpf
from core.value_objects.endereço import Endereco


def _make_nota(chave: str = None, status: StatusNota = StatusNota.AUTORIZADA) -> NotaFiscal:
    nota = NotaFiscal(
        emitente_cnpj=CnpjCpf("12345678000199"),
        destinatario_cnpj=CnpjCpf("98765432000100"),
        emitente_endereco=Endereco("Av. X", "1", "SP", "SP", "01001000"),
        destinatario_endereco=Endereco("Rua Y", "2", "RJ", "RJ", "20020000"),
    )
    nota.chave_acesso = chave or "A" * 44
    nota.status = status
    return nota


class TestEmitInvoiceUseCase:
    def test_calls_emissor_and_saves_to_repo(self):
        nota = _make_nota()
        emissor = MagicMock()
        emissor.emitir.return_value = nota
        repo = MagicMock()

        result = EmitInvoiceUseCase(emissor, repo).execute(nota)

        emissor.emitir.assert_called_once_with(nota)
        repo.save.assert_called_once_with(nota)
        assert result is nota

    def test_returns_nota_from_emissor(self):
        input_nota = _make_nota(chave="B" * 44, status=StatusNota.EM_PROCESSAMENTO)
        emitted = _make_nota(chave="C" * 44, status=StatusNota.AUTORIZADA)

        emissor = MagicMock()
        emissor.emitir.return_value = emitted
        repo = MagicMock()

        result = EmitInvoiceUseCase(emissor, repo).execute(input_nota)

        assert result.status == StatusNota.AUTORIZADA
        assert result.chave_acesso == "C" * 44

    def test_save_receives_the_emitted_nota(self):
        input_nota = _make_nota()
        emitted = _make_nota(chave="D" * 44)

        emissor = MagicMock()
        emissor.emitir.return_value = emitted
        repo = MagicMock()

        EmitInvoiceUseCase(emissor, repo).execute(input_nota)

        repo.save.assert_called_once_with(emitted)


class TestCancelInvoiceUseCase:
    def test_cancels_nota_and_updates_status(self):
        chave = "E" * 44
        nota = _make_nota(chave=chave, status=StatusNota.AUTORIZADA)
        cancel_result = _make_nota(chave=chave, status=StatusNota.CANCELADA)
        cancel_result.protocolo_autorizacao = "123456789"

        cancel_port = MagicMock()
        cancel_port.cancelar.return_value = cancel_result
        repo = MagicMock()
        repo.get_by_chave.return_value = nota

        result = CancelInvoiceUseCase(cancel_port, repo).execute(chave)

        repo.get_by_chave.assert_called_once_with(chave)
        cancel_port.cancelar.assert_called_once_with(chave)
        repo.save.assert_called_once_with(nota)
        assert result.status == StatusNota.CANCELADA

    def test_updates_protocolo_on_original_nota(self):
        chave = "F" * 44
        nota = _make_nota(chave=chave)
        cancel_result = _make_nota(chave=chave, status=StatusNota.CANCELADA)
        cancel_result.protocolo_autorizacao = "999888777"

        cancel_port = MagicMock()
        cancel_port.cancelar.return_value = cancel_result
        repo = MagicMock()
        repo.get_by_chave.return_value = nota

        result = CancelInvoiceUseCase(cancel_port, repo).execute(chave)

        assert result.protocolo_autorizacao == "999888777"

    def test_raises_when_nota_not_found(self):
        cancel_port = MagicMock()
        repo = MagicMock()
        repo.get_by_chave.return_value = None

        with pytest.raises(NotaNaoEncontradaException):
            CancelInvoiceUseCase(cancel_port, repo).execute("0" * 44)

    def test_does_not_call_cancel_port_when_nota_missing(self):
        cancel_port = MagicMock()
        repo = MagicMock()
        repo.get_by_chave.return_value = None

        with pytest.raises(NotaNaoEncontradaException):
            CancelInvoiceUseCase(cancel_port, repo).execute("0" * 44)

        cancel_port.cancelar.assert_not_called()


class TestCorrectionInvoiceUseCase:
    def test_corrects_autorizada_nota_and_saves(self):
        chave = "G" * 44
        nota = _make_nota(chave=chave, status=StatusNota.AUTORIZADA)
        correction_result = MagicMock()
        correction_result.protocol_number = "CCE-001"

        correction_port = MagicMock()
        correction_port.corrigir.return_value = correction_result
        repo = MagicMock()
        repo.get_by_chave.return_value = nota

        result = CorrectionInvoiceUseCase(correction_port, repo).execute(chave, "Texto correcao")

        correction_port.corrigir.assert_called_once_with(chave, "Texto correcao")
        repo.save.assert_called_once_with(nota)
        assert result.protocolo_cce == "CCE-001"

    def test_raises_when_nota_not_found(self):
        correction_port = MagicMock()
        repo = MagicMock()
        repo.get_by_chave.return_value = None

        with pytest.raises(NotaNaoEncontradaException):
            CorrectionInvoiceUseCase(correction_port, repo).execute("0" * 44, "Texto")

    def test_raises_when_nota_is_not_autorizada(self):
        chave = "H" * 44
        for status in (StatusNota.EM_PROCESSAMENTO, StatusNota.REJEITADA, StatusNota.CANCELADA):
            nota = _make_nota(chave=chave, status=status)
            correction_port = MagicMock()
            repo = MagicMock()
            repo.get_by_chave.return_value = nota

            with pytest.raises(DomainException):
                CorrectionInvoiceUseCase(correction_port, repo).execute(chave, "Texto")

    def test_does_not_call_correction_port_when_nota_missing(self):
        correction_port = MagicMock()
        repo = MagicMock()
        repo.get_by_chave.return_value = None

        with pytest.raises(NotaNaoEncontradaException):
            CorrectionInvoiceUseCase(correction_port, repo).execute("0" * 44, "Texto")

        correction_port.corrigir.assert_not_called()
