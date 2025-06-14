from core.services.ports.carta_correcao_port import CartaCorrecaoPort
from infrastructure.external_services.sefaz_client import SefazClient

class NotaFiscalCorreccaoAdapter(CartaCorrecaoPort):
    def __init__(self, client: SefazClient):
        self.client = client

    def corrigir(self, chave_acesso: str, texto_correcao: str):
        xml = self.client.generate_cce_xml(chave_acesso, texto_correcao)
        response = self.client.send_cce(xml)
        return response
