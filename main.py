import sqlite3
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel #primera clase
from health_check import run_all_checks

 
app = FastAPI(title="FinTech Nova - Secure API Practice")

@app.get('/health')
def health_check_endpoint():
    """
    Endpoint de verificación de salud del sistema.
    Retorna 200 OK si todo está bien, 503 Service Unavailable si hay problemas.
    Los orquestadores (Kubernetes, Docker) consultan este endpoint para decidir
    si deben enviar tráfico o reiniciar el servicio.
    """
    result = run_all_checks()
    if result['status'] == 'unhealthy':
        raise HTTPException(status_code=503, detail=result)
    return result  # FastAPI convierte el dict a JSON automáticamente
 
#middleware de seguridad
 
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
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
 
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."}
 
 
#Enpoint vulnerable a sql injection
@app.get("/vulnerable/users/{username}")
def get_user_vulnerable(username: str):
    conn = get_db()
    cursor = conn.cursor()
    # ⚠️ NUNCA HACER ESTO: Concatenación directa
    query = f"SELECT * FROM users WHERE username = '{username}'"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return {"query_ejecutada": query, "resultado": result}
    except Exception as e:
        return {"error": str(e)}
 
# --- 4. ENDPOINT SEGURO (Prepared Statements) 
@app.get("/secure/users/{username}")
def get_user_secure(username: str):
    conn = get_db()
    cursor = conn.cursor()
    # ✅ FORMA SEGURA: Parametrización
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    return {"query_ejecutada": query, "resultado": result}

##Primera clase ___________________________________________
class SolicitudCredito(BaseModel): 
    edad: int 
    ingreso :float
    deudas :float

@app.get("/status")
def get_status():
    return {"estado":"Operacional","servidor": "Node-01"}

@app.post("/evaluar-riesgo") 
def evaluar_riesgo(solicitud: SolicitudCredito): 
    score = solicitud.ingreso - solicitud.deudas 
    if solicitud.edad < 18:
        resultado = "Rechazado (Menor de edad)" 
    elif score > 1000: 
        resultado = "Aprobado"  
    else: 
        resultado = "En Revision"  
    return {"resultado": resultado, "score_simulado": score} 
    
@app.get("/datos-financieros/{id_cliente}") 
def obtener_historial(id_cliente: int): 
        return { 
        "cliente_id": id_cliente, 
        "historial": "Limpio", 
        "score_interno": 750 
    } 
 