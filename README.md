# 🏦 FinTech Nova - Secure API Practice

API educativa desarrollada con **FastAPI** para practicar validación de datos, consultas SQL seguras, autenticación y medidas de hardening en APIs. Diseñada como caso de estudio para el **Proyecto Final Integrador: Arquitectura, Seguridad y Automatización de una API en la Nube**.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación Rápida](#-instalación-rápida)
- [Ejecución](#-ejecución)
- [Arquitectura](#-arquitectura)
- [Endpoints](#-endpoints)
- [Autenticación](#-autenticación)
- [Testing](#-testing)
- [Seguridad](#-seguridad)
- [Docker](#-docker)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🎯 Descripción

**FinTech Nova** es una API de predicción de riesgo crediticio que simula un servicio financiero real. El proyecto demuestra:

- ✅ Arquitectura moderna en la nube (GitHub Codespaces)
- ✅ Autenticación y control de acceso (Bearer Token)
- ✅ Prevención de SQL Injection (Prepared Statements)
- ✅ Headers de seguridad HTTP
- ✅ Rate limiting por IP
- ✅ Tests automatizados con pytest
- ✅ Contenerización con Docker y Docker Compose
- ✅ CI/CD con GitHub Actions

---

## ✨ Características

| Característica | Descripción | Status |
|---|---|---|
| **Autenticación Bearer Token** | Protege endpoints sensibles con tokens por env var | ✅ |
| **Endpoints de Análisis** | Evaluación crediticia y datos financieros | ✅ |
| **Ejemplos de Seguridad** | Vulnerable vs. Secure lado a lado | ✅ |
| **Headers de Seguridad** | HSTS, CSP, X-Frame-Options, etc. | ✅ |
| **Rate Limiting** | Límite de peticiones por IP con slowapi | ✅ |
| **Health Check** | Monitoreo automático del sistema | ✅ |
| **Tests Automatizados** | Suite de 16 tests con pytest | ✅ |
| **Docker / Docker Compose** | Contenerización lista para producción | ✅ |
| **GitHub Actions** | Pipeline CI/CD con tests y auditoría de seguridad | ✅ |
| **Documentación** | Swagger UI y ReDoc integrados | ✅ |

---

## 📦 Requisitos

- **Python:** 3.9 o superior (3.12 recomendado)
- **pip:** Gestor de paquetes de Python
- **Docker:** (Opcional) Para ejecución en contenedores
- **Git:** Para control de versiones

---

## 🚀 Instalación Rápida

### Opción 1: Ejecución Local

```bash
# 1. Clonar repositorio
git clone https://github.com/lfcordobap-png/SeminarioSanmateo.git
cd SeminarioSanmateo

# 2. Crear entorno virtual
python -m venv env

# 3. Activar entorno virtual
# En Windows:
env\Scripts\activate
# En macOS/Linux:
source env/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 6. Ejecutar API
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Opción 2: GitHub Codespaces

```bash
# 1. Hacer fork del repositorio
# 2. Crear Codespace
# 3. En la terminal:
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --host 0.0.0.0 --port 8000

# 4. Abrir en navegador
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Opción 3: Docker Compose

```bash
# 1. Configurar variables de entorno
cp .env.example .env

# 2. Levantar con Docker Compose
docker compose up -d

# 3. Acceder a la API
# http://localhost:8000/docs
```

### Opción 4: Docker Manual

```bash
# 1. Construir imagen
docker build -t fintech-nova:2.0 .

# 2. Ejecutar contenedor
docker run -p 8000:8000 --env-file .env fintech-nova:2.0

# 3. Acceder a la API
# http://localhost:8000/docs
```

---

## 📡 Ejecución

### Comando Básico

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Salida Esperada

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Acceder a la API

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **API Base:** http://localhost:8000

---

## 🏗️ Arquitectura

Para información detallada sobre la arquitectura, ver [`ARCHITECTURE.md`](ARCHITECTURE.md).

**Diagrama de Alto Nivel:**

```
Cliente (App Móvil)
        │
        └──► HTTP/HTTPS
                │
                └──► FastAPI (main.py)
                        │
                        ├── Rate Limiter (slowapi)
                        ├── Autenticación (HTTPBearer)
                        ├── Validación (Pydantic)
                        └── Base de Datos (SQLite)
```

---

## 🔌 Endpoints

### Endpoints Públicos (Sin Autenticación)

#### 1. Bienvenida

```bash
GET /
```

**Respuesta (200 OK):**
```json
{
  "mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."
}
```

#### 2. Estado del Sistema

```bash
GET /status
```

**Respuesta (200 OK):**
```json
{
  "estado": "Operacional",
  "servidor": "Node-01"
}
```

#### 3. Health Check

```bash
GET /health
```

**Respuesta (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-06-25T22:00:00+00:00",
  "version": "1.0.0",
  "checks": {
    "database": {"status": "ok", "message": "BD accesible..."},
    "disk": {"status": "ok", "message": "Disco saludable..."},
    "backup": {"status": "warning", "message": "..."}
  }
}
```

#### 4. Evaluación de Riesgo Crediticio

```bash
POST /evaluar-riesgo
Content-Type: application/json

{
  "edad": 30,
  "ingreso": 2500.0,
  "deudas": 1200.0
}
```

**Respuesta (200 OK):**
```json
{
  "resultado": "Aprobado",
  "score_simulado": 1300.0
}
```

> ⏱️ **Rate Limit:** 10 peticiones por minuto por IP.

**Resultados posibles:**

| Condición | Resultado |
|---|---|
| `edad < 18` | `"Rechazado (Menor de edad)"` |
| `ingreso - deudas > 1000` | `"Aprobado"` |
| Cualquier otro caso | `"En Revisión"` |

### Endpoints Protegidos (Requieren Bearer Token)

#### 5. Datos Financieros del Cliente 🔐

```bash
GET /datos-financieros/{id_cliente}
Authorization: Bearer secret-token-fintech
```

> ⏱️ **Rate Limit:** 30 peticiones por minuto por IP.

**Parámetros:**
- `id_cliente` (integer): ID del cliente

**Respuesta (200 OK):**
```json
{
  "cliente_id": 1,
  "historial": "Limpio",
  "score_interno": 750,
  "autorizado_por": "Token válido"
}
```

**Sin Token (403 Forbidden):**
```json
{"detail": "Not authenticated"}
```

**Token Inválido (401 Unauthorized):**
```json
{"detail": "Token inválido o expirado"}
```

### Endpoints Educativos (Ejemplos de Seguridad)

#### 6. Consulta Vulnerable a SQL Injection ⚠️

```bash
GET /vulnerable/users/{username}
```

> ⏱️ **Rate Limit:** 20 peticiones por minuto por IP.

**Ejemplo de Explotación:**
```bash
curl "http://localhost:8000/vulnerable/users/admin' OR '1'='1"
# Devuelve TODOS los usuarios (SQL Injection)
```

#### 7. Consulta Segura (Prepared Statements) ✅

```bash
GET /secure/users/{username}
```

> ⏱️ **Rate Limit:** 20 peticiones por minuto por IP.

**Uso Correcto:**
```bash
curl http://localhost:8000/secure/users/admin
# Devuelve solo usuario "admin"
```

---

## 🔐 Autenticación

### Configuración de Tokens

Los tokens se configuran mediante **variables de entorno** en el archivo `.env`:

```env
API_TOKEN=secret-token-fintech
ADMIN_TOKEN=admin-token-fintech
```

### Tokens por Defecto (Desarrollo)

```
secret-token-fintech    # Token estándar (API_TOKEN)
admin-token-fintech     # Token administrativo (ADMIN_TOKEN)
```

### Ejemplos de Uso

**✅ Con Token Válido:**

```bash
curl -H "Authorization: Bearer secret-token-fintech" \
     http://localhost:8000/datos-financieros/1

# Respuesta:
{
  "cliente_id": 1,
  "historial": "Limpio",
  "score_interno": 750,
  "autorizado_por": "Token válido"
}
```

**❌ Sin Token (403):**

```bash
curl http://localhost:8000/datos-financieros/1

# Respuesta:
{"detail": "Not authenticated"}
```

**❌ Con Token Inválido (401):**

```bash
curl -H "Authorization: Bearer token-incorrecto" \
     http://localhost:8000/datos-financieros/1

# Respuesta:
{"detail": "Token inválido o expirado"}
```

### Implementación de Autenticación en Código

```python
import os
from fastapi.security import HTTPBearer

security = HTTPBearer()

VALID_TOKENS = [
    os.getenv("API_TOKEN", "secret-token-fintech"),
    os.getenv("ADMIN_TOKEN", "admin-token-fintech"),
]

def verify_token(credentials = Depends(security)):
    if credentials.credentials not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return credentials.credentials
```

---

## 🧪 Testing

### Tests Automatizados (pytest)

El proyecto incluye una suite de **16 tests** en `tests/test_main.py`.

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Salida esperada:
# tests/test_main.py::test_root_returns_200 PASSED
# tests/test_main.py::test_status_operacional PASSED
# tests/test_main.py::test_health_returns_valid_status PASSED
# tests/test_main.py::test_security_headers_presentes PASSED
# tests/test_main.py::test_vulnerable_users_responde PASSED
# tests/test_main.py::test_secure_users_responde PASSED
# tests/test_main.py::test_secure_users_usuario_inexistente PASSED
# tests/test_main.py::test_evaluar_riesgo_aprobado PASSED
# tests/test_main.py::test_evaluar_riesgo_menor_de_edad PASSED
# tests/test_main.py::test_evaluar_riesgo_en_revision PASSED
# tests/test_main.py::test_evaluar_riesgo_campos_faltantes PASSED
# tests/test_main.py::test_evaluar_riesgo_tipos_invalidos PASSED
# tests/test_main.py::test_datos_financieros_sin_token PASSED
# tests/test_main.py::test_datos_financieros_token_invalido PASSED
# tests/test_main.py::test_datos_financieros_token_valido PASSED
# tests/test_main.py::test_datos_financieros_admin_token PASSED
# 16 passed in 1.05s
```

### Cobertura de Tests

| Categoría | Tests |
|---|---|
| Endpoints públicos | `test_root`, `test_status`, `test_health` |
| Security headers | `test_security_headers_presentes` |
| SQL injection | `test_vulnerable_users`, `test_secure_users` |
| Evaluación de riesgo | Aprobado, Menor de edad, En Revisión, campos inválidos |
| Autenticación | Sin token, token inválido, token válido, admin token |

### Pruebas Manuales con cURL

```bash
# Test 1: Endpoint público
curl http://localhost:8000/

# Test 2: Evaluación de crédito
curl -X POST http://localhost:8000/evaluar-riesgo \
  -H "Content-Type: application/json" \
  -d '{"edad": 25, "ingreso": 3000, "deudas": 500}'

# Test 3: Endpoint protegido (sin token → 403)
curl http://localhost:8000/datos-financieros/1

# Test 4: Endpoint protegido (con token → 200)
curl -H "Authorization: Bearer secret-token-fintech" \
     http://localhost:8000/datos-financieros/1

# Test 5: SQL Injection (vulnerable)
curl "http://localhost:8000/vulnerable/users/admin' OR '1'='1"

# Test 6: Consulta segura
curl http://localhost:8000/secure/users/admin
```

### Pruebas en Swagger UI

1. Abrir http://localhost:8000/docs
2. Click en endpoint
3. Click en "Try it out"
4. Modificar parámetros
5. Click en "Execute"

---

## 🛡️ Seguridad

Para análisis completo de seguridad, ver [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md).

### Características de Seguridad Implementadas

✅ **Autenticación:**
- Bearer Token authentication
- Tokens configurables por variables de entorno
- Validación en endpoints sensibles

✅ **Rate Limiting:**
- `/evaluar-riesgo` → 10 peticiones/minuto por IP
- `/secure/users` y `/vulnerable/users` → 20 peticiones/minuto por IP
- `/datos-financieros` → 30 peticiones/minuto por IP
- Respuesta automática `429 Too Many Requests` al superarse el límite

✅ **Validación:**
- Pydantic models para validación de entrada
- Prepared statements contra SQL injection

✅ **Headers HTTP:**
- `X-Content-Type-Options: nosniff` (MIME type sniffing)
- `X-Frame-Options: SAMEORIGIN` (Clickjacking)
- `X-XSS-Protection: 1; mode=block` (XSS)
- `Strict-Transport-Security` (HSTS)
- `Content-Security-Policy: default-src 'self'`
- `Referrer-Policy: strict-origin-when-cross-origin`

✅ **Docker:**
- Ejecución como usuario no-root (`appuser`)
- Imagen base `python:3.12-slim` (minimizada)
- Health check integrado en el contenedor

---

## 🐳 Docker

### Docker Compose (Recomendado)

```bash
# Levantar servicios
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f

# Detener servicios
docker compose down
```

### Build y Ejecución Manual

```bash
# Build imagen
docker build -t fintech-nova:2.0 .

# Run detached con env vars
docker run -d -p 8000:8000 --env-file .env --name fintech fintech-nova:2.0

# Ver logs
docker logs fintech

# Acceder al contenedor
docker exec -it fintech bash
```

### Despliegue Automatizado

```bash
# Usar el script de despliegue incluido
bash deploy.sh
```

El script `deploy.sh` realiza automáticamente: build → stop contenedor anterior → run nuevo → verificación de salud.

### Monitoreo

```bash
# Ver estadísticas de CPU/memoria
docker stats fintech

# Ver información detallada
docker inspect fintech
```

---

## 🤝 Contribución

Para contribuir, ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

**Pasos Rápidos:**

```bash
# 1. Fork del repositorio
# 2. Crear rama feature
git checkout -b feature/tu-caracteristica

# 3. Hacer cambios
# ... editar archivos ...

# 4. Ejecutar tests antes de commitear
pytest tests/ -v

# 5. Commit
git commit -m "feat: descripción del cambio"

# 6. Push
git push origin feature/tu-caracteristica

# 7. Pull Request
# Crear PR en GitHub
```

---

## 📚 Documentación Adicional

- [`ARCHITECTURE.md`](ARCHITECTURE.md) - Diseño arquitectónico detallado
- [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md) - Análisis de vulnerabilidades y controles
- [`CHANGELOG.md`](CHANGELOG.md) - Historial de cambios
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - Guía de contribución
- [FastAPI Docs](https://fastapi.tiangolo.com) - Documentación de FastAPI
- [Pydantic Docs](https://docs.pydantic.dev) - Validación de datos

---

## 📄 Licencia

Este proyecto está licenciado bajo la MIT License. Ver [`LICENSE`](LICENSE) para detalles.

---

## 👥 Autores

- **Luigi Córdoba** ([@lfcordobap-png](https://github.com/lfcordobap-png)) - Desarrollo y Arquitectura
- **Roslay Bautista** ([@RoslayBautista](https://github.com/RoslayBautista)) - Proyecto Base

---

## 📞 Soporte

¿Preguntas o problemas?

- 📧 **Email:** luigicordoba11@gmail.com
- 💬 **GitHub Issues:** [Reportar Issue](https://github.com/lfcordobap-png/SeminarioSanmateo/issues)
- 📖 **Documentación:** Ver archivos markdown en el repositorio

---

## 🎯 Estado del Proyecto

- **Versión:** 2.0 ✅
- **Status:** Production Ready 🚀
- **Última Actualización:** Junio 25, 2026

---

**Made with ❤️ for Cloud Architecture Learning**
