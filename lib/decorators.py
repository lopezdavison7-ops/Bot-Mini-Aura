# -*- coding: utf-8 -*-

"""
🎯 Decoradores para BOT MINI AURA
Version: 2.0.0
"""

from functools import wraps
from config.settings import OWNER_NUMBER, OWNERS
import logging

logger = logging.getLogger(__name__)

def solo_owner(func):
    """Decorador para comandos solo de owner"""
    @wraps(func)
    def wrapper(usuario, *args, **kwargs):
        if usuario not in OWNERS and usuario != OWNER_NUMBER:
            return "❌ *No tienes permisos para usar este comando*"
        return func(usuario, *args, **kwargs)
    return wrapper

def manejar_errores(func):
    """Decorador para manejar errores"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {e}")
            return f"❌ *Error al ejecutar el comando*\n\n{str(e)}"
    return wrapper

def requerir_vinculacion(func):
    """Decorador para requerir vinculación"""
    @wraps(func)
    def wrapper(usuario, *args, **kwargs):
        # Aquí se verificaría la vinculación
        return func(usuario, *args, **kwargs)
    return wrapper