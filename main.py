#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 BOT MINI AURA - Bot Multi-propósito para WhatsApp
Versión: 3.0.0
Owner: +50578391933
Sistema: Baileys Python
Total de comandos: 101
"""

import asyncio
import json
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('MINI-AURA')

# Importar Baileys
try:
    from baileys import WhatsAppSocket
except ImportError:
    logger.error("Baileys no instalado. Ejecuta: pip install baileys")
    exit(1)

# Importar configuraciones
from config.settings import *
from lib.database import Database
from lib.vincular import SistemaVinculacion

# ==================== CLASE PRINCIPAL ====================

class BotMiniAura:
    def __init__(self):
        self.socket = None
        self.db = Database()
        self.db.initialize()
        self.sistema_vinculacion = SistemaVinculacion()
        self.codigos_pendientes = {}
        self.mensajes_procesados = set()
    
    async def iniciar(self):
        """Iniciar el bot"""
        try:
            logger.info("🚀 Iniciando BOT MINI AURA...")
            
            # Crear socket de WhatsApp
            self.socket = WhatsAppSocket()
            
            # Mostrar QR
            print("\n" + "=" * 60)
            print("📱 *ESCANEA EL CÓDIGO QR CON TU WHATSAPP*")
            print("=" * 60 + "\n")
            
            # Esperar conexión
            await self.socket.wait_for_connection()
            
            logger.info("✅ ¡Conectado a WhatsApp!")
            print("\n" + "=" * 60)
            print("🤖 *BOT MINI AURA - ACTIVO*")
            print(f"👑 Owner: +{OWNER_NUMBER}")
            print("📊 Total comandos: 101")
            print("=" * 60 + "\n")
            
            # Escuchar mensajes
            @self.socket.on_message
            async def on_message(message):
                await self.procesar_mensaje(message)
            
            # Mantener bot activo
            await asyncio.Future()
            
        except Exception as e:
            logger.error(f"Error al iniciar: {e}")
    
    async def procesar_mensaje(self, message):
        """Procesar mensajes recibidos"""
        try:
            texto = message.text.strip()
            remitente = message.from_user
            
            # Evitar procesar mensajes duplicados
            if texto in self.mensajes_procesados:
                return
            self.mensajes_procesados.add(texto)
            
            logger.info(f"Mensaje de {remitente}: {texto}")
            
            # Procesar comando
            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' ' in texto else []
                
                respuesta = await self.ejecutar_comando(comando, args, remitente)
                
            else:
                respuesta = self.procesar_mensaje_normal(texto, remitente)
            
            # Enviar respuesta
            if respuesta:
                await self.socket.send_message(remitente, respuesta)
                logger.info(f"Respuesta enviada a {remitente}")
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
    
    async def ejecutar_comando(self, comando, args, remitente):
        """Ejecutar comando"""
        try:
            # ============ COMANDOS DE VINCULACIÓN ============
            if comando in ['vincular', 'link', 'conectar']:
                return self.comando_vincular(remitente, args)
            
            elif comando in ['codigo', 'code']:
                return self.comando_codigo(remitente)
            
            elif comando in ['verificar', 'verify']:
                return self.comando_verificar(remitente, args)
            
            elif comando in ['estado', 'status']:
                return self.comando_estado(remitente)
            
            elif comando in ['desvincular', 'unlink']:
                return self.comando_desvincular(remitente)
            
            # ============ VERIFICAR VINCULACIÓN ============
            if not self.sistema_vinculacion.esta_vinculado(remitente) and remitente != OWNER_NUMBER:
                return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ⚠️ *VINCULACIÓN REQUERIDA* ⚠️   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

❌ *Debes vincularte para usar el bot*

🔗 *Para vincularte:*
Escribe: {PREFIX}vincular [tu_número]

📌 *Ejemplo:* {PREFIX}vincular 50578391933
                """
            
            # ============ COMANDOS GENERALES ============
            if comando in ['menu', 'ayuda', 'help', 'start']:
                from commands.menu import mostrar_menu_principal
                return mostrar_menu_principal()
            
            elif comando in ['ping', 'test', 'latencia']:
                from commands.utilidades import verificar_ping
                return verificar_ping()
            
            elif comando in ['info', 'bot', 'about']:
                from commands.utilidades import info_bot
                return info_bot()
            
            # ============ ECONOMÍA ============
            elif comando in ['monedas', 'balance', 'bal', 'wallet']:
                from commands.economia import ver_balance
                return ver_balance(remitente)
            
            elif comando in ['trabajar', 'work', 'minar']:
                from commands.economia import trabajar
                return trabajar(remitente)
            
            elif comando in ['top', 'ranking', 'top10']:
                from commands.economia import ver_ranking
                return ver_ranking()
            
            elif comando in ['robar', 'steal']:
                from commands.economia import robar
                return robar(remitente, args)
            
            elif comando in ['depositar', 'dep', 'banco']:
                from commands.economia import depositar
                return depositar(remitente, args)
            
            elif comando in ['retirar', 'ret', 'sacar']:
                from commands.economia import retirar
                return retirar(remitente, args)
            
            elif comando in ['regalar', 'enviar', 'transferir']:
                from commands.economia import regalar_monedas
                return regalar_monedas(remitente, args)# ============ JUEGOS ============
