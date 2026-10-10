import os
import sys
import time
import random
import logging
import threading
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MINI-AURA')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

SESSION_DIR = os.path.join(BASE_DIR, 'wa_session')
DB_PATH = os.path.join(SESSION_DIR, 'mini-aura.db')

try:
    from neonize.client import NewClient
    from neonize.events import ConnectedEv, MessageEv, PairStatusEv
    try:
        from neonize.utils.message import extract_text
    except Exception:
        def extract_text(m):
            t = getattr(m, 'conversation', '') or ''
            if not t:
                etm = getattr(m, 'extendedTextMessage', None)
                if etm is not None:
                    t = getattr(etm, 'text', '') or ''
            return t
except ModuleNotFoundError:
    print('❌ neonize no instalado. Ejecuta: pip install neonize qrcode')
    sys.exit(1)

# ═══ Comandos del bot (opcionales si falta la carpeta) ═══
try:
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
    COMANDOS_DISPONIBLES = True
except ImportError:
    COMANDOS_DISPONIBLES = False
    logger.warning("⚠️ No se encontró la carpeta 'commands'. Comandos deshabilitados.")

PREFIX = "."
NUMERO_VINCULAR = "50576641902"
OWNER_NUMBER = "50578391933"
VERSION = "5.0.0-neonize"

def _print_qr(qr_string):
    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(qr_string)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except Exception:
        print(qr_string)

