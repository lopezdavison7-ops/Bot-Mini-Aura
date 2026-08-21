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

# Importar comandos generales
from commands.general import menu as cmd_menu
from commands.general import info as cmd_info
from commands.general import ping as cmd_ping
from commands.general import owner as cmd_owner

# Importar comandos de diversión
from commands.fun import chiste as cmd_chiste
from commands.fun import dato as cmd_dato
from commands.fun import frase as cmd_frase
from commands.fun import amor as cmd_amor
from commands.fun import futuro as cmd_futuro

# Importar comandos de juegos
from commands.games import dado as cmd_dado
from commands.games import moneda as cmd_moneda
from commands.games import ppt as cmd_ppt
from commands.games import ball as cmd_ball

# Importar comandos de utilidades
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

# Importar comandos de economía
from commands.economy import balance as cmd_balance
from commands.economy import work as cmd_work
from commands.economy import rank as cmd_rank
from commands.economy import rob as cmd_rob
from commands.economy import deposit as cmd_deposit
from commands.economy import withdraw as cmd_withdraw
from commands.economy import give as cmd_give

# Importar comandos de antispam
from commands.antispam import toggle as cmd_toggle
from commands.antispam import warn as cmd_warn
from commands.antispam import unwarn as cmd_unwarn
from commands.antispam import warns as cmd_warns

# Importar comandos de admin
from commands.admin import kick as cmd_kick
from commands.admin import ban as cmd_ban
from commands.admin import promote as cmd_promote
from commands.admin import demote as cmd_demote
from commands.admin import group as cmd_group
from commands.admin import welcome as cmd_welcome

# Importar comandos de owner
from commands.owner import stats as cmd_stats
from commands.owner import broadcast as cmd_broadcast
from commands.owner import addowner as cmd_addowner
from commands.owner import delowner as cmd_delowner
from commands.owner import listowners as cmd_listowners
from commands.owner import users as cmd_users
from commands.owner import dar as cmd_dar
from commands.owner import quitar as cmd_quitar
from commands.owner import reset as cmd_reset
from commands.owner import banuser as cmd_banuser
from commands.owner import unbanuser as cmd_unbanuser

# Configuración
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
            numero_remitente = remitente.split('@')[0] if '@' in remitente else remitente
            mencion = f"@{numero_remitente}"

            if not texto:
                return

            if texto in self.mensajes_procesados:
                return
            self.mensajes_procesados.add(texto)

            logger.info(f"Mensaje de {numero_remitente}: {texto[:50]}")

            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' ' in texto else []
                respuesta = await self.ejecutar_comando(comando, args, numero_remitente, mencion)
            else:
                respuesta = self.procesar_normal(texto, mencion)

            if respuesta:
                await self.sock['sendMessage'](remitente, {'text': respuesta})

        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")

    async def ejecutar_comando(self, comando, args, usuario, mencion):
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
            
            # Economía
            elif comando in ['balance', 'bal', 'monedas']:
                return cmd_balance(mencion, usuario)
            elif comando in ['work', 'trabajar']:
                return cmd_work(mencion, usuario)
            elif comando in ['rank', 'top', 'ranking']:
                return cmd_rank(mencion, usuario)
            elif comando in ['robar', 'rob', 'steal']:
                return cmd_rob(args, mencion, usuario)
            elif comando in ['depositar', 'dep']:
                return cmd_deposit(args, mencion, usuario)
            elif comando in ['retirar', 'with']:
                return cmd_withdraw(args, mencion, usuario)
            elif comando in ['regalar', 'give', 'pay']:
                return cmd_give(args, mencion, usuario)
            
            # Antispam
            elif comando in ['antispam', 'spam']:
                return cmd_toggle(args, mencion, usuario)
            elif comando in ['warn', 'advertir']:
                return cmd_warn(args, mencion, usuario)
            elif comando in ['unwarn', 'quitarwarn']:
                return cmd_unwarn(args, mencion, usuario)
            elif comando in ['warns', 'advertencias']:
                return cmd_warns(mencion, usuario)
            
            # Admin
            elif comando in ['kick', 'expulsar']:
                return cmd_kick(args, mencion, usuario)
            elif comando in ['ban', 'banear']:
                return cmd_ban(args, mencion, usuario)
            elif comando in ['promover', 'promote']:
                return cmd_promote(args, mencion, usuario)
            elif comando in ['demover', 'demote']:
                return cmd_demote(args, mencion, usuario)
            elif comando in ['grupo', 'group']:
                return cmd_group(mencion, usuario)
            elif comando in ['bienvenida', 'welcome']:
                return cmd_welcome(args, mencion, usuario)
            
            # Owner
            elif comando in ['stats', 'estadisticas']:
                return cmd_stats(mencion, usuario)
            elif comando in ['broadcast', 'anuncio']:
                return cmd_broadcast(args, mencion, usuario)
            elif comando in ['addowner', 'agregarowner']:
                return cmd_addowner(args, mencion, usuario)
            elif comando in ['delowner', 'quitarowner']:
                return cmd_delowner(args, mencion, usuario)
            elif comando in ['listowners', 'owners']:
                return cmd_listowners(mencion, usuario)
            elif comando in ['usuarios', 'users']:
                return cmd_users(mencion, usuario)
            elif comando in ['dar', 'give']:
                return cmd_dar(args, mencion, usuario)
            elif comando in ['quitar', 'remove']:
                return cmd_quitar(args, mencion, usuario)
            elif comando in ['reset', 'reiniciaruser']:
                return cmd_reset(args, mencion, usuario)
            elif comando in ['banuser', 'banearuser']:
                return cmd_banuser(args, mencion, usuario)
            elif comando in ['unbanuser', 'desbanear']:
                return cmd_unbanuser(args, mencion, usuario)
            
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