elif comando in ['dado', 'dice', 'roll']:
    from commands.juegos import tirar_dado
    return tirar_dado(remitente)

elif comando in ['moneda', 'coinflip', 'cara']:
    from commands.juegos import lanzar_moneda
    return lanzar_moneda(remitente)

elif comando in ['ppt', 'piedra', 'rps']:
    from commands.juegos import piedra_papel_tijera
    return piedra_papel_tijera(remitente, args)

elif comando in ['ahorcado', 'ahorcar']:
    from commands.juegos import ahorcado
    return ahorcado(remitente)

elif comando in ['trivia', 'quiz']:
    from commands.juegos import trivia
    return trivia(remitente)

elif comando in ['ruleta', 'rusa']:
    from commands.juegos import ruleta_rusa
    return ruleta_rusa(remitente)

elif comando in ['loteria', 'loto']:
    from commands.juegos import loteria
    return loteria(remitente)

# ============ UTILIDADES ============
elif comando in ['clima', 'weather']:
    from commands.utilidades import obtener_clima
    return obtener_clima(args)

elif comando in ['calc', 'calcular', 'math']:
    from commands.utilidades import calculadora
    return calculadora(args)

elif comando in ['password', 'pass']:
    from commands.utilidades import generar_password
    return generar_password(args)

elif comando in ['fecha', 'date']:
    from commands.utilidades import ver_fecha
    return ver_fecha()

elif comando in ['hora', 'time']:
    from commands.utilidades import ver_hora
    return ver_hora()

elif comando in ['binario', 'bin']:
    from commands.utilidades import texto_binario
    return texto_binario(args)

elif comando in ['hex', 'hexadecimal']:
    from commands.utilidades import texto_hex
    return texto_hex(args)

elif comando in ['base64', 'b64']:
    from commands.utilidades import texto_base64
    return texto_base64(args)

elif comando in ['md5', 'hash']:
    from commands.utilidades import texto_md5
    return texto_md5(args)

elif comando in ['reverso', 'reverse']:
    from commands.utilidades import texto_reverso
    return texto_reverso(args)

elif comando in ['mayus', 'uppercase']:
    from commands.utilidades import texto_mayus
    return texto_mayus(args)

elif comando in ['minus', 'lowercase']:
    from commands.utilidades import texto_minus
    return texto_minus(args)

elif comando in ['contar', 'count']:
    from commands.utilidades import contar_caracteres
    return contar_caracteres(args)

# ============ DIVERSIÓN ============
elif comando in ['dato', 'fact']:
    from commands.diversion import dato_curioso
    return dato_curioso()

