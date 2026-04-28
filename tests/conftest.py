import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

from unittest.mock import MagicMock, patch
from typing import Dict, List, Optional

import pytest
from fastapi.testclient import TestClient

_patcher = patch("sqlalchemy.schema.MetaData.create_all", MagicMock())
_patcher.start()

from app.main import app  # noqa: E402
from app.interfaces.controllers.invoice_controller import (  # noqa: E402
    get_cancel_use_case,
    get_correction_use_case,
    get_emit_use_case,
    get_repository,
)
from application.use_cases.cancel_invoice import CancelInvoiceUseCase  # noqa: E402
from application.use_cases.correct_invoice import CorrectionInvoiceUseCase  # noqa: E402
from application.use_cases.emit_invoice import EmitInvoiceUseCase  # noqa: E402
from core.entities.nota_fiscal import NotaFiscal  # noqa: E402
from core.services.ports.nota_fiscal_repository_port import NotaFiscalRepository  # noqa: E402
from infrastructure.adapters.cancelamento_nota_adapter import NotaFiscalCancelamentoAdapter  # noqa: E402
from infrastructure.adapters.carta_correcao_nota_adapter import NotaFiscalCorreccaoAdapter  # noqa: E402
from infrastructure.adapters.emissao_nota_adapter import NotaFiscalEmissaoAdapter  # noqa: E402
from infrastructure.external_services.sefaz_client import SefazClient  # noqa: E402
from infrastructure.external_services.signer import Signer  # noqa: E402

_patcher.stop()


class InMemoryRepository(NotaFiscalRepository):
    def __init__(self):
        self._store: Dict[str, NotaFiscal] = {}

    def save(self, nota: NotaFiscal) -> None:
        self._store[nota.chave_acesso] = nota

    def get_by_chave(self, chave_acesso: str) -> Optional[NotaFiscal]:
        return self._store.get(chave_acesso)

    def list_all(self) -> List[NotaFiscal]:
        return list(self._store.values())


@pytest.fixture
def repo():
    return InMemoryRepository()


@pytest.fixture
def client(repo):
    app.dependency_overrides[get_emit_use_case] = lambda: EmitInvoiceUseCase(
        NotaFiscalEmissaoAdapter(SefazClient(), Signer()), repo
    )
    app.dependency_overrides[get_cancel_use_case] = lambda: CancelInvoiceUseCase(
        NotaFiscalCancelamentoAdapter(SefazClient(), Signer()), repo
    )
    app.dependency_overrides[get_correction_use_case] = lambda: CorrectionInvoiceUseCase(
        NotaFiscalCorreccaoAdapter(SefazClient()), repo
    )
    app.dependency_overrides[get_repository] = lambda: repo

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def invoice_payload():
    return {
        "emitente_cnpj": "12345678000199",
        "destinatario_cnpj": "98765432000100",
        "emitente_endereco": {
            "logradouro": "Av. Exemplo",
            "numero": "1000",
            "municipio": "Cidade",
            "uf": "SP",
            "cep": "01001000",
            "complemento": "Sala 1",
            "bairro": "Centro",
        },
        "destinatario_endereco": {
            "logradouro": "Rua Teste",
            "numero": "200",
            "municipio": "Outra",
            "uf": "RJ",
            "cep": "20020000",
            "complemento": "",
            "bairro": "Bairro",
        },
        "itens": [
            {
                "sku": "ABC123",
                "descricao": "Produto Teste",
                "quantidade": 2,
                "valor_unitario": 50.0,
                "cfop": "5102",
                "ncm": "12345678",
                "cst": "102",
                "impostos": {"icms": 10.0, "ipi": 5.0, "pis": 0.0, "cofins": 0.0},
            }
        ],
    }
