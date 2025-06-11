from core.entities.nota_fiscal import NotaFiscal
from core.enum.status_nota import StatusNota
from core.services.ports.cancelamento_nota_port import CancelamentoNotaPort
from infrastructure.external_services.sefaz_client import SefazClient
from infrastructure.external_services.signer import Signer

class NotaFiscalCancelamentoAdapter(CancelamentoNotaPort):
    def __init__(self, sefaz_client: SefazClient, signer: Signer):
        self.sefaz_client = sefaz_client
        self.signer = signer

    def cancelar(self, chave_acesso: str) -> NotaFiscal:
        xml = self.sefaz_client.generate_cancel_xml(chave_acesso)
        signed = self.signer.sign(xml)
        response = self.sefaz_client.send_cancel(signed)
        nota = NotaFiscal(
            emitente_cnpj=None,
            destinatario_cnpj=None,
            emitente_endereco=None,
            destinatario_endereco=None
        )
        nota.chave_acesso = chave_acesso
        nota.protocolo_autorizacao = response.protocol_number
        nota.status = StatusNota.CANCELADA if response.status == 'CANCELADO' else StatusNota.REJEITADA
        return nota