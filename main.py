#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 BOT MINI AURA v4.0.0
Owner: +50578391933
Sistema: Selenium + WhatsApp Web
"""

import time
import json
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MINI-AURA')

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    logger.error("Instala: pip install selenium webdriver-manager")
    exit(1)

from config.settings import PREFIX, OWNER_NUMBER, VERSION

class BotMiniAura:
    def __init__(self):
        self.driver = None
        self.vinculados = self.cargar_vinculados()
        self.codigos = {}
        self.mensajes_procesados = set()
    
    def cargar_vinculados(self):
        try:
            archivo = Path('data/vinculados.json')
            if archivo.exists():
                with open(archivo, 'r') as f:
                    return set(json.load(f))
            return set()
        except:
            return set()
    
    def guardar_vinculados(self):
        try:
            archivo = Path('data/vinculados.json')
            archivo.parent.mkdir(parents=True, exist_ok=True)
            with open(archivo, 'w') as f:
                json.dump(list(self.vinculados), f, indent=2)
        except:
            pass
    
    def iniciar(self):
        try:
            logger.info("Iniciando BOT MINI AURA...")
            
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.get("https://web.whatsapp.com")
            
            print("\n" + "=" * 50)
            print("📱 ESCANEA EL QR CON TU WHATSAPP")
            print("=" * 50 + "\n")
            
            try:
                WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
                )
                print("✅ Conectado!")
            except:
                print("❌ Tiempo agotado")
                self.driver.quit()
                exit(1)
            
            print("🤖 BOT MINI AURA ACTIVO")
            print(f"👑 Owner: +{OWNER_NUMBER}")
            
            while True:
                try:
                    mensajes = self.obtener_mensajes()
                    for msg in mensajes:
                        respuesta = self.procesar(msg)
                        if respuesta:
                            self.enviar(respuesta)
                    time.sleep(2)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"Error: {e}")
                    time.sleep(5)
        except Exception as e:
            logger.error(f"Error fatal: {e}")
        finally:
            if self.driver:
                self.driver.quit()
    
    def obtener_mensajes(self):
        mensajes = []
        try:
            chats = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[contains(@class, "selectable-text")]')
            for chat in chats[-5:]:
                texto = chat.text.strip()
                if texto and texto not in self.mensajes_procesados:
                    self.mensajes_procesados.add(texto)
                    mensajes.append(texto)
        except:
            pass
        return mensajes
    
    def enviar(self, texto):
        try:
            caja = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
            caja.click()
            caja.send_keys(texto)
            time.sleep(0.5)
            caja.send_keys(Keys.ENTER)
            return True
        except:
            return False
    
    def procesar(self, texto):
        try:
            if not texto.startswith(PREFIX):
                return self.procesar_normal(texto)
            
            comando = texto[len(PREFIX):].split(' ')[0].lower()
            args = texto.split(' ')[1:] if ' ' in texto else []
            
            if comando in ['vincular', 'link']:
                return self.cmd_vincular(args)
            elif comando in ['codigo', 'code']:
                return self.cmd_codigo()
            elif comando in ['verificar', 'verify']:
                return self.cmd_verificar(args)
            elif comando in ['estado', 'status']:
                return self.cmd_estado()
            
            if comando in ['menu', 'ayuda', 'help', 'start']:
                return self.menu_principal()
            elif comando in ['ping', 'test']:
                return "🏓 *Pong!* Bot activo"
            elif comando in ['info', 'bot']:
                return f"🤖 *BOT MINI AURA*\nVersión: {VERSION}\nOwner: +{OWNER_NUMBER}"
            elif comando in ['owner', 'dueño']:
                return f"👑 Owner: +{OWNER_NUMBER}\n🇳🇮 Nicaragua"
            elif comando in ['dado', 'dice', 'roll']:
                return f"🎲 Sacaste: {random.randint(1, 6)}"
            elif comando in ['moneda', 'coin']:
                return f"🪙 Resultado: {random.choice(['Cara', 'Cruz'])}"
            elif comando in ['dato', 'fact']:
                return random.choice(["🐙 Pulpos tienen 3 corazones", "🍯 La miel nunca caduca", "🦩 Flamencos son rosados por su comida"])
            elif comando in ['chiste', 'joke']:
                return random.choice(["😂 ¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter", "😂 ¿Qué le dice un semáforo a otro? No me mires, me estoy cambiando"])
            elif comando in ['frase', 'motivacion']:
                return random.choice(["🌟 El éxito es la suma de pequeños esfuerzos", "💪 Cree en ti y todo será posible"])
            elif comando in ['fecha', 'date']:
                return f"📅 {datetime.now().strftime('%d/%m/%Y')}"
            elif comando in ['hora', 'time']:
                return f"⏰ {datetime.now().strftime('%H:%M:%S')}"
            elif comando in ['calc', 'math']:
                try:
                    return f"🧮 Resultado: {eval(' '.join(args))}"
                except:
                    return "❌ Error en operación"
            elif comando in ['password', 'pass']:
                import string
                chars = string.ascii_letters + string.digits
                return f"🔑 `{''.join(random.choice(chars) for _ in range(12))}`"
            elif comando in ['reverso', 'reverse']:
                if args:
                    return f"🔄 {' '.join(args)[::-1]}"
                return "❌ Uso: .reverso texto"
            elif comando in ['amor', 'love']:
                if len(args) >= 2:
                    return f"💑 {args[0]} + {args[1]} = {random.randint(50, 100)}%"
                return "❌ Uso: .amor nombre1 nombre2"
            elif comando in ['8ball', 'bola']:
                return random.choice(["Sí ✅", "No ❌", "Quizás 🤔"])
            elif comando in ['futuro', 'predecir']:
                return random.choice(["🔮 Veo éxito", "🌟 Algo bueno viene", "💫 Sorpresa cerca"])
            else:
                return "❌ Comando no reconocido\n\nEscribe .menu"
        except Exception as e:
            logger.error(f"Error procesando: {e}")
            return "⚠️ Error interno"
    
    def procesar_normal(self, texto):
        t = texto.lower()
        if 'hola' in t:
            return "👋 ¡Hola! Soy MINI AURA\n\nEscribe .menu"
        elif 'gracias' in t:
            return "😊 ¡De nada!"
        elif 'adios' in t:
            return "👋 ¡Hasta luego!"
        elif 'como estas' in t:
            return "💪 ¡Estoy genial!"
        return "No entendí 🤔\n\nEscribe .menu"
    
    def cmd_vincular(self, args):
        if not args:
            return "📱 Escribe: .vincular 50578391933"
        return "✅ Número guardado\n\nAhora escribe: .codigo"
    
    def cmd_codigo(self):
        codigo = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        self.codigos['usuario'] = codigo
        return f"🔢 *Código:* {codigo[0:4]} {codigo[4:8]}\n\nVerifica: .verificar {codigo}"
    
    def cmd_verificar(self, args):
        if not args:
            return "❌ Uso: .verificar codigo"
        codigo = args[0].replace(' ', '')
        if self.codigos.get('usuario') == codigo:
            self.vinculados.add(OWNER_NUMBER)
            self.guardar_vinculados()
            return "✅ *¡Vinculación exitosa!*\n\nEscribe .menu"
        return "❌ Código incorrecto"
    
    def cmd_estado(self):
        if self.vinculados:
            return "✅ Estás vinculado"
        return "❌ No estás vinculado\n\n.vincular 50578391933"
    
    def menu_principal(self):
        return """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🤖 *BOT MINI AURA* 🤖   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

⚡ *GENERALES*
├─ .menu - Menú
├─ .info - Info
├─ .ping - Latencia
└─ .owner - Dueño

🎮 *JUEGOS*
├─ .dado - Dado
├─ .moneda - Moneda
└─ .8ball - Bola mágica

🛠️ *UTILIDADES*
├─ .calc - Calculadora
├─ .fecha - Fecha
├─ .hora - Hora
├─ .password - Contraseña
└─ .reverso - Invertir

🎭 *DIVERSIÓN*
├─ .dato - Dato curioso
├─ .chiste - Chiste
├─ .frase - Motivación
├─ .amor - Compatibilidad
└─ .futuro - Predecir
        """

if __name__ == '__main__':
    bot = BotMiniAura()
    bot.iniciar()