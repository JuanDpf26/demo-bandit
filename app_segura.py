"""Versión corregida del demo."""
import ast
import hashlib
import json
import os
import subprocess

import requests

DB_PASSWORD = os.environ.get("DB_PASSWORD")


def calcular(expresion):
    return ast.literal_eval(expresion)


def hacer_ping(host):
    return subprocess.call(["ping", "-c", "1", host])  # nosec B603 - lista de argumentos, sin shell


def hash_password(pwd, salt):
    return hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt, 200_000).hex()


def cargar_sesion(datos):
    return json.loads(datos)


def consultar_api(url):
    return requests.get(url, timeout=10)


def buscar_paciente(cursor, nombre):
    cursor.execute("SELECT * FROM pacientes WHERE nombre = %s", (nombre,))
