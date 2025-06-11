from core.entities.nota_fiscal import NotaFiscal
from core.enum.status_nota import StatusNota
from core.services.emissao_nota_port import EmissaoNotaPort
from infrastructure.external_services.sefaz_client import SefazClient
from infrastructure.external_services.signer import Signer

class NotaFiscalEmissaoAdapter(EmissaoNotaPort):
    def __init__(self, sefaz_client: SefazClient, signer: Signer):
        self.sefaz_client = sefaz_client
        self.signer = signer

    def emitir(self, nota: NotaFiscal) -> NotaFiscal:
        xml = self.sefaz_client.generate_xml(nota)
        signed_xml = self.signer.sign(xml)
        response = self.sefaz_client.send_xml(signed_xml)
        if response.status == 'AUTORIZADO':
            nota.chave_acesso = response.access_key
            nota.protocolo_autorizacao = response.protocol_number
            nota.status = StatusNota.AUTORIZADA
        else:
            nota.status = StatusNota.REJEITADA
        return nota
