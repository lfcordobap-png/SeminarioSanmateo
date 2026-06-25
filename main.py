import os
import sqlite3
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from health_check import run_all_checks

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="FinTech Nova - Secure API Practice")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ===== AUTENTICACIÓN CON TOKEN =====
security = HTTPBearer()

VALID_TOKENS = [
    os.getenv("API_TOKEN", "secret-token-fintech"),
    os.getenv("ADMIN_TOKEN", "admin-token-fintech"),
]

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verifica que el token sea válido.
    Los tokens se leen desde variables de entorno API_TOKEN y ADMIN_TOKEN.
    """
    if credentials.credentials not in VALID_TOKENS:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

@app.get('/health')
def health_check_endpoint():
    """
    Endpoint de verificación de salud del sistema.
    Retorna 200 OK si todo está bien, 503 Service Unavailable si hay problemas.
    """
    result = run_all_checks()
    if result['status'] == 'unhealthy':
        raise HTTPException(status_code=503, detail=result)
    return result

# ===== MIDDLEWARE DE SEGURIDAD =====
DOCS_PATHS = {"/docs", "/redoc", "/openapi.json"}

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    if request.url.path in DOCS_PATHS:
        return response
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

def get_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
    cursor.executemany("INSERT INTO users (username, role) VALUES (?, ?)",
                       [("admin", "superadmin"), ("juan", "user"), ("maria", "user")])
    conn.commit()
    return conn

# ===== ENDPOINTS PÚBLICOS =====

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."}

@app.get("/status")
def get_status():
    return {"estado": "Operacional", "servidor": "Node-01"}

# ===== ENDPOINTS CON EJEMPLOS DE SEGURIDAD =====

@app.get("/vulnerable/users/{username}")
@limiter.limit("20/minute")
def get_user_vulnerable(request: Request, username: str):
    """
    ⚠️ EJEMPLO VULNERABLE A SQL INJECTION
    Este endpoint muestra cómo NO hacer consultas a BD.
    Solo para fines educativos.
    """
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return {"query_ejecutada": query, "resultado": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/secure/users/{username}")
@limiter.limit("20/minute")
def get_user_secure(request: Request, username: str):
    """
    ✅ ENDPOINT SEGURO CON PARAMETRIZACIÓN
    Usa prepared statements para prevenir SQL injection.
    """
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    return {"query_ejecutada": query, "resultado": result}

# ===== MODELO DE DATOS =====

class SolicitudCredito(BaseModel):
    edad: int
    ingreso: float
    deudas: float

# ===== ENDPOINT PROTEGIDO POR AUTENTICACIÓN =====

@app.get("/datos-financieros/{id_cliente}")
@limiter.limit("30/minute")
def obtener_historial(request: Request, id_cliente: int, token: str = Depends(verify_token)):
    """
    🔐 ENDPOINT PROTEGIDO - Requiere autenticación

    Uso:
    curl -H "Authorization: Bearer secret-token-fintech" \
         http://localhost:8000/datos-financieros/1

    Sin token o con token inválido: retorna 401 Unauthorized
    """
    return {
        "cliente_id": id_cliente,
        "historial": "Limpio",
        "score_interno": 750,
        "autorizado_por": "Token válido"
    }

# ===== ENDPOINT DE EVALUACIÓN DE CRÉDITO =====

@app.post("/evaluar-riesgo")
@limiter.limit("10/minute")
def evaluar_riesgo(request: Request, solicitud: SolicitudCredito):
    """
    Evalúa el riesgo crediticio de un solicitante.
    No requiere autenticación (es un endpoint de análisis público).
    Limitado a 10 peticiones por minuto por IP.
    """
    score = solicitud.ingreso - solicitud.deudas
    if solicitud.edad < 18:
        resultado = "Rechazado (Menor de edad)"
    elif score > 1000:
        resultado = "Aprobado"
    else:
        resultado = "En Revisión"
    return {"resultado": resultado, "score_simulado": score}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
