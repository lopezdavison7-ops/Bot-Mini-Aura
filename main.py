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
        logging.FileHandler('logs/bot.log'),
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
from src.lib.database import Database

# ==================== CLASE PRINCIPAL ====================

class BotMiniAura:
    def __init__(self):
        self.socket = None
        self.db = Database()
        self.db.initialize()
        self.vinculados = self.cargar_vinculados()
        self.codigos_pendientes = {}
        self.mensajes_procesados = set()
        
    def cargar_vinculados(self):
        """Cargar usuarios vinculados"""
        try:
            archivo = Path('src/data/json/vinculados.json')
            if archivo.exists():
                with open(archivo, 'r') as f:
                    return set(json.load(f))
            return set()
        except:
            return set()
    
    def guardar_vinculados(self):
        """Guardar usuarios vinculados"""
        try:
            archivo = Path('src/data/json/vinculados.json')
            archivo.parent.mkdir(parents=True, exist_ok=True)
            with open(archivo, 'w') as f:
                json.dump(list(self.vinculados), f, indent=2)
        except Exception as e:
            logger.error(f"Error guardando vinculados: {e}")
    
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
            if remitente not in self.vinculados and remitente != OWNER_NUMBER:
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
                from src.commands.menu import mostrar_menu_principal
                return mostrar_menu_principal()
            
            elif comando in ['ping', 'test', 'latencia']:
                from src.commands.utilidades import verificar_ping
                return verificar_ping()
            
            elif comando in ['info', 'bot', 'about']:
                from src.commands.utilidades import info_bot
                return info_bot()
            
            # ============ ECONOMÍA ============
            elif comando in ['monedas', 'balance', 'bal', 'wallet']:
                from src.commands.economia import ver_balance
                return ver_balance(remitente)
            
            elif comando in ['trabajar', 'work', 'minar']:
                from src.commands.economia import trabajar
                return trabajar(remitente)
            
            elif comando in ['top', 'ranking', 'top10']:
                from src.commands.economia import ver_ranking
                return ver_ranking()
            
            elif comando in ['robar', 'steal']:
                from src.commands.economia import robar
                return robar(remitente, args)
            
            elif comando in ['depositar', 'dep', 'banco']:
                from src.commands.economia import depositar
                return depositar(remitente, args)
            
            elif comando in ['retirar', 'ret', 'sacar']:
                from src.commands.economia import retirar
                return retirar(remitente, args)
            
            elif comando in ['regalar', 'enviar', 'transferir']:
                from src.commands.economia import regalar_monedas
                return regalar_monedas(remitente, args)# ============ JUEGOS ============
elif comando in ['dado', 'dice', 'roll']:
    from src.commands.juegos import tirar_dado
    return tirar_dado(remitente)

elif comando in ['moneda', 'coinflip', 'cara']:
    from src.commands.juegos import lanzar_moneda
    return lanzar_moneda(remitente)

elif comando in ['ppt', 'piedra', 'rps']:
    from src.commands.juegos import piedra_papel_tijera
    return piedra_papel_tijera(remitente, args)

elif comando in ['ahorcado', 'ahorcar']:
    from src.commands.juegos import ahorcado
    return ahorcado(remitente)

elif comando in ['trivia', 'quiz']:
    from src.commands.juegos import trivia
    return trivia(remitente)

elif comando in ['ruleta', 'rusa']:
    from src.commands.juegos import ruleta_rusa
    return ruleta_rusa(remitente)

elif comando in ['loteria', 'loto']:
    from src.commands.juegos import loteria
    return loteria(remitente)

# ============ UTILIDADES ============
elif comando in ['clima', 'weather']:
    from src.commands.utilidades import obtener_clima
    return obtener_clima(args)

elif comando in ['calc', 'calcular', 'math']:
    from src.commands.utilidades import calculadora
    return calculadora(args)

elif comando in ['password', 'pass']:
    from src.commands.utilidades import generar_password
    return generar_password(args)

elif comando in ['fecha', 'date']:
    from src.commands.utilidades import ver_fecha
    return ver_fecha()

