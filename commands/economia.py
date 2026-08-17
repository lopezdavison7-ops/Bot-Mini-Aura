# -*- coding: utf-8 -*-

"""
💰 Sistema de Economía para BOT MINI AURA
Version: 2.0.0
"""

import random
from datetime import datetime, timedelta
from src.lib.database import Database
from config.settings import MONEDAS_POR_TRABAJO, PREFIX, OWNER_NUMBER

db = Database()

def ver_balance(usuario):
    """Ver balance de monedas del usuario"""
    try:
        datos = db.obtener_usuario(usuario)
        if not datos:
            db.crear_usuario(usuario)
            datos = db.obtener_usuario(usuario)
        
        monedas = datos.get('monedas', 0)
        banco = datos.get('banco', 0)
        nivel = datos.get('nivel', 1)
        exp = datos.get('exp', 0)
        
        # Calcular progreso de nivel
        progreso = (exp / 100) * 20  # 20 bloques de progreso
        barra = '█' * int(progreso) + '░' * (20 - int(progreso))
        
        mensaje = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    💰 *TU BALANCE* 💰     ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👤 *Usuario:* {usuario}
💎 *Monedas:* {monedas}
🏦 *Banco:* {banco}
⭐ *Nivel:* {nivel}
📊 *Experiencia:* {exp}/100
[{barra}]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Tip:* Usa {PREFIX}trabajar para ganar monedas
        """
        return mensaje
    except Exception as e:
        return f"❌ *Error al obtener balance:* {e}"

def trabajar(usuario):
    """Trabajar para ganar monedas"""
    try:
        datos = db.obtener_usuario(usuario)
        if not datos:
            db.crear_usuario(usuario)
            datos = db.obtener_usuario(usuario)
        
        # Verificar cooldown
        ultimo_trabajo = datos.get('ultimo_trabajo')
        if ultimo_trabajo:
            try:
                ultimo = datetime.fromisoformat(ultimo_trabajo)
                if datetime.now() - ultimo < timedelta(hours=1):
                    tiempo_restante = timedelta(hours=1) - (datetime.now() - ultimo)
                    minutos = int(tiempo_restante.total_seconds() // 60)
                    segundos = int(tiempo_restante.total_seconds() % 60)
                    return f"⏰ *¡Espera!* Debes esperar {minutos}m {segundos}s para trabajar de nuevo."
            except:
                pass
        
        # Generar monedas aleatorias
        monedas_ganadas = random.randint(MONEDAS_POR_TRABAJO, MONEDAS_POR_TRABAJO * 5)
        exp_ganada = random.randint(5, 15)
        
        # Actualizar base de datos
        db.actualizar_monedas(usuario, monedas_ganadas)
        db.actualizar_ultimo_trabajo(usuario)
        db.agregar_exp(usuario, exp_ganada)
        
        trabajos = [
            "programador", "chef", "mecánico", "doctor", "abogado",
            "artista", "músico", "carpintero", "electricista", "plomero",
            "diseñador", "profesor", "ingeniero", "arquitecto", "veterinario",
            "periodista", "fotógrafo", "barbero", "cocinero", "taxista"
        ]
        trabajo = random.choice(trabajos)
        
        emojis_trabajo = {
            "programador": "💻", "chef": "👨‍🍳", "mecánico": "🔧",
            "doctor": "👨‍⚕️", "abogado": "⚖️", "artista": "🎨",
            "músico": "🎵", "carpintero": "🪚", "electricista": "⚡",
            "plomero": "🔧", "diseñador": "🎨", "profesor": "📚",
            "ingeniero": "🏗️", "arquitecto": "📐", "veterinario": "🐾",
            "periodista": "📰", "fotógrafo": "📷", "barbero": "💈",
            "cocinero": "🍳", "taxista": "🚗"
        }
        
        emoji = emojis_trabajo.get(trabajo, "💼")
        
        mensaje = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   💼 *¡A TRABAJAR!* 💼    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{emoji} Trabajaste como *{trabajo}*
💰 Ganaste *{monedas_ganadas}* monedas
⭐ Experiencia ganada: *+{exp_ganada}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Vuelve en 1 hora para trabajar de nuevo
        """
        return mensaje
    except Exception as e:
        return f"❌ *Error al trabajar:* {e}"

def ver_ranking():
    """Ver ranking de usuarios"""
    try:
        top_usuarios = db.obtener_ranking(10)
        
        if not top_usuarios:
            return "📊 *Aún no hay usuarios registrados*"
        
        mensaje = """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🏆 *TOP 10 USUARIOS* 🏆    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

"""
        medallas = ['🥇', '🥈', '🥉']
        
        for i, usuario in enumerate(top_usuarios):
            medalla = medallas[i] if i < 3 else f"{i+1}️⃣"
            mensaje += f"{medalla} *{usuario['nombre']}*\n   💎 {usuario['monedas']} monedas | ⭐ Nivel {usuario['nivel']}\n\n"
        
        mensaje += "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n💡 *¡Sigue trabajando para subir!*"
        return mensaje
    except Exception as e:
        return f"❌ *Error al obtener ranking:* {e}"

