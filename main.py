#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 BOT MINI AURA - Bot Multi-propósito para WhatsApp
Versión: 3.0.0
Owner: +50578391933
Sistema: Selenium + WhatsApp Web
Total de comandos: 101
"""

import os
import sys
import json
import time
import random
import logging
import threading
import traceback
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

# Importar Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import *
except ImportError:
    logger.error("Selenium no instalado. Ejecuta: pip install selenium")
    sys.exit(1)

# Importar configuraciones
sys.path.insert(0, str(Path(__file__).parent))
from config.settings import *
from src.lib.database import Database
from src.lib.vincular import SistemaVinculacion

# ==================== CLASE PRINCIPAL DEL BOT ====================

class BotMiniAura:
    def __init__(self):
        self.driver = None
        self.db = Database()
        self.db.initialize()
        self.sistema_vinculacion = SistemaVinculacion()
        self.vinculados = set()
        self.codigos_pendientes = {}
        self.mensajes_procesados = set()
        self.ultimo_mensaje = {}
        
    def iniciar_driver(self):
        """Inicializar el driver de Chrome"""
        try:
            logger.info("🚀 Iniciando Chrome...")
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--user-data-dir=src/sessions/chrome")
            
            # Si quieres ver el navegador, comenta esta línea
            # chrome_options.add_argument("--headless")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get("https://web.whatsapp.com")
            
            logger.info("📱 Abriendo WhatsApp Web...")
            print("\n" + "=" * 60)
            print("📱 *ESCANEA EL CÓDIGO QR CON TU WHATSAPP*")
            print("=" * 60 + "\n")
            
            # Esperar a que el usuario escanee el QR
            self.esperar_qr()
            
            logger.info("✅ ¡WhatsApp Web conectado!")
            
        except Exception as e:
            logger.error(f"Error iniciando driver: {e}")
            sys.exit(1)
    
    def esperar_qr(self, timeout=120):
        """Esperar a que el usuario escanee el QR"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
            )
            logger.info("✅ QR escaneado correctamente")
        except TimeoutException:
            logger.error("⏰ Tiempo de espera agotado para escanear QR")
            self.driver.quit()
            sys.exit(1)
    
    def esperar_elemento(self, xpath, timeout=10):
        """Esperar a que aparezca un elemento"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            return None
    
    def obtener_mensajes(self):
        """Obtener mensajes nuevos de WhatsApp"""
        mensajes = []
        try:
            # Buscar mensajes no leídos
            chats_no_leidos = self.driver.find_elements(By.XPATH, 
                '//div[contains(@class, "message-in")]//span[contains(@class, "selectable-text")]')
            
            for chat in chats_no_leidos[-5:]:  # Últimos 5 mensajes
                try:
                    texto = chat.text.strip()
                    if texto and texto not in self.mensajes_procesados:
                        self.mensajes_procesados.add(texto)
                        mensajes.append(texto)
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Error obteniendo mensajes: {e}")
        
        return mensajes
    
    def enviar_mensaje(self, numero, mensaje):
        """Enviar mensaje a un número específico"""
        try:
            # Formatear número
            numero = numero.replace("+", "").replace(" ", "")
            
            # Abrir chat con el número
            self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&text={mensaje}")
            
            # Esperar a que cargue
            time.sleep(3)
            
            # Encontrar botón de enviar y hacer click
            boton_enviar = self.esperar_elemento('//button[@data-tab="11"]', 10)
            if boton_enviar:
                boton_enviar.click()
                logger.info(f"✅ Mensaje enviado a {numero}")
                return True
            else:
                # Intentar con Enter
                caja_mensaje = self.esperar_elemento('//div[@contenteditable="true"]', 10)
                if caja_mensaje:
                    caja_mensaje.send_keys(Keys.ENTER)
                    logger.info(f"✅ Mensaje enviado a {numero}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")
            return False
    
    def responder_mensaje(self, texto, remitente="desconocido"):
        """Procesar y responder mensajes"""
        try:
            # Verificar si es comando
            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' ' in texto else []
                
                logger.info(f"Comando recibido: {comando} de {remitente}")
                
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
                
                # ============ COMANDOS DE ECONOMÍA ============
                elif comando in ['monedas', 'balance', 'bal', 'wallet', 'dinero']:
                    from src.commands.economia import ver_balance
                    return ver_balance(remitente)
                
                elif comando in ['trabajar', 'work', 'minar', 'chambear']:
                    from src.commands.economia import trabajar
                    return trabajar(remitente)
                
                elif comando in ['top', 'ranking', 'leaderboard', 'top10']:
                    from src.commands.economia import ver_ranking
                    return ver_ranking()
                
                elif comando in ['robar', 'steal', 'hurtar']:
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
                    return regalar_monedas(remitente, args)
                
                # ============ COMANDOS DE JUEGOS ============
                elif comando in ['dado', 'dice', 'roll', 'tirar']:
                    from src.commands.juegos import tirar_dado
                    return tirar_dado(remitente)
                
                elif comando in ['moneda', 'coinflip', 'cara', 'volado']:
                    from src.commands.juegos import lanzar_moneda
                    return lanzar_moneda(remitente)
                
                elif comando in ['ppt', 'piedra', 'rps', 'juego']:
                    from src.commands.juegos import piedra_papel_tijera
                    return piedra_papel_tijera(remitente, args)
                
                elif comando in ['ahorcado', 'ahorcar']:
                    from src.commands.juegos import ahorcado
                    return ahorcado(remitente)
                
                elif comando in ['trivia', 'pregunta', 'quiz']:
                    from src.commands.juegos import trivia
                    return trivia(remitente)
                
                elif comando in ['ruleta', 'rusa']:
                    from src.commands.juegos import ruleta_rusa
                    return ruleta_rusa(remitente)
                
                elif comando in ['loteria', 'loto']:
                    from src.commands.juegos import loteria
                    return loteria(remitente)
                
                # ============ COMANDOS DE UTILIDADES ============
                elif comando in ['clima', 'weather', 'tiempo']:
                    from src.commands.utilidades import obtener_clima
                    return obtener_clima(args)
                
                elif comando in ['calc', 'calcular', 'math', 'matematica']:
                    from src.commands.utilidades import calculadora
                    return calculadora(args)
                
                elif comando in ['password', 'contraseña', 'clave', 'pass']:
                    from src.commands.utilidades import generar_password
                    return generar_password(args)
                
                elif comando in ['fecha', 'date', 'hoy']:
                    from src.commands.utilidades import ver_fecha
                    return ver_fecha()
                
                elif comando in ['hora', 'time', 'reloj']:
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
                
                elif comando in ['reverso', 'reverse', 'invertir']:
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
                
                # ============ COMANDOS DE DIVERSIÓN ============
                elif comando in ['dato', 'fact', 'curiosidad']:
                    from src.commands.diversion import dato_curioso
                    return dato_curioso()
                
                elif comando in ['chiste', 'joke', 'broma']:
                    from src.commands.diversion import chiste
                    return chiste()
                
                elif comando in ['frase', 'quote', 'motivacion']:
                    from src.commands.diversion import frase_motivacional
                    return frase_motivacional()
                
                elif comando in ['piropo', 'halago']:
                    from src.commands.diversion import piropo
                    return piropo()
                
                elif comando in ['8ball', 'bola', 'pregunta8']:
                    from src.commands.diversion import bola_ocho
                    return bola_ocho(args)
                
                elif comando in ['amor', 'love', 'ship']:
                    from src.commands.diversion import calcular_amor
                    return calcular_amor(args)
                
                elif comando in ['edad', 'age', 'años']:
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
                
                # ============ COMANDOS EXCLUSIVOS ============
                elif comando in ['futuro', 'predecir', 'destino']:
                    from src.commands.exclusivos import predecir_futuro
                    return predecir_futuro(remitente, args)
                
                elif comando in ['match', 'compatibilidad']:
                    from src.commands.exclusivos import compatibilidad_nombres
                    return compatibilidad_nombres(args)
                
                elif comando in ['test', 'personalidad']:
                    from src.commands.exclusivos import test_personalidad
                    return test_personalidad(remitente, args)
                
                elif comando in ['correo', 'email', 'mail']:
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
                    return texto_emoji(args)
                
                # ============ COMANDOS PREMIUM ============
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
                
                # ============ COMANDO DESCONOCIDO ============
                else:
                    return f"❌ *Comando no reconocido*\n\nEscribe *{PREFIX}menu* para ver todos los comandos."
            
            # Respuestas automáticas
            return self.procesar_mensaje_normal(texto, remitente)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            logger.error(traceback.format_exc())
            return "⚠️ *Error interno*\n\nOcurrió un error inesperado."
    
    # ==================== COMANDOS DE VINCULACIÓN ====================
    
    def comando_vincular(self, usuario, args):
        """Comando para vincular número"""
        try:
            if usuario in self.vinculados:
                return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ✅ *YA ESTÁS VINCULADO* ✅   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Tu número:* {usuario}
🔗 *Estado:* Vinculado

Escribe {PREFIX}menu para comenzar
                """
            
            if not args:
                return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔗 *VINCULACIÓN DE BOT* 🔗  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Para vincular tu número:*

