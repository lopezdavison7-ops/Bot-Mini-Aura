import asyncio
import json
import base64
import os
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MINI-AURA')

from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds
from WAeys.Utils.browser_utils import Browsers
from WAeys.Socket.socket import make_socket

# Importar comandos
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
from commands.economy import balance as cmd_balance
from commands.economy import work as cmd_work
from commands.economy import rank as cmd_rank
from commands.economy import rob as cmd_rob
from commands.economy import deposit as cmd_deposit
from commands.economy import withdraw as cmd_withdraw
from commands.economy import give as cmd_give
from commands.antispam import toggle as cmd_toggle
from commands.antispam import warn as cmd_warn
from commands.antispam import unwarn as cmd_unwarn
from commands.antispam import warns as cmd_warns
from commands.admin import kick as cmd_kick
from commands.admin import ban as cmd_ban
from commands.admin import promote as cmd_promote
from commands.admin import demote as cmd_demote
from commands.admin import group as cmd_group
from commands.admin import welcome as cmd_welcome
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

# Persistencia de sesión
SESSION_DIR = os.path.join(os.getcwd(), 'wa_session')
CREDS_FILE = os.path.join(SESSION_DIR, 'creds.json')
KEYS_FILE = os.path.join(SESSION_DIR, 'keys.json')