elif comando in ['chiste', 'joke']:
    from commands.diversion import chiste
    return chiste()

elif comando in ['frase', 'motivacion']:
    from commands.diversion import frase_motivacional
    return frase_motivacional()

elif comando in ['piropo', 'halago']:
    from commands.diversion import piropo
    return piropo()

elif comando in ['8ball', 'bola']:
    from commands.diversion import bola_ocho
    return bola_ocho(args)

elif comando in ['amor', 'love']:
    from commands.diversion import calcular_amor
    return calcular_amor(args)

elif comando in ['edad', 'age']:
    from commands.diversion import calcular_edad
    return calcular_edad(args)

elif comando in ['nombre', 'randomname']:
    from commands.diversion import generar_nombre
    return generar_nombre()

elif comando in ['color', 'randomcolor']:
    from commands.diversion import color_aleatorio
    return color_aleatorio()

elif comando in ['emoji', 'randomemoji']:
    from commands.diversion import emoji_aleatorio
    return emoji_aleatorio()

# ============ EXCLUSIVOS ============
elif comando in ['futuro', 'predecir']:
    from commands.exclusivos import predecir_futuro
    return predecir_futuro(remitente, args)

elif comando in ['match', 'compatibilidad']:
    from commands.exclusivos import compatibilidad_nombres
    return compatibilidad_nombres(args)

elif comando in ['test', 'personalidad']:
    from commands.exclusivos import test_personalidad
    return test_personalidad(remitente, args)

elif comando in ['correo', 'email']:
    from commands.exclusivos import generar_correo
    return generar_correo(args)

elif comando in ['iguser', 'usuarioig']:
    from commands.exclusivos import generar_usuario_instagram
    return generar_usuario_instagram(args)

elif comando in ['bio', 'biografia']:
    from commands.exclusivos import generar_bio
    return generar_bio(args)

elif comando in ['horoscopo', 'signo']:
    from commands.exclusivos import horoscopo_diario
    return horoscopo_diario(args)

elif comando in ['imc', 'masacorporal']:
    from commands.exclusivos import calcular_imc
    return calcular_imc(args)

elif comando in ['regla3', 'reglatres']:
    from commands.exclusivos import calcular_regla_tres
    return calcular_regla_tres(args)

elif comando in ['descuento', 'oferta']:
    from commands.exclusivos import calcular_descuento
    return calcular_descuento(args)

elif comando in ['cuenta', 'countdown']:
    from commands.exclusivos import cuenta_regresiva
    return cuenta_regresiva(args)

elif comando in ['edadexacta', 'exacta']:
    from commands.exclusivos import edad_exacta
    return edad_exacta(args)

elif comando in ['leet', '1337']:
    from commands.exclusivos import texto_leet
    return texto_leet(args)

elif comando in ['morse', 'codigomorse']:
    from commands.exclusivos import texto_morse
    return texto_morse(args)

elif comando in ['textemoji', 'emoji_texto']:
    from commands.exclusivos import texto_emoji
    return texto_emoji(args)            # ============ PREMIUM ============
            elif comando in ['analizar', 'texto']:
                from commands.premium import analizar_texto
                return analizar_texto(args)
            
            elif comando in ['numero', 'num']:
                from commands.premium import analizar_numero
                return analizar_numero(args)
            
            elif comando in ['temp', 'temperatura']:
                from commands.premium import convertir_temperatura
                return convertir_temperatura(args)
            
            elif comando in ['distancia', 'longitud']:
                from commands.premium import convertir_distancia
                return convertir_distancia(args)
            
            elif comando in ['historia', 'cuento']:
                from commands.premium import generar_historia
                return generar_historia(args)
            
            elif comando in ['poema', 'poesia']:
                from commands.premium import generar_poema
                return generar_poema(args)
            
            elif comando in ['consejo', 'tip']:
                from commands.premium import generar_consejo
                return generar_consejo(args)
            
            elif comando in ['palabras', 'wordgame']:
                from commands.premium import juego_palabras
                return juego_palabras(args)
            
            # ============ DESCONOCIDO ============
            else:
                return f"❌ *Comando no reconocido*\n\nEscribe *{PREFIX}menu* para ver todos los comandos."
                
        except Exception as e:
            logger.error(f"Error ejecutando comando: {e}")
            return "⚠️ *Error interno*"
    
    # ============ COMANDOS DE VINCULACIÓN ============
    
    def comando_vincular(self, usuario, args):
        if self.sistema_vinculacion.esta_vinculado(usuario):
            return f"✅ *Ya estás vinculado*\n\nEscribe {PREFIX}menu para comenzar"
        
        if not args:
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔗 *VINCULACIÓN DE BOT* 🔗  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

