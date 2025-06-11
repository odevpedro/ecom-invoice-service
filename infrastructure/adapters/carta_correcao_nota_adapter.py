from core.entities.nota_fiscal import NotaFiscal
from core.enum.status_nota import StatusNota
from infrastructure.external_services.sefaz_client import SefazClient
from infrastructure.external_services.signer import Signer
from core.services.ports.carta_correcao_port import CartaCorrecaoPort


class NotaFiscalCartaCorrecaoAdapter(CartaCorrecaoPort):
    def __init__(self, sefaz_client: SefazClient, signer: Signer):
        self.sefaz_client = sefaz_client
        self.signer = signer

    def corrigir(self, chave_acesso: str, texto_correcao: str) -> NotaFiscal:
        xml = self.sefaz_client.generate_cce_xml(chave_acesso, texto_correcao)
        signed = self.signer.sign(xml)
        response = self.sefaz_client.send_cce(signed)
        nota = NotaFiscal(
            emitente_cnpj=None,
            destinatario_cnpj=None,
            emitente_endereco=None,
            destinatario_endereco=None
        )
        nota.chave_acesso = chave_acesso
        nota.status = StatusNota.AUTORIZADA if response.status == 'CCE_AUTORIZADA' else StatusNota.REJEITADA
        return nota