elif comando in ['hora', 'time']:
    from src.commands.utilidades import ver_hora
    return ver_hora()

elif comando in ['binario', 'bin']:
    from src.commands.utilidades import texto_binario
    return texto_binario(args)

elif comando in ['hex', 'hexadecimal']:
    from src.commands.utilidades import texto_hex
    return texto_hex(args)

elif comando in ['base64', 'b64']:
    from src.commands.utilidades import texto_base64
    return texto_base64(args)

elif comando in ['md5', 'hash']:
    from src.commands.utilidades import texto_md5
    return texto_md5(args)

elif comando in ['reverso', 'reverse']:
    from src.commands.utilidades import texto_reverso
    return texto_reverso(args)

elif comando in ['mayus', 'uppercase']:
    from src.commands.utilidades import texto_mayus
    return texto_mayus(args)

elif comando in ['minus', 'lowercase']:
    from src.commands.utilidades import texto_minus
    return texto_minus(args)

elif comando in ['contar', 'count']:
    from src.commands.utilidades import contar_caracteres
    return contar_caracteres(args)

# ============ DIVERSIÓN ============
elif comando in ['dato', 'fact']:
    from src.commands.diversion import dato_curioso
    return dato_curioso()

elif comando in ['chiste', 'joke']:
    from src.commands.diversion import chiste
    return chiste()

elif comando in ['frase', 'motivacion']:
    from src.commands.diversion import frase_motivacional
    return frase_motivacional()

elif comando in ['piropo', 'halago']:
    from src.commands.diversion import piropo
    return piropo()

elif comando in ['8ball', 'bola']:
    from src.commands.diversion import bola_ocho
    return bola_ocho(args)

elif comando in ['amor', 'love']:
    from src.commands.diversion import calcular_amor
    return calcular_amor(args)

elif comando in ['edad', 'age']:
    from src.commands.diversion import calcular_edad
    return calcular_edad(args)

elif comando in ['nombre', 'randomname']:
    from src.commands.diversion import generar_nombre
    return generar_nombre()

elif comando in ['color', 'randomcolor']:
    from src.commands.diversion import color_aleatorio
    return color_aleatorio()

elif comando in ['emoji', 'randomemoji']:
    from src.commands.diversion import emoji_aleatorio
    return emoji_aleatorio()

# ============ EXCLUSIVOS ============
elif comando in ['futuro', 'predecir']:
    from src.commands.exclusivos import predecir_futuro
    return predecir_futuro(remitente, args)

elif comando in ['match', 'compatibilidad']:
    from src.commands.exclusivos import compatibilidad_nombres
    return compatibilidad_nombres(args)

elif comando in ['test', 'personalidad']:
    from src.commands.exclusivos import test_personalidad
    return test_personalidad(remitente, args)

elif comando in ['correo', 'email']:
    from src.commands.exclusivos import generar_correo
    return generar_correo(args)

elif comando in ['iguser', 'usuarioig']:
    from src.commands.exclusivos import generar_usuario_instagram
    return generar_usuario_instagram(args)

elif comando in ['bio', 'biografia']:
    from src.commands.exclusivos import generar_bio
    return generar_bio(args)

elif comando in ['horoscopo', 'signo']:
    from src.commands.exclusivos import horoscopo_diario
    return horoscopo_diario(args)

elif comando in ['imc', 'masacorporal']:
    from src.commands.exclusivos import calcular_imc
    return calcular_imc(args)

elif comando in ['regla3', 'reglatres']:
    from src.commands.exclusivos import calcular_regla_tres
    return calcular_regla_tres(args)

elif comando in ['descuento', 'oferta']:
    from src.commands.exclusivos import calcular_descuento
    return calcular_descuento(args)

elif comando in ['cuenta', 'countdown']:
    from src.commands.exclusivos import cuenta_regresiva
    return cuenta_regresiva(args)

elif comando in ['edadexacta', 'exacta']:
    from src.commands.exclusivos import edad_exacta
    return edad_exacta(args)

elif comando in ['leet', '1337']:
    from src.commands.exclusivos import texto_leet
    return texto_leet(args)

