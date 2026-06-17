# FinTech Nova - Secure API Practice

API educativa desarrollada con FastAPI para practicar validación de datos, consultas SQL seguras y medidas básicas de hardening en APIs.

## Qué incluye

- Ruta principal de bienvenida.
- Endpoint de estado del servicio.
- Ejemplo vulnerable a SQL injection para fines demostrativos.
- Ejemplo seguro con consultas parametrizadas.
- Evaluación simple de riesgo crediticio con Pydantic.
- Historial financiero simulado por cliente.
- Cabeceras de seguridad agregadas en cada respuesta.

## Requisitos

- Python 3.9 o superior.
- pip.
- Entorno virtual recomendado.

## Instalación

1. Crear el entorno virtual:

   python -m venv env

2. Activar el entorno virtual:

   source env/bin/activate

3. Instalar dependencias:

   pip install -r requirements.txt

## Estructura del proyecto

.
├── main.py
├── requirements.txt
├── README.md
├── backup_db.sh
├── backups/
└── docs/
    └── diagramas/

## Ejecución

Inicia la API con:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Si el puerto 8000 ya está en uso, usa otro valor de puerto.

## Endpoints

### GET /

Devuelve un mensaje de bienvenida.

Respuesta:

{
  "mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."
}

### GET /status

Retorna el estado operacional de la API.

Respuesta:

{
  "estado": "Operacional",
  "servidor": "Node-01"
}

### GET /vulnerable/users/{username}

Construye la consulta SQL mediante concatenación directa. Es un ejemplo inseguro y solo debe usarse con fines educativos.

### GET /secure/users/{username}

Usa consultas parametrizadas para evitar inyección SQL.

### POST /evaluar-riesgo

Evalúa una solicitud de crédito con este cuerpo:

{
  "edad": 30,
  "ingreso": 2500.0,
  "deudas": 1200.0
}

Respuesta posible:

{
  "resultado": "Aprobado",
  "score_simulado": 1300.0
}

### GET /datos-financieros/{id_cliente}

Devuelve un historial financiero simulado para el cliente solicitado.

## Usuarios simulados

- admin: superadmin
- juan: user
- maria: user

## Documentación automática

FastAPI expone documentación interactiva en:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## Notas técnicas

- La base de datos se crea en memoria en cada petición.
- La aplicación agrega cabeceras de seguridad como X-Content-Type-Options, X-Frame-Options, Content-Security-Policy y Strict-Transport-Security.
- El proyecto usa FastAPI, Uvicorn y Pydantic.

