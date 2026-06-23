#!/bin/bash

# resource_monitor.sh
# Script para monitorear recursos del sistema: CPU, Memoria, Disco
# Autor: Equipo de Seguridad Seminario San Mateo

# Umbrales de advertencia
UMBRAL_MEMORIA=80
UMBRAL_DISCO=85

echo "=== Monitoreo de Recursos - $(date) ==="

# --- 1. Verificar Uso de Memoria ---
# Obtiene el porcentaje de memoria RAM usada
MEMORY_USED=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
echo "Memoria RAM usada: ${MEMORY_USED}%"

# Condición para advertencia de memoria
if [ "$MEMORY_USED" -gt "$UMBRAL_MEMORIA" ]; then
    echo "WARNING: Uso de memoria RAM alto (${MEMORY_USED}% > ${UMBRAL_MEMORIA}%)"
fi

# --- 2. Verificar Espacio en Disco ---
# Obtiene el porcentaje de disco usado en el directorio actual
DISK_USED=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')
echo "Espacio en disco usado: ${DISK_USED}%"

# Condición para advertencia de disco
if [ "$DISK_USED" -gt "$UMBRAL_DISCO" ]; then
    echo "WARNING: Espacio en disco bajo (${DISK_USED}% > ${UMBRAL_DISCO}%)"
fi

# --- 3. Resumen de Métricas ---
echo "--- Resumen ---"
echo "CPU Load (1m): $(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}')"
echo "Memoria RAM usada: ${MEMORY_USED}%"
echo "Espacio en disco usado: ${DISK_USED}%"
echo "================"