# application/use_cases/cancel_invoice.py
"""
Use case for canceling an invoice.
"""
from core.entities.nota_fiscal import NotaFiscal
from core.exceptions.domain_exceptions import NotaNaoEncontradaException
from core.services.ports.cancelamento_nota_port import CancelamentoNotaPort
from core.services.ports.nota_fiscal_repository_port import NotaFiscalRepository

class CancelInvoiceUseCase:
    """
    Orchestrates the invoice cancellation workflow:
    1) Retrieves the existing NotaFiscal by access key.
    2) Calls the CancelamentoNotaPort to send the cancellation to SEFAZ.
    3) Persists the updated NotaFiscal with status CANCELADA or REJEITADA.
    """
    def __init__(
        self,
        cancel_port: CancelamentoNotaPort,
        repository: NotaFiscalRepository,
    ):
        self.cancel_port = cancel_port
        self.repository = repository

    def execute(self, chave_acesso: str) -> NotaFiscal:
        """
        Executes the cancellation process for a given access key.

        Args:
            chave_acesso (str): the NF-e access key to be canceled.

        Returns:
            NotaFiscal: the updated entity with status CANCELADA or REJEITADA.

        Raises:
            NotaNaoEncontradaException: if no invoice is found for the key.
        """
        # 1. Retrieve original entity
        nota = self.repository.get_by_chave(chave_acesso)
        if not nota:
            raise NotaNaoEncontradaException(f"Nota com chave {chave_acesso} não encontrada.")

        # 2. Trigger external cancellation on stub
        nota_result = self.cancel_port.cancelar(chave_acesso)

        # 3. Update only status and protocol on original nota
        nota.status = nota_result.status
        nota.protocolo_autorizacao = nota_result.protocolo_autorizacao

        # 4. Persist the updated entity
        self.repository.save(nota)
        return nota
