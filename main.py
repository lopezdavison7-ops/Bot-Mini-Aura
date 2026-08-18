#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 BOT MINI AURA - Bot Multi-propósito para WhatsApp
Versión: 4.0.0
Owner: +50578391933
Sistema: Baileys Python
Total de comandos: 130+
"""

import asyncio
import json
import random
import logging
import re
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

# Importar todos los comandos
from commands.menu import *
from commands.economia import *
from commands.juegos import *
from commands.utilidades import *
from commands.diversion import *
from commands.exclusivos import *
from commands.premium import *
from commands.owner import *
from commands.admin import *
from commands.antispam import *

# ==================== CLASE PRINCIPAL ====================

class BotMiniAura:
    def __init__(self):
        self.socket = None
        self.db = Database()
        self.db.initialize()
        self.sistema_vinculacion = SistemaVinculacion()
        self.mensajes_procesados = set()
        self.usuarios_advertidos = {}
        self.antispam_activo = True
        self.ultimo_mensaje = {}
        self.mensajes_seguidos = {}
    
    async def iniciar(self):
        """Iniciar el bot"""
        try:
            logger.info("🚀 Iniciando BOT MINI AURA...")
            
            self.socket = WhatsAppSocket()
            
            print("\n" + "=" * 60)
            print("📱 *ESCANEA EL CÓDIGO QR CON TU WHATSAPP*")
            print("=" * 60 + "\n")
            
            await self.socket.wait_for_connection()
            
            logger.info("✅ ¡Conectado a WhatsApp!")
            print("\n" + "=" * 60)
            print("🤖 *BOT MINI AURA - ACTIVO*")
            print(f"👑 Owner: +{OWNER_NUMBER}")
            print("📊 Total comandos: 130+")
            print("🛡️ Anti-spam: Activado")
            print("=" * 60 + "\n")
            
            @self.socket.on_message
            async def on_message(message):
                await self.procesar_mensaje(message)
            
            await asyncio.Future()
            
        except Exception as e:
            logger.error(f"Error al iniciar: {e}")
    
    async def procesar_mensaje(self, message):
        """Procesar mensajes recibidos"""
        try:
            texto = message.text.strip()
            remitente = message.from_user
            
            # Validar mensaje
            if not texto:
                return
            
            # Anti-spam
            if await self.verificar_spam(remitente, texto):
                await self.socket.send_message(remitente, "⚠️ *Anti-spam activado*\n\nHas enviado muchos mensajes. Espera 30 segundos.")
                return
            
            # Evitar duplicados
            if texto in self.mensajes_procesados:
                return
            self.mensajes_procesados.add(texto)
            
            logger.info(f"Mensaje de {remitente}: {texto[:50]}")
            
            # Obtener mención
            mencion = f"@{remitente.split('@')[0]}"
            
            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' ' in texto else []
                respuesta = await self.ejecutar_comando(comando, args, remitente, mencion)
            else:
                respuesta = self.procesar_mensaje_normal(texto, remitente, mencion)
            
            if respuesta:
                await self.socket.send_message(remitente, respuesta)
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
    
    async def verificar_spam(self, usuario, texto):
        """Verificar anti-spam"""
        try:
            if not self.antispam_activo:
                return False
            
            ahora = datetime.now()
            
            # Verificar mensajes seguidos
            if usuario in self.mensajes_seguidos:
                datos = self.mensajes_seguidos[usuario]
                if (ahora - datos['fecha']).seconds < 2:
                    datos['cantidad'] += 1
                else:
                    datos['cantidad'] = 1
                datos['fecha'] = ahora
                
                if datos['cantidad'] > 5:
                    return True
            else:
                self.mensajes_seguidos[usuario] = {
                    'cantidad': 1,
                    'fecha': ahora
                }
            
            return False
        except:
            return False
    
    async def ejecutar_comando(self, comando, args, remitente, mencion):
        """Ejecutar comando"""
        try:
            # ============ VINCULACIÓN ============
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

❌ *Hola {mencion}*

Debes vincularte para usar el bot

🔗 *Para vincularte:*
Escribe: {PREFIX}vincular [tu_número]

📌 *Ejemplo:* {PREFIX}vincular 50578391933
                """
            
            # ============ GENERALES ============
            if comando in ['menu', 'ayuda', 'help', 'start']:
                return f"👋 *Hola {mencion}*\n\n{mostrar_menu_principal()}"
            elif comando in ['ping', 'test', 'latencia']:
                return verificar_ping()
            elif comando in ['info', 'bot', 'about']:
                return info_bot()
            
            # ============ ECONOMÍA ============
            elif comando in ['monedas', 'balance', 'bal', 'wallet']:
                return f"👤 *{mencion}*\n\n{ver_balance(remitente)}"
            elif comando in ['trabajar', 'work', 'minar']:
                return f"👤 *{mencion}*\n\n{trabajar(remitente)}"
            elif comando in ['top', 'ranking', 'top10']:
                return ver_ranking()
            elif comando in ['robar', 'steal']:
                return robar(remitente, args)
            elif comando in ['depositar', 'dep', 'banco']:
                return depositar(remitente, args)
            elif comando in ['retirar', 'ret', 'sacar']:
                return retirar(remitente, args)
            elif comando in ['regalar', 'enviar', 'transferir']:
                return regalar_monedas(remitente, args)    # ============ JUEGOS ============
    elif comando in ['dado', 'dice', 'roll']:
        return f"🎲 *{mencion}*\n\n{tirar_dado(remitente)}"
    elif comando in ['moneda', 'coinflip', 'cara']:
        return f"🪙 *{mencion}*\n\n{lanzar_moneda(remitente)}"
    elif comando in ['ppt', 'piedra', 'rps']:
        return f"✊ *{mencion}*\n\n{piedra_papel_tijera(remitente, args)}"
    elif comando in ['ahorcado', 'ahorcar']:
        return f"🎯 *{mencion}*\n\n{ahorcado(remitente)}"
    elif comando in ['trivia', 'quiz']:
        return f"🧠 *{mencion}*\n\n{trivia(remitente)}"
    elif comando in ['ruleta', 'rusa']:
        return f"🔫 *{mencion}*\n\n{ruleta_rusa(remitente)}"
    elif comando in ['loteria', 'loto']:
        return f"🎰 *{mencion}*\n\n{loteria(remitente)}"
    
    # ============ UTILIDADES ============
    elif comando in ['clima', 'weather']:
        return obtener_clima(args)
    elif comando in ['calc', 'calcular', 'math']:
        return calculadora(args)
    elif comando in ['password', 'pass']:
        return generar_password(args)
    elif comando in ['fecha', 'date']:
        return ver_fecha()
    elif comando in ['hora', 'time']:
        return ver_hora()
    elif comando in ['binario', 'bin']:
        return texto_binario(args)
    elif comando in ['hex', 'hexadecimal']:
        return texto_hex(args)
    elif comando in ['base64', 'b64']:
        return texto_base64(args)
    elif comando in ['md5', 'hash']:
        return texto_md5(args)
    elif comando in ['reverso', 'reverse']:
        return texto_reverso(args)
    elif comando in ['mayus', 'uppercase']:
        return texto_mayus(args)
    elif comando in ['minus', 'lowercase']:
        return texto_minus(args)
    elif comando in ['contar', 'count']:
        return contar_caracteres(args)
    elif comando in ['foto', 'perfil', 'fotoperfil']:
        return await self.ver_foto_perfil(remitente, args, mencion)
    
    # ============ DIVERSIÓN ============
    elif comando in ['dato', 'fact']:
        return dato_curioso()
    elif comando in ['chiste', 'joke']:
        return chiste()
    elif comando in ['frase', 'motivacion']:
        return frase_motivacional()
    elif comando in ['piropo', 'halago']:
        return f"💖 *Para {mencion}:*\n\n{piropo()}"
    elif comando in ['8ball', 'bola']:
        return bola_ocho(args)
    elif comando in ['amor', 'love']:
        return calcular_amor(args)
    elif comando in ['edad', 'age']:
        return calcular_edad(args)
    elif comando in ['nombre', 'randomname']:
        return generar_nombre()
    elif comando in ['color', 'randomcolor']:
        return color_aleatorio()
    elif comando in ['emoji', 'randomemoji']:
        return emoji_aleatorio()
    
    # ============ EXCLUSIVOS ============
    elif comando in ['futuro', 'predecir']:
        return f"🔮 *{mencion}*\n\n{predecir_futuro(remitente, args)}"
    elif comando in ['match', 'compatibilidad']:
        return compatibilidad_nombres(args)
    elif comando in ['test', 'personalidad']:
        return f"🧠 *{mencion}*\n\n{test_personalidad(remitente, args)}"
    elif comando in ['correo', 'email']:
        return generar_correo(args)
    elif comando in ['iguser', 'usuarioig']:
        return generar_usuario_instagram(args)
    elif comando in ['bio', 'biografia']:
        return generar_bio(args)
    elif comando in ['horoscopo', 'signo']:
        return horoscopo_diario(args)
    elif comando in ['imc', 'masacorporal']:
        return calcular_imc(args)
    elif comando in ['regla3', 'reglatres']:
        return calcular_regla_tres(args)
    elif comando in ['descuento', 'oferta']:
        return calcular_descuento(args)
    elif comando in ['cuenta', 'countdown']:
        return cuenta_regresiva(args)
    elif comando in ['edadexacta', 'exacta']:
        return edad_exacta(args)
    elif comando in ['leet', '1337']:
        return texto_leet(args)
    elif comando in ['morse', 'codigomorse']:
        return texto_morse(args)
    elif comando in ['textemoji', 'emoji_texto']:
        return texto_emoji(args)
    
    # ============ PREMIUM ============
    elif comando in ['analizar', 'texto']:
        return analizar_texto(args)
    elif comando in ['numero', 'num']:
        return analizar_numero(args)
    elif comando in ['temp', 'temperatura']:
        return convertir_temperatura(args)
    elif comando in ['distancia', 'longitud']:
        return convertir_distancia(args)
    elif comando in ['historia', 'cuento']:
        return generar_historia(args)
    elif comando in ['poema', 'poesia']:
        return generar_poema(args)
    elif comando in ['consejo', 'tip']:
        return generar_consejo(args)
    elif comando in ['palabras', 'wordgame']:
        return juego_palabras(args)
    
    # ============ ADMINISTRACIÓN ============
    elif comando in ['kick', 'expulsar']:
        return kick_usuario(remitente, args)
    elif comando in ['ban', 'banear']:
        return ban_usuario(remitente, args)
    elif comando in ['promover', 'promote']:
        return promover_usuario(remitente, args)
    elif comando in ['demover', 'demote']:
        return demover_usuario(remitente, args)
    elif comando in ['grupo', 'infogrupo']:
        return info_grupo(remitente)
    elif comando in ['bienvenida', 'welcome']:
        return configurar_bienvenida(remitente, args)
    elif comando in ['fotogrupo', 'groupphoto']:
        return await self.ver_foto_grupo(remitente, mencion)
    
    # ============ ANTI-SPAM ============
    elif comando in ['antispam', 'spam']:
        return toggle_antispam(remitente, args)
    elif comando in ['warn', 'advertir']:
        return advertir_usuario(remitente, args)
    elif comando in ['unwarn', 'quitartar']:
        return quitar_advertencia(remitente, args)
    elif comando in ['warns', 'advertencias']:
        return ver_advertencias(remitente)
    
    # ============ OWNER ============
    elif comando in ['owner', 'dueño', 'creador']:
        return info_owner(remitente)
    elif comando in ['stats', 'estadisticas']:
        return estadisticas_bot(remitente)
    elif comando in ['broadcast', 'anuncio']:
        return broadcast(remitente, args)
    elif comando in ['addowner', 'agregarowner']:
        return agregar_owner(remitente, args)
    elif comando in ['delowner', 'quitarowner']:
        return quitar_owner(remitente, args)
    elif comando in ['listowners', 'owners']:
        return listar_owners(remitente)
    elif comando in ['usuarios', 'users']:
        return listar_usuarios(remitente)
    elif comando in ['dar', 'give']:
        return dar_monedas(remitente, args)
    elif comando in ['quitar', 'remove']:
        return quitar_monedas(remitente, args)
    elif comando in ['reset', 'reiniciaruser']:
        return reset_usuario(remitente, args)
    elif comando in ['banuser', 'banearuser']:
        return banear_usuario_owner(remitente, args)
    elif comando in ['unbanuser', 'desbanear']:
        return desbanear_usuario_owner(remitente, args)
    
    # ============ DESCONOCIDO ============
    else:
        return f"❌ *{mencion}*\n\nComando no reconocido\n\nEscribe *{PREFIX}menu* para ver todos los comandos."
        
