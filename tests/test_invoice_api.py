def test_emit_invoice_returns_201_with_chave_and_itens(client, invoice_payload):
    response = client.post("/invoices/", json=invoice_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["chave_acesso"]
    assert isinstance(data["itens"], list) and len(data["itens"]) == 1


def test_emit_invoice_status_is_autorizada(client, invoice_payload):
    response = client.post("/invoices/", json=invoice_payload)
    assert response.json()["status"] == "AUTORIZADA"


def test_list_invoices_returns_emitted_nota(client, invoice_payload):
    client.post("/invoices/", json=invoice_payload)
    resp = client.get("/invoices/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_get_invoice_by_chave(client, invoice_payload):
    chave = client.post("/invoices/", json=invoice_payload).json()["chave_acesso"]
    resp = client.get(f"/invoices/{chave}")
    assert resp.status_code == 200
    assert resp.json()["chave_acesso"] == chave


def test_cancel_invoice_returns_cancelada(client, invoice_payload):
    chave = client.post("/invoices/", json=invoice_payload).json()["chave_acesso"]
    resp = client.post(f"/invoices/{chave}/cancel")
    assert resp.status_code == 200
    assert resp.json()["status"] == "CANCELADA"


def test_correction_on_autorizada_returns_200(client, invoice_payload):
    chave = client.post("/invoices/", json=invoice_payload).json()["chave_acesso"]
    resp = client.post(f"/invoices/{chave}/correction", json={"texto_correcao": "Correcao valida"})
    assert resp.status_code == 200


def test_get_invoice_not_found(client):
    resp = client.get(f"/invoices/{'0' * 44}")
    assert resp.status_code == 404


def test_cancel_invoice_not_found(client):
    resp = client.post(f"/invoices/{'0' * 44}/cancel")
    assert resp.status_code == 404


def test_correction_invoice_not_found(client):
    resp = client.post(
        f"/invoices/{'0' * 44}/correction",
        json={"texto_correcao": "Texto"},
    )
    assert resp.status_code == 404


def test_correction_on_cancelada_returns_400(client, invoice_payload):
    chave = client.post("/invoices/", json=invoice_payload).json()["chave_acesso"]
    client.post(f"/invoices/{chave}/cancel")
    resp = client.post(f"/invoices/{chave}/correction", json={"texto_correcao": "Texto"})
    assert resp.status_code == 400


def test_emit_invoice_item_total_is_correct(client, invoice_payload):
    data = client.post("/invoices/", json=invoice_payload).json()
    item = data["itens"][0]
    assert item["total"] == item["quantidade"] * item["valor_unitario"]


def test_emit_invoice_invalid_cnpj_returns_422(client, invoice_payload):
    invoice_payload["emitente_cnpj"] = "123"
    resp = client.post("/invoices/", json=invoice_payload)
    assert resp.status_code == 422


def test_emit_invoice_empty_itens_returns_422(client, invoice_payload):
    invoice_payload["itens"] = []
    resp = client.post("/invoices/", json=invoice_payload)
    assert resp.status_code == 422
