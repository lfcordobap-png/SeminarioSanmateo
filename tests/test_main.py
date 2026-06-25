import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

VALID_TOKEN = "secret-token-fintech"
ADMIN_TOKEN = "admin-token-fintech"


# ── Endpoints públicos ────────────────────────────────────────

def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert "mensaje" in response.json()


def test_status_operacional():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["estado"] == "Operacional"


def test_health_returns_valid_status():
    response = client.get("/health")
    assert response.status_code in [200, 503]
    body = response.json()
    if response.status_code == 200:
        assert body["status"] in ["healthy", "degraded"]
    else:
        assert "detail" in body


# ── Security headers ─────────────────────────────────────────

def test_security_headers_presentes():
    response = client.get("/")
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "SAMEORIGIN"
    assert response.headers.get("x-xss-protection") == "1; mode=block"
    assert "content-security-policy" in response.headers


# ── SQL injection educativo ───────────────────────────────────

def test_vulnerable_users_responde():
    response = client.get("/vulnerable/users/admin")
    assert response.status_code == 200
    assert "query_ejecutada" in response.json()


def test_secure_users_responde():
    response = client.get("/secure/users/admin")
    assert response.status_code == 200
    assert "resultado" in response.json()


def test_secure_users_usuario_inexistente():
    response = client.get("/secure/users/noexiste")
    assert response.status_code == 200
    assert response.json()["resultado"] == []


# ── Evaluación de riesgo ─────────────────────────────────────

def test_evaluar_riesgo_aprobado():
    response = client.post("/evaluar-riesgo", json={"edad": 30, "ingreso": 2500.0, "deudas": 1000.0})
    assert response.status_code == 200
    assert response.json()["resultado"] == "Aprobado"
    assert response.json()["score_simulado"] == 1500.0


def test_evaluar_riesgo_menor_de_edad():
    response = client.post("/evaluar-riesgo", json={"edad": 16, "ingreso": 2500.0, "deudas": 0.0})
    assert response.status_code == 200
    assert "Rechazado" in response.json()["resultado"]


def test_evaluar_riesgo_en_revision():
    response = client.post("/evaluar-riesgo", json={"edad": 25, "ingreso": 800.0, "deudas": 600.0})
    assert response.status_code == 200
    assert response.json()["resultado"] == "En Revisión"


def test_evaluar_riesgo_campos_faltantes():
    response = client.post("/evaluar-riesgo", json={"edad": 30})
    assert response.status_code == 422


def test_evaluar_riesgo_tipos_invalidos():
    response = client.post("/evaluar-riesgo", json={"edad": "treinta", "ingreso": 2000.0, "deudas": 500.0})
    assert response.status_code == 422


# ── Endpoint protegido ────────────────────────────────────────

def test_datos_financieros_sin_token():
    response = client.get("/datos-financieros/1")
    assert response.status_code == 403


def test_datos_financieros_token_invalido():
    response = client.get("/datos-financieros/1", headers={"Authorization": "Bearer token-falso"})
    assert response.status_code == 401


def test_datos_financieros_token_valido():
    response = client.get("/datos-financieros/1", headers={"Authorization": f"Bearer {VALID_TOKEN}"})
    assert response.status_code == 200
    data = response.json()
    assert data["cliente_id"] == 1
    assert "historial" in data
    assert "score_interno" in data


def test_datos_financieros_admin_token():
    response = client.get("/datos-financieros/42", headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})
    assert response.status_code == 200
    assert response.json()["cliente_id"] == 42
