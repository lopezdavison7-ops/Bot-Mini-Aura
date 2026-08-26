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

# Importar comandos - IGUAL QUE EL TUYO
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

PREFIX = "."
NUMERO_VINCULAR = "50576641902"
OWNER_NUMBER = "50578391933"
VERSION = "4.0.0"

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

    async def iniciar(self):
        creds = load_creds()
        if creds is not None:
            self.auth = {'creds': creds, 'keys': make_file_key_store()}
        else:
            self.auth = {'creds': init_auth_creds(), 'keys': make_file_key_store()}

        config = default_connection_config()
        config['auth'] = self.auth
        config['browser'] = Browsers.windows('Chrome') # CAMBIO 1
        config['keepAliveIntervalMs'] = 5000 # CAMBIO 2
        config['markOnlineOnConnect'] = False # CAMBIO 3
        config['logger'].level = 'info'

        self.sock = make_socket(config)
        ev = self.sock['ev']
        emparejado = asyncio.Event()

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
                emparejado.set()
                print('\n🤖 BOT MINI AURA ACTIVO')
                print(f'👑 Owner: +{OWNER_NUMBER}')

        ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))
        ev.on('messages.upsert', lambda m: asyncio.ensure_future(self.procesar_mensaje(m)))

        try:
            await asyncio.wait_for(emparejado.wait(), timeout=120)
        except asyncio.TimeoutError:
            print('⏰ Tiempo agotado para emparejar')

        await asyncio.Event().wait()

    async def procesar_mensaje(self, message):
        try:
            msgs = message.get('messages', [])
            if not msgs: return
            msg = msgs[0]
            texto = msg.get('message', {}).get('conversation', '').strip()
            if not texto:
                texto = msg.get('message', {}).get('extendedTextMessage', {}).get('text', '').strip()

            remitente = msg.get('key', {}).get('remoteJid', 'desconocido')
            numero_remitente = remitente.split('@')[0] if '@' in remitente else remitente
            mencion = f"@{numero_remitente}"

            if not texto: return
            if texto in self.mensajes_procesados: return
            self.mensajes_procesados.add(texto)

            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' in texto else []
                respuesta = await self.ejecutar_comando(comando, args, numero_remitente, mencion)
            else:
                respuesta = self.procesar_normal(texto, mencion)

            if respuesta:
                await self.sock['sendMessage'](remitente, {'text': respuesta})

        except Exception as e:
            logger.error(f"Error: {e}")

    async def ejecutar_comando(self, comando, args, usuario, mencion):
        # TODO TU CODIGO DE COMANDOS IGUAL
        try:
            if comando in ['menu', 'help', 'comandos']:
                return cmd_menu(mencion)
            #... pega aquí todo tu if/elif igual...
            else:
                return f"❌ *{mencion}*\n\nComando no reconocido\nEscribe.menu"
        except Exception as e:
            logger.error(f"Error: {e}")
            return "⚠️ Error interno"

    def procesar_normal(self, texto, mencion):
        t = texto.lower()
        respuestas = {
            'hola': f'👋 ¡Hola {mencion}! Soy *MINI AURA*\n\nEscribe.menu',
            'gracias': f'😊 ¡De nada {mencion}!',
            'adios': f'👋 ¡Hasta luego {mencion}!',
            'como estas': f'💪 ¡Estoy genial {mencion}!',
            'te amo': f'💙 ¡Yo también te quiero {mencion}!',
            'owner': f'👑 Mi dueño es +{OWNER_NUMBER}',
        }
        for clave, respuesta in respuestas.items():
            if clave in t:
                return respuesta
        return f"{mencion}, no entendí 🤔\nEscribe.menu"

if __name__ == '__main__':
    bot = BotMiniAura()
    try:
        asyncio.run(bot.iniciar())
    except KeyboardInterrupt:
        print("\n👋 Bot detenido")
    except Exception as e:
        logger.error(f"Error fatal: {e}")