Escribe: {PREFIX}vincular [tu_número]
Ejemplo: {PREFIX}vincular 50578391933

Después escribe: {PREFIX}codigo
            """
        
        numero = args[0]
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔗 *VINCULACIÓN INICIADA* 🔗  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Número:* {numero}

Escribe: {PREFIX}codigo
Para recibir tu código de 8 dígitos
        """
    
    def comando_codigo(self, usuario):
        codigo = self.sistema_vinculacion.generar_codigo(usuario)
        
        if not codigo:
            return "❌ *Error al generar código*"
        
        logger.info(f"Código para {usuario}: {codigo}")
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🔢 *CÓDIGO DE VINCULACIÓN* 🔢   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Tu código es:*

*{codigo[0:4]} {codigo[4:8]}*

Escribe: {PREFIX}verificar {codigo}

⏰ *Válido por 5 minutos*
🔒 *Tienes 3 intentos*
        """
    
    def comando_verificar(self, usuario, args):
        if not args:
            return f"❌ *Uso:* {PREFIX}verificar [código]"
        
        codigo_ingresado = args[0].replace(' ', '')
        
        resultado = self.sistema_vinculacion.verificar_codigo(usuario, codigo_ingresado)
        
        return resultado['mensaje']
    
    def comando_estado(self, usuario):
        if self.sistema_vinculacion.esta_vinculado(usuario):
            return f"✅ *Ya estás vinculado*\n\nEscribe {PREFIX}menu para comenzar"
        return f"❌ *No estás vinculado*\n\nEscribe {PREFIX}vincular [tu_número]"
    
    def comando_desvincular(self, usuario):
        if self.sistema_vinculacion.desvincular(usuario):
            return "✅ *Has sido desvinculado*"
        return "❌ *No estabas vinculado*"
    
    def procesar_mensaje_normal(self, mensaje, remitente):
        mensaje_lower = mensaje.lower()
        
        respuestas = {
            'hola': '¡Hola! 👋 Soy *MINI AURA*\n\nEscribe *.menu* para ver todo lo que puedo hacer.',
            'buenos días': '¡Buenos días! ☀️ Espero que tengas un excelente día.',
            'buenas tardes': '¡Buenas tardes! 🌤️',
            'buenas noches': '¡Buenas noches! 🌙',
            'como estas': '¡Estoy genial! 💪 Siempre listo para ayudarte.',
            'gracias': '¡De nada! 😊',
            'adios': '¡Hasta luego! 👋',
            'te amo': '¡Yo también te quiero! 💙',
            'quien te creo': f'Fui creado por un desarrollador genial 💻\n\nEscribe *.info* para conocerme mejor.',
            'owner': f'Mi dueño es +{OWNER_NUMBER} 👑',
            'menu': f'Escribe *{PREFIX}menu* para ver todos los comandos disponibles.',
            'comandos': f'Escribe *{PREFIX}menu* para ver los 101 comandos disponibles.',
        }
        
        for clave, respuesta in respuestas.items():
            if clave in mensaje_lower:
                return respuesta
        
        return f"No entendí tu mensaje 🤔\n\nEscribe *{PREFIX}menu* para ver los comandos."


# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    bot = BotMiniAura()
    asyncio.run(bot.iniciar())