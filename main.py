from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="FinTech Nova - Motor de Riesgo",
    version="1.0.0"
)
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

