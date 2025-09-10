from fastapi.testclient import TestClient
from app.main import app

Client = TestClient(app)

def test_criar_lista_obter_atualizacao_deletar_ticket():
    # criar
    novo = {
        "titulo": "erro NF-e",
        "descricao": "CEAN invalido ao emitir NFC-e",
        "solicitante": "Cliente X",
        "prioridade": "alta",
        "status": "aberto",
        "responsavel": "Luiz"
    }

    r = Client.post("/tickets/", json=novo)
    assert r.status_code == 201
    t = r.json()
    ticket_id = t["id"]

    # lista

    r = Client.get("/tickets/")
    assert r.status_code == 200
    assert any(item["id"] == ticket_id for item in r.json())

    # obter por id

    r = Client.get(f"/tickets/{ticket_id}")
    assert r.status_code == 200
    assert r.json()["titulo"] == "erro NF-e"

    # atualizar

    r = Client.patch(f"/tickets/{ticket_id}", json={"status": "em_andamento"})
    assert r.status_code == 200
    assert r.json()["status"] == "em_andamento"

    # delete

    r = Client.delete(f"/tickets/{ticket_id}")
    assert r.status_code == 204

    # conferir que sumiu
    r = Client.get(f"/tickets/{ticket_id}")
    assert r.status_code == 404