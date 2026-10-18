from fastapi.testclient import TestClient

from main import app, puntaje_fraude

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"estado": "ok"}


def test_pago_valido():
    r = client.post("/api/pagos", json={"monto": 50000, "comercio": "Tienda Uno"})
    assert r.status_code == 200
    assert r.json()["decision"] in {"aprobado", "revision", "rechazado"}


def test_pago_monto_negativo_rechazado():
    r = client.post("/api/pagos", json={"monto": -10, "comercio": "Tienda Uno"})
    assert r.status_code == 422


def test_puntaje_en_rango():
    for monto in (1000, 100000, 10000000):
        assert 0 <= puntaje_fraude(monto) <= 1
