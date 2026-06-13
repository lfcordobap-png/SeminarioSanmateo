# FinTech Nova - Motor de Riesgo

API desarrollada con FastAPI para practicar conceptos de seguridad en aplicaciones web y demostrar un flujo básico de evaluación de riesgo crediticio.

## Descripción

Esta aplicación ofrece una API sencilla que incluye:

- Un endpoint de bienvenida.
- Un endpoint de estado del servicio.
- Un ejemplo de consulta vulnerable a SQL injection.
- Un ejemplo equivalente usando consultas parametrizadas.
- Un endpoint para simular la evaluación de riesgo de un crédito.
- Un endpoint para consultar datos financieros de ejemplo.

Además, la API añade cabeceras de seguridad mediante middleware para reforzar la configuración básica de la aplicación.

## Requisitos

- Python 3.9 o superior
- pip
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

## Estructura del proyecto

```text
.
├── main.py
├── requirements.txt
├── README.md
└── docs/
```

## Ejecución

Iniciar la API con:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Si el puerto 8000 está ocupado, puede cambiarse por otro, por ejemplo:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## Endpoints disponibles

### GET /

Devuelve un mensaje de bienvenida.

Ejemplo de respuesta:

```json
{
  "mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."
}
```

### GET /status

Verifica si el servicio se encuentra operativo.

Ejemplo de respuesta:

```json
{
  "estado": "Operacional",
  "servidor": "Node-01"
}
```

### GET /vulnerable/users/{username}

Ejemplo académico de una consulta vulnerable a SQL injection.

Ejemplo:

```http
GET /vulnerable/users/admin
```

### GET /secure/users/{username}

Versión segura de la consulta anterior usando parámetros preparados.

Ejemplo:

```http
GET /secure/users/admin
```

### POST /evaluar-riesgo

Simula una evaluación de riesgo crediticio a partir de los datos enviados.

Body de ejemplo:

```json
{
  "edad": 35,
  "ingreso": 2500,
  "deudas": 800
}
```

Respuesta esperada:

```json
{
  "resultado": "En Revision",
  "score_simulado": 1700
}
```

### GET /datos-financieros/{id_cliente}

Devuelve un ejemplo de información financiera para un cliente.

Ejemplo:

```http
GET /datos-financieros/101
```

## Documentación automática

FastAPI genera documentación interactiva en:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## Dependencias

- fastapi
- uvicorn
- pydantic
