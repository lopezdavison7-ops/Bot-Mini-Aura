# -*- coding: utf-8 -*-

"""
🛡️ Sistema Anti-Spam para BOT MINI AURA
Versión: 4.0.0
"""

from datetime import datetime, timedelta
from config.settings import PREFIX, OWNER_NUMBER

# Variables globales
usuarios_advertidos = {}
mensajes_por_usuario = {}
antispam_activo = True

def toggle_antispam(usuario, args):
    """Activar o desactivar anti-spam"""
    global antispam_activo
    
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            estado = "activado" if antispam_activo else "desactivado"
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🛡️ *ANTI-SPAM* 🛡️   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📊 *Estado:* {estado}

💡 *Usa:* {PREFIX}antispam on/off
            """
        
        opcion = args[0].lower()
        
        if opcion in ['on', 'activar', 'si', '1']:
            antispam_activo = True
            return "✅ *Anti-spam activado*"
        elif opcion in ['off', 'desactivar', 'no', '0']:
            antispam_activo = False
            return "❌ *Anti-spam desactivado*"
        else:
            return f"❌ *Opción inválida*\n\nUsa: {PREFIX}antispam on/off"
            
    except Exception as e:
        return f"❌ *Error:* {e}"

def advertir_usuario(usuario, args):
    """Advertir a un usuario"""
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"❌ *Uso:* {PREFIX}warn [número]\n\nEjemplo: {PREFIX}warn 50512345678"
        
        objetivo = args[0]
        
        if objetivo not in usuarios_advertidos:
            usuarios_advertidos[objetivo] = {
                'cantidad': 0,
                'fecha': datetime.now().isoformat()
            }
        
        usuarios_advertidos[objetivo]['cantidad'] += 1
        usuarios_advertidos[objetivo]['fecha'] = datetime.now().isoformat()
        
        cantidad = usuarios_advertidos[objetivo]['cantidad']
        
        if cantidad >= 3:
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🚨 *USUARIO PELIGROSO* 🚨   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

⚠️ +{objetivo} tiene *{cantidad}* advertencias

💡 *Recomendación:* BANEAR al usuario
Usa: {PREFIX}banuser {objetivo}
            """
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ⚠️ *ADVERTENCIA ENVIADA* ⚠️   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👤 *Usuario:* +{objetivo}
📊 *Advertencias:* {cantidad}/3

💡 *A la tercera advertencia, banear*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def quitar_advertencia(usuario, args):
    """Quitar advertencia a un usuario"""
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"❌ *Uso:* {PREFIX}unwarn [número]"
        
        objetivo = args[0]
        
        if objetivo in usuarios_advertidos and usuarios_advertidos[objetivo]['cantidad'] > 0:
            usuarios_advertidos[objetivo]['cantidad'] -= 1
            restantes = usuarios_advertidos[objetivo]['cantidad']
            
            if restantes == 0:
                del usuarios_advertidos[objetivo]
            
            return f"""
✅ *Advertencia quitada*

👤 *Usuario:* +{objetivo}
📊 *Restantes:* {restantes}/3
            """
        else:
            return f"❌ *+{objetivo} no tiene advertencias*"
            
    except Exception as e:
        return f"❌ *Error:* {e}"

def ver_advertencias(usuario):
    """Ver todos los usuarios advertidos"""
    try:
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not usuarios_advertidos:
            return "📊 *No hay usuarios advertidos*"
        
        mensaje = """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   📊 *USUARIOS ADVERTIDOS* 📊   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

"""
        
        for num, datos in usuarios_advertidos.items():
            cantidad = datos['cantidad']
            emoji = '🚨' if cantidad >= 3 else '⚠️'
            mensaje += f"{emoji} *+{num}*\n   📊 {cantidad}/3 advertencias\n\n"
        
        mensaje += "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n💡 *3 advertencias = ban*"
        
        return mensaje
    except Exception as e:
        return f"❌ *Error:* {e}"

def verificar_spam(usuario, texto):
    """Verificar si un usuario está haciendo spam"""
    try:
        if not antispam_activo:
            return False
        
        ahora = datetime.now()
        
        if usuario not in mensajes_por_usuario:
            mensajes_por_usuario[usuario] = {
                'mensajes': [],
                'ultima_vez': ahora
            }
        
        datos = mensajes_por_usuario[usuario]
        
        # Limpiar mensajes viejos (más de 10 segundos)
        datos['mensajes'] = [m for m in datos['mensajes'] 
                            if (ahora - m['fecha']).seconds < 10]
        
        # Agregar mensaje actual
        datos['mensajes'].append({
            'texto': texto,
            'fecha': ahora
        })
        
        # Verificar si hay más de 5 mensajes en 10 segundos
        if len(datos['mensajes']) > 5:
            return True
        
        # Verificar mensajes repetidos
        textos = [m['texto'] for m in datos['mensajes']]
        for t in textos:
            if textos.count(t) > 3:
                return True
        
        return False
        
    except Exception as e:
        return False