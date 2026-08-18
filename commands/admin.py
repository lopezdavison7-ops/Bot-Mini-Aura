# -*- coding: utf-8 -*-

"""
👮 Comandos de Administración para BOT MINI AURA
Versión: 4.0.0
"""

from config.settings import PREFIX, OWNER_NUMBER

def kick_usuario(usuario, args):
    """Expulsar usuario del grupo"""
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"❌ *Uso:* {PREFIX}kick [número]\n\nEjemplo: {PREFIX}kick 50512345678"
        
        objetivo = args[0]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   👢 *USUARIO EXPULSADO* 👢   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ha sido expulsado del grupo

👮 *Ejecutado por:* +{usuario}
        """
    except Exception as e:
        return f"❌ *Error al expulsar:* {e}"

def ban_usuario(usuario, args):
    """Banear usuario del grupo"""
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"❌ *Uso:* {PREFIX}ban [número]\n\nEjemplo: {PREFIX}ban 50512345678"
        
        objetivo = args[0]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🔨 *USUARIO BANEADO* 🔨   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ha sido baneado del grupo

👮 *Ejecutado por:* +{usuario}
        """
    except Exception as e:
        return f"❌ *Error al banear:* {e}"

def promover_usuario(usuario, args):
    """Promover usuario a admin"""
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"❌ *Uso:* {PREFIX}promover [número]\n\nEjemplo: {PREFIX}promover 50512345678"
        
        objetivo = args[0]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  ⬆️ *USUARIO PROMOVIDO* ⬆️  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ahora es admin del grupo

👮 *Ejecutado por:* +{usuario}
        """
    except Exception as e:
        return f"❌ *Error al promover:* {e}"

def demover_usuario(usuario, args):
    """Quitar admin a usuario"""
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"❌ *Uso:* {PREFIX}demover [número]\n\nEjemplo: {PREFIX}demover 50512345678"
        
        objetivo = args[0]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  ⬇️ *USUARIO DEGRADADO* ⬇️  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ya no es admin del grupo

👮 *Ejecutado por:* +{usuario}
        """
    except Exception as e:
        return f"❌ *Error al degradar:* {e}"

def info_grupo(usuario):
    """Información del grupo"""
    try:
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   👥 *INFO DEL GRUPO* 👥   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Grupo actual:* WhatsApp
👤 *Tu número:* +{usuario}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Comandos de admin:*
├─ {PREFIX}kick - Expulsar
├─ {PREFIX}ban - Banear
├─ {PREFIX}promover - Hacer admin
├─ {PREFIX}demover - Quitar admin
└─ {PREFIX}bienvenida - Configurar bienvenida
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def configurar_bienvenida(usuario, args):
    """Configurar mensaje de bienvenida"""
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"""
❌ *Uso:* {PREFIX}bienvenida [mensaje]

📝 *Variables disponibles:*
├─ {{usuario}} - Menciona al usuario
├─ {{grupo}} - Nombre del grupo
└─ {{fecha}} - Fecha actual

📌 *Ejemplo:* {PREFIX}bienvenida ¡Hola {{usuario}}! Bienvenido a {{grupo}}
            """
        
        mensaje = ' '.join(args)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  👋 *BIENVENIDA CONFIGURADA* 👋  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ *Mensaje:* {mensaje}

💡 *Variables usadas:*
├─ {{usuario}} - Menciona al usuario
├─ {{grupo}} - Nombre del grupo
└─ {{fecha}} - Fecha actual
        """
    except Exception as e:
        return f"❌ *Error:* {e}"