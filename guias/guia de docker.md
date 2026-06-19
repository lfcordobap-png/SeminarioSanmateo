# ── Construir la imagen Docker
docker build -t fintech-nova:1.0 .

# ── Verificar la imagen construida
docker images

# ── Ejecutar el contenedor de FinTech Nova
docker run -d -p 8000:8000 --name fintech-api fintech-nova:1.0

# ── que el contenedor está ejecutándose
docker ps

Comandos esenciales de monitoreo Docker
# ── VER LOGS DEL CONTENEDOR ──────────────────────────────────
docker logs fintech-api
docker logs -f fintech-api # -f = follow, en tiempo real
docker logs --tail 50 fintech-api # últimas 50 líneas
# ── INSPECCIONAR EL ESTADO DEL CONTENEDOR ───────────────────
docker inspect fintech-api # información detallada en JSON
docker stats fintech-api # uso de CPU, memoria, red en tiempo real
# ── ACCEDER AL INTERIOR DEL CONTENEDOR ─────────────────────
docker exec -it fintech-api bash # abrir terminal interactiva
# Dentro del contenedor puedes explorar, diagnosticar, etc.
# 'exit' para salir
# ── DETENER Y ELIMINAR ───────────────────────────────────────
docker stop fintech-api # detiene el contenedor ordenadamente
docker start fintech-api # reinicia un contenedor detenido
docker rm fintech-api # elimina el contenedor (detenido)
docker rm -f fintech-api # elimina aunque esté corriendo