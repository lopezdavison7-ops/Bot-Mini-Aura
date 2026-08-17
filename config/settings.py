# -*- coding: utf-8 -*-

"""
⚙️ Configuración de BOT MINI AURA
Version: 2.0.0
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ==================== IDENTIDAD DEL BOT ====================

NOMBRE_BOT = "🤖 BOT MINI AURA"
VERSION = "2.0.0"
DESARROLLADOR = "Tu Nombre"

# ==================== OWNER ====================

OWNER_NUMBER = "50578391933"
OWNER_NAME = "Dueño del Bot"

# Lista de owners autorizados
OWNERS = [
    "50578391933",  # Owner principal
    # Agrega más números aquí
]

# ==================== PREFIJO ====================

PREFIX = "."

# ==================== MODO DEBUG ====================

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ==================== VINCULACIÓN ====================

VINCULACION = {
    'tiempo_espera_codigo': 300,  # 5 minutos
    'intentos_maximos': 3,
    'usar_qr': True,
    'usar_codigo': True,
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
    'youtube': os.getenv('YOUTUBE_API_KEY', ''),
    'tiktok': os.getenv('TIKTOK_API_KEY', ''),
    'weather': os.getenv('WEATHER_API_KEY', ''),
    'twilio_sid': os.getenv('TWILIO_SID', ''),
    'twilio_token': os.getenv('TWILIO_TOKEN', ''),
}

# ==================== PATHS ====================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'src', 'data')
DATABASE_PATH = os.path.join(DATA_DIR, 'database', 'bot.db')
MEDIA_PATH = os.path.join(DATA_DIR, 'media')
SESSION_PATH = os.path.join(BASE_DIR, 'src', 'sessions')