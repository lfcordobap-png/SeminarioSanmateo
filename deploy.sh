#!/bin/bash
set -e

IMAGE_NAME="fintech-nova"
CONTAINER_NAME="fintech-api"
PORT=8000
MAX_WAIT=20

echo "[$(date '+%H:%M:%S')] Iniciando despliegue de FinTech Nova..."

# ── 1. Construir imagen ───────────────────────────────────────
echo "[INFO] Construyendo imagen Docker: ${IMAGE_NAME}:latest"
docker build -t ${IMAGE_NAME}:latest .
echo "[OK] Imagen construida exitosamente."

# ── 2. Detener contenedor anterior si existe ─────────────────
if docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q .; then
    echo "[INFO] Deteniendo contenedor anterior: ${CONTAINER_NAME}"
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
    echo "[OK] Contenedor anterior eliminado."
fi

# ── 3. Iniciar nuevo contenedor ───────────────────────────────
echo "[INFO] Iniciando contenedor: ${CONTAINER_NAME}"
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8000 \
    --env-file .env \
    --restart unless-stopped \
    ${IMAGE_NAME}:latest

echo "[OK] Contenedor iniciado."

# ── 4. Verificar salud ────────────────────────────────────────
echo "[INFO] Esperando que la API esté disponible (máx ${MAX_WAIT}s)..."
for i in $(seq 1 ${MAX_WAIT}); do
    if curl -sf http://localhost:${PORT}/health > /dev/null 2>&1; then
        echo "[OK] API disponible en http://localhost:${PORT}"
        echo "[$(date '+%H:%M:%S')] Despliegue completado exitosamente."
        exit 0
    fi
    sleep 1
done

echo "[ERROR] La API no respondió en ${MAX_WAIT} segundos."
echo "[INFO] Revisá los logs con: docker logs ${CONTAINER_NAME}"
exit 1
