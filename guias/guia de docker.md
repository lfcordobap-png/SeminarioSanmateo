# Guía de Docker — FinTech Nova API

## Archivos Docker del proyecto

| Archivo | Propósito |
|---|---|
| `Dockerfile` | Imagen de producción (Python 3.12-slim, usuario sin privilegios) |
| `Dockerfile.dev` | Imagen de desarrollo (Python 3.12, hot-reload activado) |
| `docker-compose.yml` | Orquestación del servicio con volúmenes, variables de entorno y healthcheck |

---

## Producción — imagen directa

```bash
# Construir la imagen
docker build -t fintech-nova:1.0 .

# Verificar la imagen construida
docker images

# Ejecutar el contenedor
docker run -d -p 8000:8000 --name fintech-api fintech-nova:1.0

# Verificar que el contenedor está corriendo
docker ps
```

---

## Producción — Docker Compose (recomendado)

```bash
# Levantar el servicio (construye si no existe la imagen)
docker compose up -d

# Ver el estado del servicio
docker compose ps

# Ver logs
docker compose logs -f api

# Detener el servicio
docker compose down

# Reconstruir la imagen y levantar (tras cambios en el código)
docker compose up -d --build
```

> El `docker-compose.yml` monta automáticamente `database.db` y `backups/`,
> carga variables desde `.env` y reinicia el servicio ante caídas (`unless-stopped`).

---

## Desarrollo — imagen con hot-reload

```bash
# Construir la imagen de desarrollo
docker build -f Dockerfile.dev -t fintech-nova:dev .

# Ejecutar montando el código fuente para reflejar cambios en tiempo real
docker run -d -p 8000:8000 \
  -v $(pwd):/app \
  --name fintech-dev \
  fintech-nova:dev
```

---

## Monitoreo y diagnóstico

```bash
# Ver logs del contenedor
docker logs fintech-api
docker logs -f fintech-api          # en tiempo real
docker logs --tail 50 fintech-api   # últimas 50 líneas

# Estado del healthcheck y detalles del contenedor
docker inspect fintech-api

# Uso de CPU, memoria y red en tiempo real
docker stats fintech-api

# Abrir terminal interactiva dentro del contenedor
docker exec -it fintech-api bash
# (usa 'exit' para salir)
```

---

## Gestión del ciclo de vida

```bash
# Detener el contenedor ordenadamente
docker stop fintech-api

# Iniciar un contenedor detenido
docker start fintech-api

# Eliminar el contenedor (debe estar detenido)
docker rm fintech-api

# Forzar eliminación aunque esté corriendo
docker rm -f fintech-api

# Eliminar la imagen local
docker rmi fintech-nova:1.0
```

---

## Healthcheck

El contenedor verifica su propio estado cada 30 s llamando a:

```
GET http://localhost:8000/health
```

Configuración definida en `Dockerfile` y replicada en `docker-compose.yml`:

| Parámetro | Valor |
|---|---|
| `interval` | 30 s |
| `timeout` | 10 s |
| `retries` | 3 |
| `start_period` | 10 s |

Ver el estado del healthcheck:

```bash
docker inspect --format='{{.State.Health.Status}}' fintech-api
```

---

## Variables de entorno

Las variables se cargan desde `.env` (ver `docker-compose.yml`). Valores por defecto:

| Variable | Default |
|---|---|
| `API_TOKEN` | `secret-token-fintech` |
| `ADMIN_TOKEN` | `admin-token-fintech` |

Crear el archivo `.env` en la raíz del proyecto antes de levantar con Compose:

```bash
API_TOKEN=tu-token-seguro
ADMIN_TOKEN=tu-admin-token-seguro
```
