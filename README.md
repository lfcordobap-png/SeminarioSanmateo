# FinTech Nova - Motor de Riesgo

API sencilla desarrollada con FastAPI para evaluación de riesgo crediticio y prácticas de desarrollo con endpoints básicos.

## Descripción

Esta API incluye:

- Endpoint principal de bienvenida.
- Endpoint de verificación de estado (health check).
- Endpoint de consulta de datos de usuarios.
- Base de datos simulada en memoria.

> **Nota:** El endpoint `/datos-sensibles/{usuario}` es intencionalmente sencillo y se usa para fines académicos sobre control de acceso y autenticación.

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
  "status": "ok",
  "servicios": "operativos"
}
```

### GET /datos-sensibles/{usuario}

Devuelve información de usuario de la base de datos simulada.

Ejemplo:

```http
GET /datos-sensibles/user1
```

Ejemplo de respuesta:

```json
{
  "usuario": "user1",
  "estado": "Activo",
  "datos_financieros": "Confidencial"
}
```

## Usuarios Disponibles

- `user1` — Activo
- `user2` — Inactivo

## Documentación Automática

FastAPI genera documentación interactiva automáticamente en:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Objetivos Educativos

- Aprender la creación de APIs con FastAPI.
- Practicar despliegue local con Uvicorn.
- Revisar control de acceso y seguridad básica en endpoints.

## Dependencias

- `fastapi`
- `uvicorn`
