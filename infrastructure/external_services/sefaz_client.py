# infrastructure/external_services/sefaz_client.py
"""
Client stub for interacting with SEFAZ web services.
Provides methods to generate XML and send requests for NF-e, cancellation, and CC-e.
This stub now generates unique keys to avoid duplicates.
"""
import uuid
from random import randint
from typing import NamedTuple

from fastapi import Depends

from app.interfaces.controllers.invoice_controller import InvoiceResponseSchema, router
from core.entities.nota_fiscal import NotaFiscal
from core.services.ports.nota_fiscal_repository_port import NotaFiscalRepository


class SefazResponse(NamedTuple):
    status: str
    access_key: str
    protocol_number: str

class SefazClient:
    def generate_xml(self, nota: NotaFiscal) -> str:
        """
        Converte a entidade NotaFiscal em XML conforme layout NF-e.
        """
        # TODO: implementar conversão real para XML
        return f"<nfe><id>{nota.id}</id></nfe>"

    def send_xml(self, signed_xml: str) -> SefazResponse:
        """
        Envia o XML assinado ao SEFAZ para autorização.
        Gera valores únicos para chave de acesso e protocolo.
        """
        # Gera chave de acesso única de 44 caracteres
        unique_access_key = uuid.uuid4().hex[:44].ljust(44, '0')
        # Gera protocolo aleatório de 9 dígitos
        protocol_number = str(randint(100000000, 999999999))
        return SefazResponse(status="AUTORIZADO", access_key=unique_access_key, protocol_number=protocol_number)

    def generate_cancel_xml(self, access_key: str) -> str:
        """
        Gera XML de cancelamento conforme layout NF-e.
        """
        return f"<cancel><key>{access_key}</key></cancel>"

    def send_cancel(self, signed_xml: str) -> SefazResponse:
        """
        Envia XML de cancelamento ao SEFAZ.
        """
        protocol_number = str(randint(100000000, 999999999))
        return SefazResponse(status="CANCELADO", access_key=signed_xml, protocol_number=protocol_number)

    def generate_cce_xml(self, access_key: str, correction_text: str) -> str:
        """
        Gera XML de Carta de Correção Eletrônica (CC-e).
        """
        return f"<cce><key>{access_key}</key><text>{correction_text}</text></cce>"

    def send_cce(self, signed_xml: str) -> SefazResponse:
        """
        Envia XML de CC-e ao SEFAZ.
        """
        protocol_number = str(randint(100000000, 999999999))
        return SefazResponse(status="CCE_AUTORIZADA", access_key=signed_xml, protocol_number=protocol_number)

