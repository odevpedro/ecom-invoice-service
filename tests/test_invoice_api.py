import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

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
            "bairro": "Centro"
        },
        "destinatario_endereco": {
            "logradouro": "Rua Teste",
            "numero": "200",
            "municipio": "Outra",
            "uf": "RJ",
            "cep": "20020000",
            "complemento": "",
            "bairro": "Bairro"
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
                "impostos": {"icms": 10.0, "ipi": 5.0, "pis": 0.0, "cofins": 0.0}
            }
        ]
    }


def test_create_and_get_invoice(invoice_payload):
    response = client.post("/invoices", json=invoice_payload)
    assert response.status_code == 201
    data = response.json()
    assert "chave_acesso" in data and data["chave_acesso"]
    assert "itens" in data
    assert isinstance(data["itens"], list)


def test_list_invoices(invoice_payload):
    client.post("/invoices", json=invoice_payload)
    resp = client.get("/invoices")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_cancel_invoice(invoice_payload):
    create_resp = client.post("/invoices", json=invoice_payload)
    chave = create_resp.json()["chave_acesso"]
    cancel_resp = client.post(f"/invoices/{chave}/cancel")
    assert cancel_resp.status_code == 200
    cancel_data = cancel_resp.json()
    assert cancel_data["status"] == "CANCELADA"


def test_correction_allowed(invoice_payload):
    create_resp = client.post("/invoices", json=invoice_payload)
    chave = create_resp.json()["chave_acesso"]
    corr_resp = client.post(f"/invoices/{chave}/correction", json={"texto_correcao": "Teste"})
    assert corr_resp.status_code == 200


def test_get_not_found():
    invalid_key = "0" * 44
    resp = client.get(f"/invoices/{invalid_key}")
    assert resp.status_code == 404


def test_cancel_not_found():
    invalid_key = "0" * 44
    resp = client.post(f"/invoices/{invalid_key}/cancel")
    assert resp.status_code == 404


def test_correction_not_found():
    invalid_key = "0" * 44
    resp = client.post(f"/invoices/{invalid_key}/correction", json={"texto_correcao": "Teste"})
    assert resp.status_code == 404
