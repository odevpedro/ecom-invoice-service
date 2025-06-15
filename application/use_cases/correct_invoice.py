# application/use_cases/correct_invoice.py
"""
Caso de uso: Emissão de Carta de Correção Eletrônica.
"""
from core.entities.nota_fiscal import NotaFiscal
from core.exceptions.domain_exceptions import DomainException, NotaNaoEncontradaException
from core.enum.status_nota import StatusNota
from core.services.ports.carta_correcao_port import CartaCorrecaoPort
from core.services.persistence.nota_fiscal_model import NotaFiscalModel
from core.services.persistence.item_da_nota_model import ItemDaNotaModel
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
        # Recupera nota
        nota = self.repository.get_by_chave(chave_acesso)
        if nota is None:
            raise NotaNaoEncontradaException(f"Nota com chave {chave_acesso} não encontrada.")

        # Só nota autorizada pode receber correção
        if nota.status is not StatusNota.AUTORIZADA:
            raise DomainException("Somente notas autorizadas podem receber Carta de Correção.")

        # Dispara correção via port
        resultado = self.correction_port.corrigir(chave_acesso, texto_correcao)

        # Atualiza protocolo da correção na entidade
        nota.protocolo_cce = resultado.protocol_number

        # Persiste a alteração
        self.repository.save(nota)
        return nota
