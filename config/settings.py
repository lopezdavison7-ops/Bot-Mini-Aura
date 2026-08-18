# -*- coding: utf-8 -*-

"""
⚙️ Configuración de BOT MINI AURA
Version: 3.0.0
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ==================== IDENTIDAD DEL BOT ====================

NOMBRE_BOT = "🤖 BOT MINI AURA"
VERSION = "3.0.0"
DESARROLLADOR = "Davison López"

# ==================== OWNER ====================

OWNER_NUMBER = "50578391933"
OWNER_NAME = "Davison"

# Lista de owners autorizados
OWNERS = [
    "50578391933",  # Owner principal
]

# ==================== PREFIJO ====================

PREFIX = "."

# ==================== MODO DEBUG ====================

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ==================== VINCULACIÓN ====================

VINCULACION = {
    'tiempo_espera_codigo': 300,  # 5 minutos
    'intentos_maximos': 3,
    'longitud_codigo': 8,
}

# ==================== ECONOMÍA ====================

MONEDAS_INICIALES = 100
MONEDAS_POR_TRABAJO = 10
MAX_MONEDAS = 999999
TIEMPO_ESPERA_TRABAJO = 3600  # 1 hora
TIEMPO_ESPERA_ROBO = 1800     # 30 minutos
PROBABILIDAD_ROBO = 0.3       # 30%

# ==================== JUEGOS ====================

PREMIO_DADO = 10
COSTO_JUEGO = 5

# ==================== APIs ====================

API_KEYS = {
    'weather': os.getenv('WEATHER_API_KEY', ''),
    'youtube': os.getenv('YOUTUBE_API_KEY', ''),
    'tiktok': os.getenv('TIKTOK_API_KEY', ''),
}

# ==================== PATHS ====================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_PATH = os.path.join(DATA_DIR, 'bot.db')
VINCULADOS_PATH = os.path.join(DATA_DIR, 'vinculados.json')