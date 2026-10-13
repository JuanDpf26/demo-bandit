"""Demo para la exposición de Bandit: código con malas prácticas a propósito."""
import hashlib
import pickle
import subprocess

import requests

DB_PASSWORD = "admin123"  # B105: contraseña embebida


def calcular(expresion):
    return eval(expresion)  # B307: uso de eval


def hacer_ping(host):
    # B602: subprocess con shell=True -> inyección de comandos
    return subprocess.call("ping -c 1 " + host, shell=True)


def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()  # B324: hash débil


def cargar_sesion(datos):
    return pickle.loads(datos)  # B301: deserialización insegura


def consultar_api(url):
    return requests.get(url, verify=False)  # B501: sin verificación TLS


def buscar_paciente(cursor, nombre):
    # B608: SQL construido con concatenación
    cursor.execute("SELECT * FROM pacientes WHERE nombre = '" + nombre + "'")