class BotMiniAura:
    def __init__(self):
        self.client = None
        self.metodo = '1'            # '1' = código 8 dígitos, '2' = QR
        self.numero = NUMERO_VINCULAR
        self.procesados = set()
        self.conectado_este_ciclo = False

    # ─────────────── Menú de vinculación ───────────────
    def menu(self):
        print('\n' + '═' * 46)
        print(f'   🤖 BOT MINI AURA v{VERSION} · VINCULACIÓN')
        print('   [1] 🔢 Código de 8 dígitos')
        print('   [2] 📷 Código QR')
        print('═' * 46)
        try:
            opt = input('➡️  Elige opción (1/2): ').strip() or '1'
            self.metodo = '2' if opt == '2' else '1'
            if self.metodo == '1':
                num = input(f'📞 Número (internacional sin +, Enter = {NUMERO_VINCULAR}): ').strip()
                self.numero = num or NUMERO_VINCULAR
                print('📱 Ten abierto: WhatsApp → Dispositivos vinculados → Vincular con número.')
            else:
                print('📷 El QR aparecerá abajo: WhatsApp → Dispositivos vinculados → Vincular dispositivo.')
        except (EOFError, OSError):
            print(f'⚠️ Sin entrada interactiva: código de 8 dígitos con {NUMERO_VINCULAR}.')
            self.metodo, self.numero = '1', NUMERO_VINCULAR

    # ─────────────── Cliente y eventos ───────────────
    def make_client(self):
        os.makedirs(SESSION_DIR, exist_ok=True)
        try:
            return NewClient('MINI AURA', database=DB_PATH)
        except TypeError:
            return NewClient(DB_PATH[:-3])  # versiones que usan el nombre como ruta de DB

    def registrar_eventos(self, client):
        @client.event(ConnectedEv)
        def on_connected(cli, ev):
            self.conectado_este_ciclo = True
            print('\n✅ ¡CONECTADO Y CON SESIÓN ACTIVA!')
            print(f'👑 Owner: +{OWNER_NUMBER}')
            print('🤖 BOT MINI AURA ESCUCHANDO MENSAJES\n')

        @client.event(PairStatusEv)
        def on_pair(cli, ev):
            try:
                user = ev.ID.User
            except Exception:
                user = '?'
            print(f'👤 Sesión vinculada como: +{user}')

        qr_dec = getattr(client, 'qr', None)
        if qr_dec is not None:
            @qr_dec
            def on_qr(cli, qr):
                if self.metodo != '2':
                    return
                if isinstance(qr, (bytes, bytearray)):
                    data = qr.decode(errors='ignore')
                elif isinstance(qr, str):
                    data = qr
                else:
                    codes = getattr(qr, 'Codes', None) or getattr(qr, 'codes', None) or []
                    data = codes[0] if len(codes) else str(qr)
                print('\n📷 ESCANEA ESTE QR:\n')
                _print_qr(data)

        @client.event(MessageEv)
        def on_message(cli, message):
            self.procesar_mensaje(cli, message)

    # ─────────────── Hilo que pide el código de 8 dígitos ───────────────
    def lanzar_pedido_codigo(self):
        def worker():
            for _ in range(120):                      # espera conexión (60 s)
                if self.client.is_connected:
                    break
                time.sleep(0.5)
            if not self.client.is_connected:
                print('❌ Sin conexión con WhatsApp en 60 s; reintentando ciclo...')
                return
            for _ in range(20):                       # gracia 10 s por si retoma sesión
                if self.client.is_logged_in:
                    return
                time.sleep(0.5)
            if self.client.is_logged_in:
                return
            if self.metodo == '2':
                print('📷 Esperando el escaneo del QR...')
                return
            self._solicitar_codigo()
        threading.Thread(target=worker, daemon=True).start()

    def _solicitar_codigo(self, reintento=0):
        try:
            pair_fn = getattr(self.client, 'PairPhone', None) or getattr(self.client, 'pair_code')
            code = pair_fn(self.numero, True)
            print('\n' + '═' * 46)
            print(f'🔢 CÓDIGO DE EMPAREJAMIENTO: {code}')
            print('📞 Mételo YA en WhatsApp (caduca en ~1-2 min):')
            print('   Dispositivos vinculados → Vincular con número')
            print(f'   → +{self.numero}')
            print('═' * 46 + '\n')
        except Exception as err:
            msg = str(err).lower()
            if ('overlimit' in msg or 'rate' in msg) and reintento < 1:
                print('🚫 RATE-OVERLIMIT: el bot esperará 45 min y reintentará solo...')
                time.sleep(45 * 60)
                self._solicitar_codigo(reintento + 1)
            else:
                print(f'❌ Error pidiendo código: {err}')

    # ─────────────── Mensajes ───────────────
    def procesar_mensaje(self, cli, message):
        try:
            info = message.Info
            src = info.MessageSource
            if getattr(src, 'IsFromMe', False):
                return
            msg_id = getattr(info, 'ID', None)
            if not msg_id or msg_id in self.procesados:
                return
            if len(self.procesados) > 1000:
                self.procesados.clear()
            self.procesados.add(msg_id)

            texto = (extract_text(message.Message) or '').strip()
            if not texto:
                return
            chat = src.Chat
            sender = src.Sender
            numero = getattr(sender, 'User', '') or str(chat)
            mencion = f'@{numero}'

            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' ' in texto else []
                respuesta = self.ejecutar_comando(comando, args, numero, mencion)
            else:
                respuesta = self.procesar_normal(texto, mencion)
            if respuesta:
                cli.send_message(chat, respuesta)
        except Exception as e:
            logger.error(f'Error procesando mensaje: {e}')

    def ejecutar_comando(self, comando, args, usuario, mencion):
        if not COMANDOS_DISPONIBLES:
            return "⚠️ Comandos deshabilitados: falta la carpeta 'commands'."
        try:
            if comando in ['menu', 'help', 'comandos']:
                return cmd_menu(mencion)
            # ... pega aquí todo tu if/elif de comandos igual que lo tenías ...
            else:
                return f"❌ *{mencion}*\n\nComando no reconocido\nEscribe .menu"
        except Exception as e:
            logger.error(f'Error en comando: {e}')
            return '⚠️ Error interno'

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
        return None

    # ─────────────── Ciclo de vida 24/7 ───────────────
    def iniciar(self):
        print('\n' + '═' * 46)
        print(f'   🤖 BOT MINI AURA v{VERSION} (neonize/whatsmeow)')
        print(f'   👑 Owner: +{OWNER_NUMBER}')
        print('═' * 46)
        while True:
            if not os.path.exists(DB_PATH):
                self.menu()
            self.conectado_este_ciclo = False
            self.client = self.make_client()
            self.registrar_eventos(self.client)
            self.lanzar_pedido_codigo()
            try:
                self.client.connect()   # bloquea hasta desconexión/logout
            except KeyboardInterrupt:
                print('\n👋 Bot detenido')
                return
            except Exception as e:
                logger.error(f'Error de conexión: {e}')

            if self.conectado_este_ciclo and not self.client.is_logged_in:
                print('🔒 Sesión revocada por WhatsApp: limpiando base de sesión...')
                if os.path.exists(DB_PATH):
                    os.remove(DB_PATH)
                continue
            print('🔄 Reconectando en 5 s (la sesión se retoma sola)...')
            time.sleep(5)

if __name__ == '__main__':
    BotMiniAura().iniciar()