def _encode(v):
    if isinstance(v, bytes):
        return {'__bytes__': base64.b64encode(v).decode('ascii')}
    if isinstance(v, str):
        return {'__str__': v}
    if isinstance(v, dict):
        return {k: _encode(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_encode(x) for x in v]
    return v

def _decode(v):
    if isinstance(v, dict):
        if '__bytes__' in v:
            return base64.b64decode(v['__bytes__'])
        if '__str__' in v:
            return v['__str__']
        return {k: _decode(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_decode(x) for x in v]
    return v

def save_creds(creds):
    os.makedirs(SESSION_DIR, exist_ok=True)
    with open(CREDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(_encode(creds), f, default=str, ensure_ascii=False, indent=2)

def load_creds():
    if not os.path.exists(CREDS_FILE):
        return None
    with open(CREDS_FILE, 'r', encoding='utf-8') as f:
        return _decode(json.load(f))

def make_file_key_store():
    async def get(type_, ids):
        all_keys = {}
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, 'r', encoding='utf-8') as f:
                all_keys = _decode(json.load(f))
        return {i: all_keys.get(type_, {}).get(i) for i in ids if all_keys.get(type_, {}).get(i) is not None}

    async def set(data):
        existing = {}
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, 'r', encoding='utf-8') as f:
                existing = _decode(json.load(f))
        for type_, entries in data.items():
            for id_, value in entries.items():
                existing.setdefault(type_, {})
                if value is None:
                    existing[type_].pop(id_, None)
                else:
                    existing[type_][id_] = value
        os.makedirs(SESSION_DIR, exist_ok=True)
        with open(KEYS_FILE, 'w', encoding='utf-8') as f:
            json.dump(_encode(existing), f, default=str, ensure_ascii=False, indent=2)

    async def clear():
        if os.path.exists(KEYS_FILE):
            os.remove(KEYS_FILE)

    return {'get': get, 'set': set, 'clear': clear}


class BotMiniAura:
    def __init__(self):
        self.sock = None
        self.mensajes_procesados = set()
        self.auth = None

    async def pair(self):
        """Emparejamiento con código de 8 dígitos"""
        config = default_connection_config()
        config['auth'] = self.auth
        config['browser'] = Browsers.macOS('Safari')
        config['keepAliveIntervalMs'] = 5000
        config['logger'].level = 'info'

        self.sock = make_socket(config)
        ev = self.sock['ev']
        done = asyncio.Event()

        async def on_creds(update):
            self.auth['creds'].update(update)
            save_creds(self.auth['creds'])

        ev.on('creds.update', lambda u: asyncio.ensure_future(on_creds(u)))

        async def on_conn(update):
            if update.get('qr') and not self.sock.get('_code_requested'):
                self.sock['_code_requested'] = True
                try:
                    code = await self.sock['requestPairingCode'](NUMERO_VINCULAR)
                    print(f'\n🔢 CÓDIGO DE EMPAREJAMIENTO: {code}\n')
                except Exception as err:
                    print(f'❌ Error: {err}')
            if update.get('connection') == 'open':
                print('\n✅ ¡EMPAREJADO Y CONECTADO!')
                done.set()

        ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))

        try:
            await asyncio.wait_for(done.wait(), timeout=120)
        except asyncio.TimeoutError:
            print('⏰ Tiempo agotado')
        finally:
            await self.sock['end']()
        return done.is_set()

    async def iniciar(self):
        """Iniciar bot con reintentos"""
        self.auth = {'creds': init_auth_creds(), 'keys': make_file_key_store()}
        
        # Cargar sesión existente si hay
        creds = load_creds()
        if creds is not None:
            self.auth = {'creds': creds, 'keys': make_file_key_store()}
        
        attempt = 1
        while True:
            print(f'--- Intento {attempt} ---')
            ok = await self.pair()
            if ok:
                print('✅ Sesión guardada.')
                break
            attempt += 1
            await asyncio.sleep(3)
            self.auth['creds'] = init_auth_creds()
            save_creds(self.auth['creds'])
        
        # Después de conectar, ejecutar bot
        await self.ejecutar_bot()

    async def ejecutar_bot(self):
        """Ejecutar el bot después de conectar"""
        config = default_connection_config()
        creds = load_creds()
        config['auth'] = {'creds': creds, 'keys': make_file_key_store()}
        config['browser'] = Browsers.macOS('Safari')
        config['keepAliveIntervalMs'] = 30000
        config['logger'].level = 'info'

        self.sock = make_socket(config)
        ev = self.sock['ev']

        async def on_message(message):
            await self.procesar_mensaje(message)

        ev.on('messages.upsert', lambda m: asyncio.ensure_future(on_message(m)))

        print('\n🤖 BOT MINI AURA ACTIVO')
        print(f'👑 Owner: +{OWNER_NUMBER}')
        
        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass

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

            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' ' in texto else []
                respuesta = await self.ejecutar_comando(comando, args, numero_remitente, mencion)
            else:
                respuesta = self.procesar_normal(texto, mencion)

            if respuesta:
                await self.sock['sendMessage'](remitente, {'text': respuesta})

        except Exception as e:
            logger.error(f"Error: {e}")

    async def ejecutar_comando(self, comando, args, usuario, mencion):
        try:
            if comando in ['menu', 'help', 'comandos']:
                return cmd_menu(mencion)
            elif comando in ['info', 'bot']:
                return cmd_info(mencion)
            elif comando in ['ping', 'test']:
                return cmd_ping(mencion)
            elif comando in ['owner', 'dueño']:
                return cmd_owner(mencion)
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
            elif comando in ['dado', 'dice', 'roll']:
                return cmd_dado(mencion)
            elif comando in ['moneda', 'coin', 'cara']:
                return cmd_moneda(mencion)
            elif comando in ['ppt', 'piedra']:
                return cmd_ppt(args, mencion)
            elif comando in ['8ball', 'bola']:
                return cmd_ball(args, mencion)
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
            elif comando in ['antispam', 'spam']:
                return cmd_toggle(args, mencion, usuario)
            elif comando in ['warn', 'advertir']:
                return cmd_warn(args, mencion, usuario)
            elif comando in ['unwarn', 'quitarwarn']:
                return cmd_unwarn(args, mencion, usuario)
            elif comando in ['warns', 'advertencias']:
                return cmd_warns(mencion, usuario)
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
            logger.error(f"Error: {e}")
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
    try:
        asyncio.run(bot.iniciar())
    except KeyboardInterrupt:
        print("\n👋 Bot detenido")
    except Exception as e:
        logger.error(f"Error fatal: {e}")