def robar(usuario, args):
    """Intentar robar monedas a otro usuario"""
    try:
        if not args:
            return f"❌ *Uso incorrecto*\n\nEjemplo: {PREFIX}robar [número]\n{PREFIX}robar 50578391933"
        
        objetivo = args[0]
        
        if usuario == objetivo:
            return "❌ *No puedes robarte a ti mismo*"
        
        datos_objetivo = db.obtener_usuario(objetivo)
        if not datos_objetivo:
            return f"❌ *{objetivo} no tiene cuenta*\n\nEse usuario aún no se ha registrado."
        
        if datos_objetivo['monedas'] < 100:
            return f"❌ *{objetivo} no tiene suficientes monedas para robar*\n\nMínimo: 100 monedas"
        
        # Verificar cooldown de robo
        datos_usuario = db.obtener_usuario(usuario)
        if datos_usuario and datos_usuario.get('ultimo_robo'):
            ultimo = datetime.fromisoformat(datos_usuario['ultimo_robo'])
            if datetime.now() - ultimo < timedelta(minutes=30):
                tiempo_restante = timedelta(minutes=30) - (datetime.now() - ultimo)
                minutos = int(tiempo_restante.total_seconds() // 60)
                return f"⏰ *¡Espera!* Debes esperar {minutos} minutos para robar de nuevo."
        
        # Probabilidad de éxito (30%)
        if random.random() < 0.3:
            cantidad_robada = random.randint(10, datos_objetivo['monedas'] // 2)
            db.actualizar_monedas(objetivo, -cantidad_robada)
            db.actualizar_monedas(usuario, cantidad_robada)
            db.actualizar_ultimo_robo(usuario)
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🦹 *¡ROBO EXITOSO!* 🦹    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

💎 Robaste *{cantidad_robada}* monedas a {objetivo}
🏃 ¡Corre antes de que te atrapen!

⏰ Podrás robar de nuevo en 30 minutos
            """
        else:
            # Multa por intento fallido
            multa = random.randint(20, 50)
            db.actualizar_monedas(usuario, -multa)
            db.actualizar_ultimo_robo(usuario)
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    👮 *¡ATRAPADO!* 👮    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

❌ Fallaste en el robo
💸 Pagaste una multa de *{multa}* monedas

⏰ Podrás robar de nuevo en 30 minutos
            """
    except Exception as e:
        return f"❌ *Error al robar:* {e}"

def depositar(usuario, args):
    """Depositar monedas en el banco"""
    try:
        if not args or not args[0].isdigit():
            return f"❌ *Uso incorrecto*\n\nEjemplo: {PREFIX}depositar 100"
        
        cantidad = int(args[0])
        
        if cantidad <= 0:
            return "❌ *La cantidad debe ser mayor a 0*"
        
        datos = db.obtener_usuario(usuario)
        if not datos:
            return "❌ *No tienes cuenta*\n\nUsa " + PREFIX + "trabajar para crear una."
        
        if datos['monedas'] < cantidad:
            return f"❌ *No tienes suficientes monedas*\n\nTu balance: {datos['monedas']} monedas"
        
        db.actualizar_monedas(usuario, -cantidad)
        db.actualizar_banco(usuario, cantidad)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🏦 *DEPÓSITO EXITOSO* 🏦    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

💰 Depositaste: *{cantidad}* monedas
🏦 Balance del banco: *{datos['banco'] + cantidad}* monedas
        """
    except Exception as e:
        return f"❌ *Error al depositar:* {e}"

def retirar(usuario, args):
    """Retirar monedas del banco"""
    try:
        if not args or not args[0].isdigit():
            return f"❌ *Uso incorrecto*\n\nEjemplo: {PREFIX}retirar 100"
        
        cantidad = int(args[0])
        
        if cantidad <= 0:
            return "❌ *La cantidad debe ser mayor a 0*"
        
        datos = db.obtener_usuario(usuario)
        if not datos:
            return "❌ *No tienes cuenta*"
        
        if datos.get('banco', 0) < cantidad:
            return f"❌ *No tienes suficientes monedas en el banco*\n\nBalance del banco: {datos.get('banco', 0)} monedas"
        
        db.actualizar_banco(usuario, -cantidad)
        db.actualizar_monedas(usuario, cantidad)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🏦 *RETIRO EXITOSO* 🏦    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

💰 Retiraste: *{cantidad}* monedas
💎 Tu balance: *{datos['monedas'] + cantidad}* monedas
        """
    except Exception as e:
        return f"❌ *Error al retirar:* {e}"

def regalar_monedas(usuario, args):
    """Transferir monedas a otro usuario"""
    try:
        if len(args) < 2:
            return f"❌ *Uso incorrecto*\n\nEjemplo: {PREFIX}regalar [número] [cantidad]\n{PREFIX}regalar 50578391933 100"
        
        objetivo = args[0]
        
        if not args[1].isdigit():
            return "❌ *La cantidad debe ser un número*"
        
        cantidad = int(args[1])
        
        if cantidad <= 0:
            return "❌ *La cantidad debe ser mayor a 0*"
        
        if usuario == objetivo:
            return "❌ *No puedes transferirte a ti mismo*"
        
        datos = db.obtener_usuario(usuario)
        if not datos:
            return "❌ *No tienes cuenta*"
        
        if datos['monedas'] < cantidad:
            return f"❌ *No tienes suficientes monedas*\n\nTu balance: {datos['monedas']} monedas"
        
        # Verificar que el objetivo existe
        if not db.obtener_usuario(objetivo):
            db.crear_usuario(objetivo)
        
        db.actualizar_monedas(usuario, -cantidad)
        db.actualizar_monedas(objetivo, cantidad)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    💸 *TRANSFERENCIA* 💸    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✅ Transferiste *{cantidad}* monedas a {objetivo}
💎 Tu nuevo balance: *{datos['monedas'] - cantidad}* monedas
        """
    except Exception as e:
        return f"❌ *Error al transferir:* {e}"