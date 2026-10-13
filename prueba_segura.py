"""Prueba 2: ejecuta Bandit sobre app_segura.py y muestra el reporte en español.

Uso:
    python prueba_segura.py
"""
import json
import subprocess  # nosec B404 - se usa solo para ejecutar Bandit
import sys

ARCHIVO = "app_segura.py"

SEVERIDAD = {"LOW": "Baja", "MEDIUM": "Media", "HIGH": "Alta", "UNDEFINED": "Sin definir"}

MENSAJES = {
    "B105": "Posible contraseña escrita directamente en el código.",
    "B113": "Petición con requests sin timeout: puede quedarse colgada.",
    "B301": "pickle puede ejecutar código al deserializar datos no confiables.",
    "B307": "Uso de eval(): puede ejecutar código arbitrario. Use ast.literal_eval.",
    "B324": "Uso de hash débil (MD5/SHA1) para seguridad.",
    "B403": "Import de pickle: revise si deserializa datos externos.",
    "B404": "Import de subprocess: revise cómo se ejecutan los comandos.",
    "B501": "Petición con verify=False: se desactiva la verificación del certificado TLS.",
    "B602": "subprocess con shell=True: riesgo de inyección de comandos.",
    "B607": "Se inicia un proceso sin la ruta completa del ejecutable.",
    "B608": "Posible inyección SQL: la consulta se arma concatenando texto.",
}


def linea_de_codigo(h):
    """Devuelve solo la línea donde está el problema (Bandit trae líneas de contexto)."""
    for linea in (h.get("code") or "").splitlines():
        numero, _, texto = linea.partition(" ")
        if numero == str(h["line_number"]):
            return texto.strip()
    return ""


def main():
    comando = [sys.executable, "-m", "bandit", ARCHIVO, "-f", "json", "-q"]
    salida = subprocess.run(comando, capture_output=True, text=True)  # nosec B603
    try:
        datos = json.loads(salida.stdout)
    except json.JSONDecodeError:
        print("No se pudo leer la salida de Bandit. ¿Está instalado? (pip install bandit)")
        print(salida.stderr)
        sys.exit(2)

    hallazgos = datos.get("results", [])
    print(f"\nPRUEBA 2 - Código corregido: {ARCHIVO}")
    print("=" * 60)
    if not hallazgos:
        print("No se encontraron problemas de seguridad.")
    for i, h in enumerate(hallazgos, 1):
        test_id = h["test_id"]
        mensaje = MENSAJES.get(test_id, h["issue_text"])
        print(f"\n[{i}] {test_id} - {mensaje}")
        print(f"    Severidad: {SEVERIDAD[h['issue_severity']]}   Confianza: {SEVERIDAD[h['issue_confidence']]}")
        print(f"    Línea:     {h['line_number']}")
        print(f"    Código:    {linea_de_codigo(h)}")

    conteo = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for h in hallazgos:
        conteo[h["issue_severity"]] = conteo.get(h["issue_severity"], 0) + 1
    lineas = datos.get("metrics", {}).get("_totals", {}).get("loc", 0)
    print("\n" + "=" * 60)
    print(f"Líneas de código analizadas: {lineas}")
    print(f"Total de hallazgos: {len(hallazgos)}")
    print(f"  Severidad alta:  {conteo['HIGH']}")
    print(f"  Severidad media: {conteo['MEDIUM']}")
    print(f"  Severidad baja:  {conteo['LOW']}")
    if conteo["HIGH"] == 0 and conteo["MEDIUM"] == 0:
        print("\nResultado: sin hallazgos de severidad alta ni media.")


if __name__ == "__main__":
    main()