except Exception as e:
    logger.error(f"Error ejecutando comando: {e}")
    return "⚠️ *Error interno*\n\nOcurrió un error inesperado."    # ============ COMANDOS DE VINCULACIÓN ============
    
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
    
    # ============ COMANDOS DE FOTO ============
    
    async def ver_foto_perfil(self, usuario, args, mencion):
        """Ver foto de perfil"""
        try:
            if args:
                objetivo = args[0]
            else:
                objetivo = usuario
            
            try:
                foto = await self.socket.get_profile_picture(objetivo)
                if foto:
                    return f"📸 *Foto de perfil de {mencion}:*\n\n{foto}"
                else:
                    return f"❌ *{mencion} no tiene foto de perfil*"
            except:
                return f"❌ *No se pudo obtener la foto de {mencion}*"
        except Exception as e:
            logger.error(f"Error obteniendo foto: {e}")
            return "❌ *Error al obtener foto*"
    
    async def ver_foto_grupo(self, usuario, mencion):
        """Ver foto de grupo"""
        try:
            try:
                foto = await self.socket.get_group_picture(usuario)
                if foto:
                    return f"📸 *Foto del grupo:*\n\n{foto}"
                else:
                    return "❌ *El grupo no tiene foto*"
            except:
                return "❌ *No se pudo obtener la foto del grupo*"
        except Exception as e:
            logger.error(f"Error obteniendo foto de grupo: {e}")
            return "❌ *Error al obtener foto*"
    
    # ============ ANTI-SPAM ============
    
    def toggle_antispam(self, usuario, args):
        """Activar o desactivar anti-spam"""
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            estado = "activado" if self.antispam_activo else "desactivado"
            return f"🛡️ *Anti-spam está {estado}*\n\nUsa: {PREFIX}antispam on/off"
        
        opcion = args[0].lower()
        
        if opcion in ['on', 'activar', 'si']:
            self.antispam_activo = True
            return "✅ *Anti-spam activado*"
        elif opcion in ['off', 'desactivar', 'no']:
            self.antispam_activo = False
            return "❌ *Anti-spam desactivado*"
        else:
            return f"❌ *Opción inválida*\n\nUsa: {PREFIX}antispam on/off"
    
    def advertir_usuario(self, usuario, args):
        """Advertir usuario"""
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"❌ *Uso:* {PREFIX}warn [número]\n\nEjemplo: {PREFIX}warn 50512345678"
        
        objetivo = args[0]
        
        if objetivo not in self.usuarios_advertidos:
            self.usuarios_advertidos[objetivo] = 0
        
        self.usuarios_advertidos[objetivo] += 1
        
        return f"⚠️ *Advertencia enviada*\n\n👤 Usuario: {objetivo}\n📊 Total: {self.usuarios_advertidos[objetivo]}"
    
    def quitar_advertencia(self, usuario, args):
        """Quitar advertencia"""
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not args:
            return f"❌ *Uso:* {PREFIX}unwarn [número]"
        
        objetivo = args[0]
        
        if objetivo in self.usuarios_advertidos and self.usuarios_advertidos[objetivo] > 0:
            self.usuarios_advertidos[objetivo] -= 1
            return f"✅ *Advertencia quitada*\n\n👤 Usuario: {objetivo}\n📊 Restantes: {self.usuarios_advertidos[objetivo]}"
        else:
            return f"❌ *{objetivo} no tiene advertencias*"
    
    def ver_advertencias(self, usuario):
        """Ver advertencias"""
        if usuario != OWNER_NUMBER:
            return "❌ *Solo el owner puede usar este comando*"
        
        if not self.usuarios_advertidos:
            return "📊 *No hay usuarios advertidos*"
        
        mensaje = "📊 *USUARIOS ADVERTIDOS*\n\n"
        for num, cant in self.usuarios_advertidos.items():
            mensaje += f"├─ 👤 {num}: {cant} advertencias\n"
        
        return mensaje
    
    # ============ MENSAJES NORMALES ============
    
    def procesar_mensaje_normal(self, mensaje, remitente, mencion):
        """Procesar mensajes sin comando"""
        mensaje_lower = mensaje.lower()
        
        respuestas = {
            'hola': f'¡Hola {mencion}! 👋 Soy *MINI AURA*\n\nEscribe *.menu* para ver todo lo que puedo hacer.',
            'buenos días': f'¡Buenos días {mencion}! ☀️',
            'buenas tardes': f'¡Buenas tardes {mencion}! 🌤️',
            'buenas noches': f'¡Buenas noches {mencion}! 🌙',
            'como estas': f'¡Estoy genial {mencion}! 💪',
            'gracias': f'¡De nada {mencion}! 😊',
            'adios': f'¡Hasta luego {mencion}! 👋',
            'te amo': f'¡Yo también te quiero {mencion}! 💙',
            'quien te creo': f'Fui creado por un desarrollador genial 💻',
            'owner': f'Mi dueño es +{OWNER_NUMBER} 👑',
            'menu': f'{mencion}, escribe *{PREFIX}menu* para ver los comandos.',
        }
        
        for clave, respuesta in respuestas.items():
            if clave in mensaje_lower:
                return respuesta
        
        return f"{mencion}, no entendí tu mensaje 🤔\n\nEscribe *{PREFIX}menu* para ver los comandos."
# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    try:
        bot = BotMiniAura()
        asyncio.run(bot.iniciar())
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        logger.error(traceback.format_exc())