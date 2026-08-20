import asyncio
import random
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MINI-AURA')

# Importar WAeys
from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds, make_memory_key_store
from WAeys.Utils.browser_utils import Browsers
from WAeys.Socket.socket import make_socket

# Importar comandos desde las carpetas
from commands.general import menu as cmd_menu
from commands.general import info as cmd_info
from commands.general import ping as cmd_ping
from commands.general import owner as cmd_owner

from commands.fun import chiste as cmd_chiste
from commands.fun import dato as cmd_dato
from commands.fun import frase as cmd_frase
from commands.fun import amor as cmd_amor
from commands.fun import futuro as cmd_futuro

from commands.games import dado as cmd_dado
from commands.games import moneda as cmd_moneda
from commands.games import ppt as cmd_ppt
from commands.games import ball as cmd_ball

from commands.utils import calc as cmd_calc
from commands.utils import fecha as cmd_fecha
from commands.utils import hora as cmd_hora
from commands.utils import password as cmd_password
from commands.utils import reverso as cmd_reverso
from commands.utils import mayus as cmd_mayus
from commands.utils import minus as cmd_minus
from commands.utils import contar as cmd_contar
from commands.utils import morse as cmd_morse
from commands.utils import leet as cmd_leet

PREFIX = "."
NUMERO_VINCULAR = "50576641902"
OWNER_NUMBER = "50578391933"
VERSION = "4.0.0"

class BotMiniAura:
    def __init__(self):
        self.sock = None
        self.mensajes_procesados = set()

    async def iniciar(self):
        config = default_connection_config()
        config['auth'] = {'creds': init_auth_creds(), 'keys': make_memory_key_store()}
        config['browser'] = Browsers.macOS('Safari')
        config['keepAliveIntervalMs'] = 5000
        config['logger'].level = 'info'

        self.sock = make_socket(config)
        ev = self.sock['ev']

        async def on_conn(update):
            if update.get('qr') and not self.sock.get('_code_requested'):
                self.sock['_code_requested'] = True
                try:
                    codigo = await self.sock['requestPairingCode'](NUMERO_VINCULAR)
                    print("\n" + "=" * 50)
                    print("🤖 BOT MINI AURA")
                    print("=" * 50)
                    print(f"\n📱 Número a vincular: +{NUMERO_VINCULAR}")
                    print(f"\n🔢 CÓDIGO DE EMPAREJAMIENTO:")
                    print(f"\n*{codigo}*")
                    print("\n📱 Para vincular:")
                    print("Abre WhatsApp")
                    print("→ Ajustes → Dispositivos vinculados")
                    print("→ Vincular con número de teléfono")
                    print(f"→ Ingresa el código: {codigo}")
                    print("=" * 50 + "\n")
                except Exception as e:
                    print(f"❌ Error al solicitar código: {e}")
                    
            if update.get('connection') == 'open':
                print("\n" + "=" * 50)
                print("✅ ¡BOT MINI AURA CONECTADO!")
                print(f"📱 Número vinculado: +{NUMERO_VINCULAR}")
                print(f"👑 Owner: +{OWNER_NUMBER}")
                print("=" * 50 + "\n")

        async def on_message(message):
            await self.procesar_mensaje(message)

        ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))
        ev.on('messages.upsert', lambda m: asyncio.ensure_future(on_message(m)))

        print("\n🤖 Iniciando BOT MINI AURA...")
        print("Solicitando código de emparejamiento...\n")

        await asyncio.Event().wait()

    async def procesar_mensaje(self, message):
        try:
            texto = message.get('text', '').strip()
            remitente = message.get('from', 'desconocido')
            mencion = f"@{remitente.split('@')[0]}"

            if not texto:
                return

            if texto in self.mensajes_procesados:
                return
            self.mensajes_procesados.add(texto)

            logger.info(f"Mensaje de {remitente}: {texto[:50]}")

            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' ' in texto else []
                respuesta = await self.ejecutar_comando(comando, args, remitente, mencion)
            else:
                respuesta = self.procesar_normal(texto, mencion)

            if respuesta:
                await self.sock['sendMessage'](remitente, {'text': respuesta})

        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")

    async def ejecutar_comando(self, comando, args, remitente, mencion):
        try:
            # Generales
            if comando in ['menu', 'help', 'comandos']:
                return cmd_menu(mencion)
            elif comando in ['info', 'bot']:
                return cmd_info(mencion)
            elif comando in ['ping', 'test']:
                return cmd_ping(mencion)
            elif comando in ['owner', 'dueño']:
                return cmd_owner(mencion)
            
            # Diversión
            elif comando in ['dato', 'fact']:
                return cmd_dato(mencion)
            elif comando in ['chiste', 'joke']:
                return cmd_chiste(mencion)
            elif comando in ['frase', 'motivacion']:
                return cmd_frase(mencion)
            elif comando in ['amor', 'love']:
                return cmd_amor(args, mencion)
            elif comando in ['futuro', 'predecir']:
                return cmd_futuro(mencion)
            
            # Juegos
            elif comando in ['dado', 'dice', 'roll']:
                return cmd_dado(mencion)
            elif comando in ['moneda', 'coin', 'cara']:
                return cmd_moneda(mencion)
            elif comando in ['ppt', 'piedra']:
                return cmd_ppt(args, mencion)
            elif comando in ['8ball', 'bola']:
                return cmd_ball(args, mencion)
            
            # Utilidades
            elif comando in ['calc', 'calcular', 'math']:
                return cmd_calc(args, mencion)
            elif comando in ['fecha', 'date']:
                return cmd_fecha(mencion)
            elif comando in ['hora', 'time']:
                return cmd_hora(mencion)
            elif comando in ['password', 'pass']:
                return cmd_password(args, mencion)
            elif comando in ['reverso', 'reverse']:
                return cmd_reverso(args, mencion)
            elif comando in ['mayus', 'upper']:
                return cmd_mayus(args, mencion)
            elif comando in ['minus', 'lower']:
                return cmd_minus(args, mencion)
            elif comando in ['contar', 'count']:
                return cmd_contar(args, mencion)
            elif comando in ['morse', 'codigomorse']:
                return cmd_morse(args, mencion)
            elif comando in ['leet', '1337']:
                return cmd_leet(args, mencion)
            
            else:
                return f"❌ *{mencion}*\n\nComando no reconocido\n\nEscribe .menu"
                
        except Exception as e:
            logger.error(f"Error ejecutando comando: {e}")
            return "⚠️ Error interno"

    def procesar_normal(self, texto, mencion):
        t = texto.lower()
        respuestas = {
            'hola': f'👋 ¡Hola {mencion}! Soy *MINI AURA*\n\nEscribe .menu',
            'gracias': f'😊 ¡De nada {mencion}!',
            'adios': f'👋 ¡Hasta luego {mencion}!',
            'como estas': f'💪 ¡Estoy genial {mencion}!',
            'te amo': f'💙 ¡Yo también te quiero {mencion}!',
            'owner': f'👑 Mi dueño es +{OWNER_NUMBER}',
        }
        for clave, respuesta in respuestas.items():
            if clave in t:
                return respuesta
        return f"{mencion}, no entendí 🤔\n\nEscribe .menu"


if __name__ == '__main__':
    bot = BotMiniAura()
    asyncio.run(bot.iniciar())