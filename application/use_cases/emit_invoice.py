
from core.entities.nota_fiscal import NotaFiscal
from core.services.ports.emissao_nota_port import EmissaoNotaPort
from core.services.ports.nota_fiscal_repository_port import NotaFiscalRepository


class EmitInvoiceUseCase:

    def __init__(
        self,
        emissor: EmissaoNotaPort,
        repository: NotaFiscalRepository,
    ):
        self.emissor = emissor
        self.repository = repository

    def execute(self, nota: NotaFiscal) -> NotaFiscal:
        """
        Executes the emission process and saves the result.

        Args:
            nota (NotaFiscal): the domain entity with all required data.

        Returns:
            NotaFiscal: the updated entity with status, chave_acesso, protocolo_autorizacao.
        """
        # Trigger external emission (XML generation, signing, sending)
        nota_emitida = self.emissor.emitir(nota)
        # Persist the updated entity
        self.repository.save(nota_emitida)
        return nota_emitida