Escribe: {PREFIX}vincular [tu_número]
Ejemplo: {PREFIX}vincular 50578391933

Después escribe: {PREFIX}codigo
Para recibir tu código de 8 dígitos
                """
            
            numero = args[0]
            
            # Guardar número pendiente
            self.sistema_vinculacion.guardar_numero_pendiente(usuario, numero)
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔗 *VINCULACIÓN INICIADA* 🔗  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Número a vincular:* {numero}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 *Siguiente paso:*
Escribe: {PREFIX}codigo

Para recibir tu código de 8 dígitos
            """
        except Exception as e:
            return f"❌ *Error:* {e}"
    
    def comando_codigo(self, usuario):
        """Generar código de 8 dígitos"""
        try:
            # Generar código
            codigo = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            
            # Guardar código
            self.sistema_vinculacion.generar_codigo(usuario, codigo)
            
            logger.info(f"Código para {usuario}: {codigo}")
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🔢 *CÓDIGO DE VINCULACIÓN* 🔢   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Tu código es:*

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
            return f"❌ *Error:* {e}"
    
    def comando_verificar(self, usuario, args):
        """Verificar código de vinculación"""
        try:
            if not args:
                return f"❌ *Uso:* {PREFIX}verificar [código]"
            
            codigo_ingresado = args[0].replace(' ', '')
            
            # Verificar código
            resultado = self.sistema_vinculacion.verificar_codigo(usuario, codigo_ingresado)
            
            if resultado['valido']:
                self.vinculados.add(usuario)
                return resultado['mensaje']
            else:
                return resultado['mensaje']
                
        except Exception as e:
            return f"❌ *Error:* {e}"
    
    def comando_estado(self, usuario):
        """Ver estado de vinculación"""
        if usuario in self.vinculados:
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ✅ *YA ESTÁS VINCULADO* ✅   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📱 *Número:* {usuario}

