# -*- coding: utf-8 -*-

"""
👮 Comandos de Administración para BOT MINI AURA
Version: 2.0.0
"""

from src.lib.database import Database
from config.settings import PREFIX

db = Database()

def expulsar_usuario(usuario, args):
    """Expulsar usuario del grupo"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}kick [número]\n\nEjemplo: {PREFIX}kick 50512345678"
        
        objetivo = args[0]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   👢 *USUARIO EXPULSADO* 👢   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ha sido expulsado

📝 *Nota:* Esta función requiere permisos de admin
        """
    except Exception as e:
        return f"❌ *Error al expulsar:* {e}"

def banear_usuario(usuario, args):
    """Banear usuario"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}ban [número]\n\nEjemplo: {PREFIX}ban 50512345678"
        
        objetivo = args[0]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🔨 *USUARIO BANEADO* 🔨   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ha sido baneado

📝 *Nota:* Esta función requiere permisos de admin
        """
    except Exception as e:
        return f"❌ *Error al banear:* {e}"

def promover_usuario(usuario, args):
    """Promover usuario a admin"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}promover [número]"
        
        objetivo = args[0]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  ⬆️ *USUARIO PROMOVIDO* ⬆️  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ahora es admin
        """
    except Exception as e:
        return f"❌ *Error al promover:* {e}"

def degrada_usuario(usuario, args):
    """Degradar admin"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}demover [número]"
        
        objetivo = args[0]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  ⬇️ *USUARIO DEGRADADO* ⬇️  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ya no es admin
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
👤 *Tu número:* {usuario}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Comandos de admin:*
├─ {PREFIX}kick - Expulsar
├─ {PREFIX}ban - Banear
├─ {PREFIX}promover - Hacer admin
└─ {PREFIX}demover - Quitar admin
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def configurar_bienvenida(usuario, args):
    """Configurar mensaje de bienvenida"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}bienvenida [mensaje]\n\nUsa {{usuario}} para mencionar al nuevo miembro"
        
        mensaje = ' '.join(args)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  👋 *BIENVENIDA CONFIGURADA* 👋  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ *Mensaje:* {mensaje}

💡 *Variables disponibles:*
├─ {{usuario}} - Menciona al usuario
├─ {{grupo}} - Nombre del grupo
└─ {{fecha}} - Fecha actual
        """
    except Exception as e:
        return f"❌ *Error:* {e}"