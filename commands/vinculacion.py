# -*- coding: utf-8 -*-

"""
🔗 Sistema de Vinculación para BOT MINI AURA
Version: 2.0.0
"""

import random
import re
from datetime import datetime, timedelta
from src.lib.vincular import SistemaVinculacion
from config.settings import PREFIX, OWNER_NUMBER

sistema_vinculacion = SistemaVinculacion()

def validar_numero(numero):
    """Validar formato de número de teléfono"""
    try:
        # Eliminar espacios y caracteres especiales
        numero_limpio = re.sub(r'[\s\-\(\)\+]', '', numero)
        
        # Verificar que sean solo números
        if not numero_limpio.isdigit():
            return None
        
        # Verificar longitud (8-15 dígitos)
        if len(numero_limpio) < 8 or len(numero_limpio) > 15:
            return None
        
        return numero_limpio
    except:
        return None

def iniciar_vinculacion(usuario, args):
    """Iniciar proceso de vinculación"""
    try:
        # Si ya está vinculado
        if sistema_vinculacion.esta_vinculado(usuario):
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ✅ *YA ESTÁS VINCULADO* ✅   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Tu número:* {usuario}
🔗 *Estado:* Vinculado

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Ya puedes usar todos los comandos*
Escribe {PREFIX}menu para comenzar
            """
        
        if not args:
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔗 *VINCULACIÓN DE BOT* 🔗  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Para vincular tu número, sigue estos pasos:*

1️⃣ Escribe: {PREFIX}vincular [tu_número]
   Ejemplo: {PREFIX}vincular 50578391933

2️⃣ Elige el método de vinculación:
   • Código de 8 dígitos
   • Código QR

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Tu número debe incluir código de país*
            """
        
        numero = args[0]
        numero_valido = validar_numero(numero)
        
        if not numero_valido:
            return f"""
❌ *Número inválido*

📝 *Formato correcto:* {PREFIX}vincular [número con código de país]
📌 *Ejemplo:* {PREFIX}vincular 50578391933

💡 *Incluye el código de país sin el signo +*
            """
        
        # Guardar número en sesión temporal
        sistema_vinculacion.guardar_numero_pendiente(usuario, numero_valido)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔗 *VINCULACIÓN INICIADA* 🔗  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Número a vincular:* {numero_valido}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
*ELIGE EL MÉTODO DE VINCULACIÓN:*

1️⃣ *Código de 8 dígitos*
   Escribe: {PREFIX}codigo

2️⃣ *Código QR*
   Escribe: {PREFIX}qr

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ *Tienes 5 minutos para completar*
        """
    except Exception as e:
        return f"❌ *Error al iniciar vinculación:* {e}"

def solicitar_codigo(usuario, args):
    """Generar código de 8 dígitos"""
    try:
        # Obtener número pendiente
        numero_pendiente = sistema_vinculacion.obtener_numero_pendiente(usuario)
        
        if not numero_pendiente:
            return f"""
❌ *No has iniciado la vinculación*

📝 *Primero escribe:* {PREFIX}vincular [tu_número]
📌 *Ejemplo:* {PREFIX}vincular 50578391933
            """
        
        # Generar código
        codigo = sistema_vinculacion.generar_codigo(numero_pendiente)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🔢 *CÓDIGO DE VINCULACIÓN* 🔢   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Tu código de vinculación es:*

*{codigo[0:4]} {codigo[4:8]}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 *Para completar:*
Escribe: {PREFIX}verificar [código]
Ejemplo: {PREFIX}verificar {codigo}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ *Válido por 5 minutos*
🔒 *Tienes 3 intentos*
        """
    except Exception as e:
        return f"❌ *Error al generar código:* {e}"

def verificar_codigo(usuario, args):
    """Verificar código de vinculación"""
    try:
        if not args:
            return f"❌ *Uso incorrecto*\n\nEscribe: {PREFIX}verificar [código]\nEjemplo: {PREFIX}verificar 12345678"
        
        codigo_ingresado = args[0].replace(' ', '')
        
        # Verificar que sean 8 dígitos
        if not codigo_ingresado.isdigit() or len(codigo_ingresado) != 8:
            return "❌ *Código inválido*\n\nEl código debe tener 8 dígitos."
        
        # Verificar código
        resultado = sistema_vinculacion.verificar_codigo(usuario, codigo_ingresado)
        
        return resultado['mensaje']
    except Exception as e:
        return f"❌ *Error al verificar código:* {e}"

def solicitar_qr(usuario, args):
    """Generar código QR"""
    try:
        numero_pendiente = sistema_vinculacion.obtener_numero_pendiente(usuario)
        
        if not numero_pendiente:
            return f"""
❌ *No has iniciado la vinculación*

📝 *Primero escribe:* {PREFIX}vincular [tu_número]
            """
        
        resultado = sistema_vinculacion.generar_qr(numero_pendiente)
        return resultado['mensaje']
    except Exception as e:
        return f"❌ *Error al generar QR:* {e}"

def verificar_estado(usuario, args):
    """Verificar estado de vinculación"""
    try:
        if sistema_vinculacion.esta_vinculado(usuario):
            info = sistema_vinculacion.obtener_info_vinculacion(usuario)
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ✅ *YA ESTÁS VINCULADO* ✅   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Número:* {usuario}
📅 *Desde:* {info.get('fecha_vinculacion', 'Desconocida')[:10]}
🔗 *Método:* {info.get('metodo', 'Desconocido')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 *Disfruta de BOT MINI AURA*
Escribe {PREFIX}menu para comenzar
            """
        else:
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ❌ *NO ESTÁS VINCULADO* ❌   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🔗 *Para vincularte:*
Escribe: {PREFIX}vincular [tu_número]

📌 *Ejemplo:* {PREFIX}vincular 50578391933
            """
    except Exception as e:
        return f"❌ *Error al verificar estado:* {e}"

def desvincular(usuario, args):
    """Desvincular número"""
    try:
        if sistema_vinculacion.desvincular(usuario):
            return "✅ *Has sido desvinculado correctamente*\n\nPara volver a vincularte, usa " + PREFIX + "vincular"
        return "❌ *No estabas vinculado*"
    except Exception as e:
        return f"❌ *Error al desvincular:* {e}"