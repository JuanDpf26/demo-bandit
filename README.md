# Demo de Bandit: análisis estático de seguridad en Python

Exposición sobre [Bandit](https://github.com/PyCQA/bandit), herramienta de análisis estático (SAST) mantenida por PyCQA. Bandit recorre el AST del código Python y detecta malas prácticas de seguridad sin ejecutar el programa.

**Autor:** Juan Diego Pinzón Fontecha - Carlos Felipe Avilan Payares

## Archivos

| Archivo | Descripción |
|---|---|
| `app_vulnerable.py` | Código con malas prácticas a propósito |
| `app_segura.py` | El mismo código corregido |

## Cómo ejecutarlo

```bash
pip install bandit
bandit app_vulnerable.py
bandit app_segura.py
```

## Resultados (Bandit 1.9.4)

### app_vulnerable.py: 10 hallazgos

| Línea | ID | Problema | Severidad | Confianza |
|---|---|---|---|---|
| 3 | B403 | Import de pickle | Baja | Alta |
| 4 | B404 | Import de subprocess | Baja | Alta |
| 8 | B105 | Contraseña embebida `'admin123'` | Baja | Media |
| 12 | B307 | Uso de `eval()` | Media | Alta |
| 17 | B602 | `subprocess` con `shell=True` | Alta | Alta |
| 21 | B324 | Hash MD5 usado para seguridad | Alta | Alta |
| 25 | B301 | `pickle.loads` con datos no confiables | Media | Alta |
| 29 | B501 | `requests` con `verify=False` | Alta | Alta |
| 29 | B113 | `requests` sin timeout | Media | Baja |
| 34 | B608 | SQL armado concatenando texto | Media | Media |

**Total:** 3 altas, 4 medias, 3 bajas.

### app_segura.py: 2 avisos de severidad baja

| Línea | ID | Aviso | Severidad |
|---|---|---|---|
| 6 | B404 | Import de subprocess | Baja |
| 18 | B607 | Proceso iniciado sin ruta completa | Baja |

**Total:** 0 altas, 0 medias, 2 bajas.

## Cómo se corrigió cada problema

| ID | Inseguro | Seguro |
|---|---|---|
| B105 | `"admin123"` en el código | `os.environ.get("DB_PASSWORD")` |
| B307 | `eval(expr)` | `ast.literal_eval(expr)` |
| B602 | `"ping " + host, shell=True` | `["ping", "-c", "1", host]` |
| B324 | `hashlib.md5(pwd)` | `hashlib.pbkdf2_hmac("sha256", ...)` |
| B301 | `pickle.loads(datos)` | `json.loads(datos)` |
| B501 | `verify=False` | Verificación TLS por defecto + `timeout` |
| B608 | Concatenar texto en SQL | Consulta parametrizada `%s` |

## Referencias

- Documentación: https://bandit.readthedocs.io/en/latest/
- Código fuente: https://github.com/PyCQA/bandit
