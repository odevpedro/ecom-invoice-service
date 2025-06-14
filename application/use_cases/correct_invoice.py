# application/use_cases/correct_invoice.py
"""
Use case para Carta de Correção Eletrônica (CC-e) de uma Nota Fiscal.
"""
from core.entities.nota_fiscal import NotaFiscal
from core.exceptions.domain_exceptions import NotaNaoEncontradaException, DomainException
from core.services.ports.carta_correcao_port import CartaCorrecaoPort
from core.services.ports.nota_fiscal_repository_port import NotaFiscalRepository

class CorrectionInvoiceUseCase:
    """
    1) Busca a NotaFiscal autorizada.
    2) Valida se status == AUTORIZADA.
    3) Envia correção para SEFAZ via CartaCorrecaoPort.
    4) Atualiza protocolo_cce na entidade e persiste.
    """
    def __init__(
        self,
        correction_port: CartaCorrecaoPort,
        repository: NotaFiscalRepository,
    ):
        self.correction_port = correction_port
        self.repository = repository

    def execute(self, chave_acesso: str, texto_correcao: str) -> NotaFiscal:
        nota = self.repository.get_by_chave(chave_acesso)
        if not nota:
            raise NotaNaoEncontradaException(f"Nota com chave {chave_acesso} não encontrada.")

        if nota.status.value != "AUTORIZADA":
            raise DomainException("Somente notas autorizadas podem receber Carta de Correção.")

        # Dispara correção
        resultado = self.correction_port.corrigir(chave_acesso, texto_correcao)

        # Atualiza entidade (mantém status original)
        nota.protocolo_cce = resultado.protocol_number
        # persiste
        self.repository.save(nota)
        return nota
