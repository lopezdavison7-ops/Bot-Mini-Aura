# -*- coding: utf-8 -*-

"""
🔧 Funciones Auxiliares para BOT MINI AURA
Version: 2.0.0
"""

import re
import json
import random
import string
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def validar_telefono(numero):
    """Validar número de teléfono"""
    try:
        numero_limpio = re.sub(r'[\s\-\(\)\+]', '', numero)
        if not numero_limpio.isdigit():
            return False
        if len(numero_limpio) < 8 or len(numero_limpio) > 15:
            return False
        return True
    except:
        return False

def formatear_numero(numero):
    """Formatear número de teléfono"""
    try:
        numero_limpio = re.sub(r'[\s\-\(\)\+]', '', numero)
        return numero_limpio
    except:
        return numero

def generar_id(longitud=10):
    """Generar ID aleatorio"""
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def formatear_fecha(fecha_str):
    """Formatear fecha"""
    try:
        fecha = datetime.fromisoformat(fecha_str)
        return fecha.strftime('%d/%m/%Y %H:%M:%S')
    except:
        return fecha_str

def cargar_json(archivo):
    """Cargar archivo JSON"""
    try:
        ruta = Path(archivo)
        if ruta.exists():
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error cargando JSON: {e}")
        return {}

def guardar_json(archivo, datos):
    """Guardar archivo JSON"""
    try:
        ruta = Path(archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error guardando JSON: {e}")
        return False

def formatear_monedas(cantidad):
    """Formatear cantidad de monedas"""
    try:
        if cantidad >= 1000000:
            return f"{cantidad/1000000:.1f}M"
        elif cantidad >= 1000:
            return f"{cantidad/1000:.1f}K"
        return str(cantidad)
    except:
        return str(cantidad)

def tiempo_transcurrido(fecha_inicio):
    """Calcular tiempo transcurrido"""
    try:
        inicio = datetime.fromisoformat(fecha_inicio)
        ahora = datetime.now()
        diferencia = ahora - inicio
        
        dias = diferencia.days
        horas = diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        
        if dias > 0:
            return f"hace {dias} días"
        elif horas > 0:
            return f"hace {horas} horas"
        elif minutos > 0:
            return f"hace {minutos} minutos"
        else:
            return "hace un momento"
    except:
        return "tiempo desconocido"