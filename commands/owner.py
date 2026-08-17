# -*- coding: utf-8 -*-

"""
👑 Comandos de Owner para BOT MINI AURA
Version: 2.0.0
"""

import os
import sys
from datetime import datetime
from src.lib.database import Database
from config.settings import OWNER_NUMBER, OWNERS, PREFIX, VERSION

db = Database()

def es_owner(usuario):
    """Verificar si un usuario es owner"""
    return usuario in OWNERS or usuario == OWNER_NUMBER

def info_owner(usuario):
    """Información del owner"""
    if es_owner(usuario):
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    👑 *OWNER DEL BOT* 👑    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ *Eres el dueño del bot*

📱 *Tu número:* +{usuario}
🤖 *Bot:* MINI AURA
📊 *Versión:* {VERSION}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Comandos de owner disponibles:*
├─ {PREFIX}stats - Estadísticas
├─ {PREFIX}broadcast - Enviar anuncio
├─ {PREFIX}addowner - Agregar owner
├─ {PREFIX}delowner - Quitar owner
├─ {PREFIX}listowners - Lista de owners
├─ {PREFIX}usuarios - Lista de usuarios
├─ {PREFIX}dar - Dar monedas
├─ {PREFIX}quitar - Quitar monedas
├─ {PREFIX}reset - Resetear usuario
├─ {PREFIX}banuser - Banear usuario
└─ {PREFIX}unbanuser - Desbanear usuario
        """
    else:
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃      👑 *OWNER* 👑      ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Número:* +{OWNER_NUMBER}
🌐 *País:* Nicaragua 🇳🇮

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Contacta al owner para soporte*
        """

def estadisticas_bot(usuario):
    """Ver estadísticas del bot"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    try:
        total_usuarios = db.contar_usuarios()
        total_comandos = db.contar_comandos()
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    📊 *ESTADÍSTICAS* 📊    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👥 *Usuarios registrados:* {total_usuarios}
⚡ *Comandos ejecutados:* {total_comandos}
🤖 *Versión:* {VERSION}
📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y')}
⏰ *Hora:* {datetime.now().strftime('%H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 *Estado:* 🟢 Online
        """
    except Exception as e:
        return f"❌ *Error al obtener estadísticas:* {e}"

def broadcast(usuario, args):
    """Enviar anuncio a todos los usuarios"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    if not args:
        return f"❌ *Uso:* {PREFIX}broadcast [mensaje]\n\nEjemplo: {PREFIX}broadcast Actualización disponible"
    
    mensaje = ' '.join(args)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   📢 *ANUNCIO ENVIADO* 📢   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Mensaje:* {mensaje}
👥 *Destinatarios:* Todos los usuarios

✅ *Anuncio programado para envío*
    """

def agregar_owner(usuario, args):
    """Agregar nuevo owner"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    if not args:
        return f"❌ *Uso:* {PREFIX}addowner [número]\n\nEjemplo: {PREFIX}addowner 50512345678"
    
    nuevo_owner = args[0]
    
    if nuevo_owner in OWNERS:
        return f"❌ *{nuevo_owner} ya es owner*"
    
    OWNERS.append(nuevo_owner)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ✅ *OWNER AGREGADO* ✅   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👑 *Nuevo owner:* +{nuevo_owner}
📊 *Total owners:* {len(OWNERS)}
    """

def quitar_owner(usuario, args):
    """Quitar owner"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    if not args:
        return f"❌ *Uso:* {PREFIX}delowner [número]"
    
    owner_a_quitar = args[0]
    
    if owner_a_quitar == OWNER_NUMBER:
        return "❌ *No puedes quitar al owner principal*"
    
    if owner_a_quitar in OWNERS:
        OWNERS.remove(owner_a_quitar)
        return f"✅ *Owner {owner_a_quitar} eliminado*"
    else:
        return f"❌ *{owner_a_quitar} no es owner*"

def listar_owners(usuario):
    """Listar todos los owners"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    mensaje = """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    👑 *LISTA DE OWNERS* 👑    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

"""
    for i, owner in enumerate(OWNERS, 1):
        if owner == OWNER_NUMBER:
            mensaje += f"{i}️⃣ 👑 +{owner} *(Principal)*\n"
        else:
            mensaje += f"{i}️⃣ 👑 +{owner}\n"
    
    mensaje += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📊 *Total:* {len(OWNERS)} owners"
    
    return mensaje

def reiniciar_bot(usuario):
    """Reiniciar el bot"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    return """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🔄 *REINICIANDO BOT* 🔄   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

⏳ *El bot se reiniciará en 3 segundos...*
    """

def apagar_bot(usuario):
    """Apagar el bot"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    return """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🔴 *APAGANDO BOT* 🔴    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

⏳ *El bot se apagará...*

👋 *¡Hasta pronto!*
    """

def listar_usuarios(usuario):
    """Listar usuarios registrados"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    try:
        usuarios = db.obtener_todos_usuarios(10)
        
        if not usuarios:
            return "📊 *No hay usuarios registrados*"
        
        mensaje = """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   👥 *LISTA DE USUARIOS* 👥   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

"""
        for i, user in enumerate(usuarios, 1):
            mensaje += f"{i}️⃣ 📱 {user['telefono']}\n   💎 {user['monedas']} monedas\n\n"
        
        return mensaje
    except Exception as e:
        return f"❌ *Error:* {e}"

def dar_monedas(usuario, args):
    """Dar monedas a un usuario"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    if len(args) < 2:
        return f"❌ *Uso:* {PREFIX}dar [número] [cantidad]\n\nEjemplo: {PREFIX}dar 50512345678 100"
    
    objetivo = args[0]
    
    if not args[1].isdigit():
        return "❌ *La cantidad debe ser un número*"
    
    cantidad = int(args[1])
    
    if not db.obtener_usuario(objetivo):
        db.crear_usuario(objetivo)
    
    db.actualizar_monedas(objetivo, cantidad)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    💰 *MONEDAS DADAS* 💰    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ Diste *{cantidad}* monedas a +{objetivo}
    """

def quitar_monedas(usuario, args):
    """Quitar monedas a un usuario"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    if len(args) < 2:
        return f"❌ *Uso:* {PREFIX}quitar [número] [cantidad]"
    
    objetivo = args[0]
    
    if not args[1].isdigit():
        return "❌ *La cantidad debe ser un número*"
    
    cantidad = int(args[1])
    
    db.actualizar_monedas(objetivo, -cantidad)
    
    return f"✅ *Quitaste {cantidad} monedas a +{objetivo}*"

def reset_usuario(usuario, args):
    """Resetear usuario"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    if not args:
        return f"❌ *Uso:* {PREFIX}reset [número]"
    
    objetivo = args[0]
    
    db.reset_usuario(objetivo)
    
    return f"✅ *Usuario +{objetivo} reseteado correctamente*"

def banear_usuario_owner(usuario, args):
    """Banear usuario (owner)"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    if not args:
        return f"❌ *Uso:* {PREFIX}banuser [número]"
    
    objetivo = args[0]
    
    db.banear_usuario(objetivo)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🔨 *USUARIO BANEADO* 🔨    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ +{objetivo} ha sido baneado
    """

def desbanear_usuario_owner(usuario, args):
    """Desbanear usuario (owner)"""
    if not es_owner(usuario):
        return "❌ *No tienes permisos para usar este comando*"
    
    if not args:
        return f"❌ *Uso:* {PREFIX}unbanuser [número]"
    
    objetivo = args[0]
    
    db.desbanear_usuario(objetivo)
    
    return f"✅ *+{objetivo} ha sido desbaneado*"