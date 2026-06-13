# FinTech Nova - Motor de Riesgo

API sencilla desarrollada con FastAPI para evaluación de riesgo crediticio y prácticas de seguridad en APIs.

## Descripción

Esta API incluye:

- Endpoint principal de bienvenida.
- Endpoint de verificación de estado.
- Endpoint vulnerable a SQL injection para demostraciones.
- Endpoint seguro con consultas parametrizadas.
- Endpoint de evaluación de riesgo con modelo Pydantic.
- Base de datos SQLite en memoria para ejemplos.

## Requisitos

- Python 3.9 o superior
- `pip`
- Entorno virtual recomendado

## Instalación

1. Crear el entorno virtual:

```bash
python -m venv env
```

2. Activar el entorno virtual:

```bash
source env/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```text
.
├── main.py
├── requirements.txt
└── README.md
```

## Ejecución

Inicie la API con:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Si el puerto `8000` ya está en uso, cambie el puerto:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## Endpoints Disponibles

### GET /

Devuelve un mensaje de bienvenida.

Ejemplo de respuesta:

```json
{
  "mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."
}
```

### GET /status

Verifica el estado de la API.

Ejemplo de respuesta:

```json
{
  "estado": "Operacional",
  "servidor": "Node-01"
}
```

### GET /vulnerable/users/{username}

Ejemplo vulnerable que construye la consulta SQL mediante concatenación directa.

Ejemplo de solicitud:

```http
GET /vulnerable/users/admin
```

Respuesta posible:

```json
{
  "query_ejecutada": "SELECT * FROM users WHERE username = 'admin'",
  "resultado": [[1, "admin", "superadmin"]]
}
```

> ⚠️ Este endpoint es solo para fines educativos. No use concatenación de strings con datos de usuario en SQL reales.

### GET /secure/users/{username}

Ejemplo seguro que usa consultas parametrizadas.

Ejemplo de solicitud:

```http
GET /secure/users/juan
```

Respuesta posible:

```json
{
  "query_ejecutada": "SELECT * FROM users WHERE username = ?",
  "resultado": [[2, "juan", "user"]]
}
```

### POST /evaluar-riesgo

Evalúa una solicitud de crédito mediante un modelo Pydantic.

Ejemplo de cuerpo:

```json
{
  "edad": 30,
  "ingreso": 2500.0,
  "deudas": 1200.0
}
```

Ejemplo de respuesta:

```json
{
  "resultado": "Aprobado",
  "score_simulado": 1300.0
}
```

### GET /datos-financieros/{id_cliente}

Devuelve un historial financiero simulado para un cliente.

Ejemplo de solicitud:

```http
GET /datos-financieros/1
```

Ejemplo de respuesta:

```json
{
  "cliente_id": 1,
  "historial": "Limpio",
  "score_interno": 750
}
```

## Usuarios Simulados

- `admin` — superadmin
- `juan` — user
- `maria` — user

## Documentación Automática

FastAPI genera documentación interactiva automáticamente en:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Objetivos Educativos

- Aprender a construir APIs con FastAPI.
- Explorar riesgos de SQL injection y soluciones con queries parametrizados.
- Usar Pydantic para validación de esquemas.
- Ejecutar un servidor Uvicorn local.

## Dependencias

- `fastapi`
- `uvicorn`
- `pydantic`