elif comando in ['morse', 'codigomorse']:
    from src.commands.exclusivos import texto_morse
    return texto_morse(args)

elif comando in ['textemoji', 'emoji_texto']:
    from src.commands.exclusivos import texto_emoji
    return texto_emoji(args)            # ============ PREMIUM ============
            elif comando in ['analizar', 'texto']:
                from src.commands.premium import analizar_texto
                return analizar_texto(args)
            
            elif comando in ['numero', 'num']:
                from src.commands.premium import analizar_numero
                return analizar_numero(args)
            
            elif comando in ['temp', 'temperatura']:
                from src.commands.premium import convertir_temperatura
                return convertir_temperatura(args)
            
            elif comando in ['distancia', 'longitud']:
                from src.commands.premium import convertir_distancia
                return convertir_distancia(args)
            
            elif comando in ['historia', 'cuento']:
                from src.commands.premium import generar_historia
                return generar_historia(args)
            
            elif comando in ['poema', 'poesia']:
                from src.commands.premium import generar_poema
                return generar_poema(args)
            
            elif comando in ['consejo', 'tip']:
                from src.commands.premium import generar_consejo
                return generar_consejo(args)
            
            elif comando in ['palabras', 'wordgame']:
                from src.commands.premium import juego_palabras
                return juego_palabras(args)
            
            # ============ DESCONOCIDO ============
            else:
                return f"❌ *Comando no reconocido*\n\nEscribe *{PREFIX}menu* para ver todos los comandos."
                
        except Exception as e:
            logger.error(f"Error ejecutando comando: {e}")
            return "⚠️ *Error interno*"
    
    # ============ COMANDOS DE VINCULACIÓN ============
    
    def comando_vincular(self, usuario, args):
        if usuario in self.vinculados:
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
        codigo = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        self.codigos_pendientes[usuario] = {
            'codigo': codigo,
            'fecha': datetime.now(),
            'intentos': 0
        }
        
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
        
        if usuario not in self.codigos_pendientes:
            return "❌ *No hay código pendiente*\n\nEscribe .codigo para recibir uno"
        
        datos = self.codigos_pendientes[usuario]
        
        # Verificar expiración
        if datetime.now() - datos['fecha'] > timedelta(minutes=5):
            del self.codigos_pendientes[usuario]
            return "⏰ *Código expirado*\n\nEscribe .codigo para uno nuevo"
        
        # Verificar intentos
        if datos['intentos'] >= 3:
            del self.codigos_pendientes[usuario]
            return "❌ *Demasiados intentos*\n\nEscribe .codigo para uno nuevo"
        
        # Verificar código
        if codigo_ingresado == datos['codigo']:
            self.vinculados.add(usuario)
            self.guardar_vinculados()
            del self.codigos_pendientes[usuario]
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃ ✅ *¡VINCULACIÓN EXITOSA!* ✅ ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🎉 *¡Tu número ha sido vinculado!*

📱 *Número:* {usuario}

Escribe {PREFIX}menu para comenzar
            """
        else:
            self.codigos_pendientes[usuario]['intentos'] += 1
            intentos_restantes = 3 - datos['intentos'] - 1
            return f"❌ *Código incorrecto*\n\nTe quedan {intentos_restantes} intentos"
    
    def comando_estado(self, usuario):
        if usuario in self.vinculados:
            return f"✅ *Ya estás vinculado*\n\nEscribe {PREFIX}menu para comenzar"
        return f"❌ *No estás vinculado*\n\nEscribe {PREFIX}vincular [tu_número]"
    
    def comando_desvincular(self, usuario):
        if usuario in self.vinculados:
            self.vinculados.remove(usuario)
            self.guardar_vinculados()
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
        }
        
        for clave, respuesta in respuestas.items():
            if clave in mensaje_lower:
                return respuesta
        
        return f"No entendí tu mensaje 🤔\n\nEscribe *{PREFIX}menu* para ver los comandos."


# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    bot = BotMiniAura()
    asyncio.run(bot.iniciar())