Escribe {PREFIX}menu para comenzar
            """
        else:
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ❌ *NO ESTÁS VINCULADO* ❌   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

Escribe: {PREFIX}vincular [tu_número]
            """
    
    def comando_desvincular(self, usuario):
        """Desvincular número"""
        if usuario in self.vinculados:
            self.vinculados.remove(usuario)
            return "✅ *Has sido desvinculado*"
        return "❌ *No estabas vinculado*"
    
    def procesar_mensaje_normal(self, mensaje, remitente):
        """Procesar mensajes sin comando"""
        mensaje_lower = mensaje.lower()
        
        respuestas_auto = {
            'hola': '¡Hola! 👋 ¿Cómo estás? Soy *MINI AURA*\n\nEscribe *.menu* para ver todo lo que puedo hacer.',
            'buenos días': '¡Buenos días! ☀️',
            'buenas tardes': '¡Buenas tardes! 🌤️',
            'buenas noches': '¡Buenas noches! 🌙',
            'como estas': '¡Estoy genial! 💪',
            'gracias': '¡De nada! 😊',
            'adios': '¡Hasta luego! 👋',
        }
        
        for clave, respuesta in respuestas_auto.items():
            if clave in mensaje_lower:
                return respuesta
        
        return f"No entendí tu mensaje 🤔\n\nEscribe *{PREFIX}menu* para ver los comandos."
    
    def ejecutar(self):
        """Ejecutar el bot"""
        try:
            self.iniciar_driver()
            logger.info("🤖 BOT MINI AURA iniciado correctamente")
            logger.info(f"👑 Owner: +{OWNER_NUMBER}")
            
            print("\n" + "=" * 60)
            print("🤖 *BOT MINI AURA - ACTIVO*")
            print(f"👑 Owner: +{OWNER_NUMBER}")
            print("📊 Total comandos: 101")
            print("=" * 60 + "\n")
            
            while True:
                try:
                    # Obtener mensajes nuevos
                    mensajes = self.obtener_mensajes()
                    
                    for mensaje in mensajes:
                        # Procesar y responder
                        respuesta = self.responder_mensaje(mensaje)
                        
                        if respuesta:
                            # Enviar respuesta al chat actual
                            self.enviar_respuesta_chat(respuesta)
                    
                    time.sleep(2)  # Esperar 2 segundos
                    
                except KeyboardInterrupt:
                    logger.info("Bot detenido por el usuario")
                    break
                except Exception as e:
                    logger.error(f"Error en bucle principal: {e}")
                    time.sleep(5)
                    
        except Exception as e:
            logger.error(f"Error fatal: {e}")
            logger.error(traceback.format_exc())
        finally:
            if self.driver:
                self.driver.quit()
    
    def enviar_respuesta_chat(self, mensaje):
        """Enviar respuesta al chat actual"""
        try:
            # Encontrar caja de mensaje
            caja_mensaje = self.esperar_elemento('//div[@contenteditable="true"]', 5)
            
            if caja_mensaje:
                # Escribir mensaje
                caja_mensaje.click()
                caja_mensaje.send_keys(mensaje)
                time.sleep(0.5)
                
                # Enviar con Enter
                caja_mensaje.send_keys(Keys.ENTER)
                logger.info("✅ Respuesta enviada")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error enviando respuesta: {e}")
            return False


# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    bot = BotMiniAura()
    bot.ejecutar()