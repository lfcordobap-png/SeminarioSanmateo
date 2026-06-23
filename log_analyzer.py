import re  # Módulo de expresiones regulares (pattern matching)
import sys  # Acceso a argumentos de línea de comandos
import json  # Para exportar resultados en formato estructurado
from datetime import datetime
from collections import defaultdict

# ── PATRONES DE DETECCIÓN ───────────────────────────────────
# Cada patrón es una tupla: (regex_pattern, descripción)
# re.IGNORECASE hace la búsqueda sin importar mayúsculas/minúsculas
SQL_PATTERNS = [
    (r"'\s*OR\s*'?1'?\s*=\s*'?1", "Bypass de login (OR 1=1)"),
    (r"'\s*--", "Comentario SQL para ignorar password"),
    (r"UNION\s+SELECT", "Exfiltración UNION SELECT"),
    (r"DROP\s+TABLE", "Destrucción de tabla DROP TABLE"),
    (r"INSERT\s+INTO.*SELECT", "Inyección de datos"),
    (r"EXEC\s*\(", "Ejecución de comandos EXEC"),
]

BLACKLIST_FILE = "ip_blacklist.txt"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ── SECCIÓN: Lista negra de IPs ─────────────────────────────
def load_blacklist(blacklist_path: str = BLACKLIST_FILE) -> dict:
    """
    Carga la lista negra desde disco.
    Formato de archivo: ip,primera_deteccion,ultima_deteccion,total_intentos
    Retorna un dict: { ip: {'first_seen': datetime, 'last_seen': datetime, 'attempts': int} }
    """
    blacklist = {}

    try:
        with open(blacklist_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 4:
                    continue  # Ignora líneas corruptas en vez de fallar todo el análisis
                ip, first_seen, last_seen, attempts = parts
                blacklist[ip] = {
                    'first_seen': datetime.strptime(first_seen, DATE_FORMAT),
                    'last_seen': datetime.strptime(last_seen, DATE_FORMAT),
                    'attempts': int(attempts),
                }
    except FileNotFoundError:
        # Primera ejecución: no hay lista negra todavía, no es un error
        pass

    return blacklist


def update_blacklist(blacklist: dict, new_ips: dict, now: datetime = None) -> dict:
    """
    Actualiza la lista negra en memoria con las IPs detectadas en este análisis.
    new_ips: dict {ip: cantidad_de_intentos_en_este_log}
    """
    now = now or datetime.now()

    for ip, attempts_this_run in new_ips.items():
        if ip in blacklist:
            blacklist[ip]['last_seen'] = now
            blacklist[ip]['attempts'] += attempts_this_run
        else:
            blacklist[ip] = {
                'first_seen': now,
                'last_seen': now,
                'attempts': attempts_this_run,
            }

    return blacklist


def save_blacklist(blacklist: dict, blacklist_path: str = BLACKLIST_FILE) -> None:
    """Persiste la lista negra a disco en formato CSV simple."""
    with open(blacklist_path, 'w', encoding='utf-8') as f:
        for ip, data in blacklist.items():
            f.write(
                f"{ip},"
                f"{data['first_seen'].strftime(DATE_FORMAT)},"
                f"{data['last_seen'].strftime(DATE_FORMAT)},"
                f"{data['attempts']}\n"
            )


def days_in_blacklist(ip: str, blacklist: dict, reference_date: datetime = None) -> int:
    """
    Retorna cuántos días lleva una IP en la lista negra,
    calculado desde first_seen hasta reference_date (por defecto, ahora).
    Retorna -1 si la IP no está en la lista.
    """
    if ip not in blacklist:
        return -1

    reference_date = reference_date or datetime.now()
    delta = reference_date - blacklist[ip]['first_seen']
    return delta.days


# ── SECCIÓN: Análisis del log ───────────────────────────────
def analyze_log(log_path: str, blacklist: dict) -> dict:
    """
    Analiza un archivo de logs y retorna estadísticas e incidentes detectados.
    Las líneas cuya IP ya está en la lista negra se marcan con prioridad ALTA.
    Retorna un dict con: total_lines, clean, incidents, by_ip, by_type, new_ips
    """
    incidents = []
    by_ip = defaultdict(int)    # Cuántos ataques por cada IP (en este log)
    by_type = defaultdict(int)  # Cuántos ataques de cada tipo
    total_lines = 0

    try:
        # 'with open()' garantiza que el archivo se cierre aunque haya errores
        with open(log_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                total_lines += 1
                line = line.strip()  # Elimina espacios y saltos de línea

                if not line:  # Ignora líneas vacías
                    continue

                # Verificar cada patrón de SQL Injection
                for pattern, desc in SQL_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Extraer IP de la línea del log
                        ip_match = re.search(r'IP:(\S+)', line)
                        ip = ip_match.group(1) if ip_match else 'desconocida'

                        is_known = ip in blacklist
                        priority = 'ALTA' if is_known else 'NORMAL'

                        incident = {
                            'line': line_num,
                            'type': desc,
                            'ip': ip,
                            'content': line[:100],  # Max 100 chars
                            'priority': priority,
                            'known_attacker': is_known,
                        }

                        if is_known:
                            incident['days_in_blacklist'] = days_in_blacklist(ip, blacklist)

                        incidents.append(incident)
                        by_ip[ip] += 1
                        by_type[desc] += 1
                        break  # Una detección por línea es suficiente

    except FileNotFoundError:
        print(f'ERROR: Archivo no encontrado: {log_path}')
        sys.exit(1)
    except PermissionError:
        print(f'ERROR: Sin permisos para leer: {log_path}')
        sys.exit(1)

    return {
        'total_lines': total_lines,
        'clean': total_lines - len(incidents),
        'incidents': incidents,
        'by_ip': dict(by_ip),
        'by_type': dict(by_type),
        'new_ips': dict(by_ip),  # IPs detectadas en esta corrida, para actualizar blacklist
    }


# ── SECCIÓN: Reporte ────────────────────────────────────────
def print_report(results: dict, log_path: str, blacklist: dict) -> None:
    """Imprime un reporte formateado, priorizando atacantes ya conocidos."""
    separator = "=" * 60
    print(f"\n{separator}")
    print("  REPORTE DE SEGURIDAD — FinTech Nova")
    print(f"  Archivo analizado : {log_path}")
    print(f"  Fecha de análisis : {datetime.now().strftime(DATE_FORMAT)}")
    print(separator)
    print(f"  Total líneas      : {results['total_lines']}")
    print(f"  Líneas limpias    : {results['clean']}")
    print(f"  Incidentes        : {len(results['incidents'])}")
    print(f"  IPs en lista negra: {len(blacklist)}")
    print(f"{separator}\n")

    if results['incidents']:
        # Ordenar para mostrar primero las de prioridad ALTA (atacantes recurrentes)
        ordered = sorted(
            results['incidents'],
            key=lambda i: i['priority'] != 'ALTA'
        )

        print("  ⚠️  INCIDENTES DETECTADOS:")
        for i, incident in enumerate(ordered, 1):
            marker = "🔴" if incident['priority'] == 'ALTA' else "🟡"
            print(f"  {marker} [{i}] Línea {incident['line']}: {incident['type']}")
            print(f"        IP: {incident['ip']} | Prioridad: {incident['priority']}")
            if incident['known_attacker']:
                print(f"        ⚠️  Atacante conocido — {incident['days_in_blacklist']} día(s) en lista negra")
            print(f"        → {incident['content']}...")
    else:
        print("  ✅ No se detectaron incidentes. Logs limpios.")

    print(f"\n{separator}\n")


# ── PUNTO DE ENTRADA ─────────────────────────────────────────
if __name__ == "__main__":
    log_file = "server.log"

    print(f"[INFO] Cargando lista negra desde: {BLACKLIST_FILE}")
    blacklist = load_blacklist()
    print(f"[INFO] {len(blacklist)} IP(s) conocida(s) en lista negra")

    print(f"[INFO] Iniciando análisis de seguridad del archivo: {log_file}")
    results = analyze_log(log_file, blacklist)

    print_report(results, log_file, blacklist)

    # Actualizar y persistir la lista negra con las IPs detectadas en esta corrida
    blacklist = update_blacklist(blacklist, results['new_ips'])
    save_blacklist(blacklist)
    print(f"[INFO] Lista negra actualizada y guardada en: {BLACKLIST_FILE}")