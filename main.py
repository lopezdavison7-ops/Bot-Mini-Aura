import asyncio
import random
import logging
import qrcode
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MINI-AURA')

from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds
from WAeys.Utils.browser_utils import Browsers
from WAeys.Socket.socket import make_socket

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
        config['auth'] = {'creds': init_auth_creds(), 'keys': {}}
        config['browser'] = Browsers.macOS('Safari')
        config['logger'].level = 'info'

        self.sock = make_socket(config)
        ev = self.sock['ev']

        async def on_conn(update):
            if update.get('qr'):
                url_qr = update['qr']
                print("\n" + "=" * 50)
                print("📱 ESCANEA EL QR PARA VINCULAR")
                print(f"Número: +{NUMERO_VINCULAR}")
                print("=" * 50 + "\n")
                
                # Generar QR real como imagen
                try:
                    qr = qrcode.QRCode(version=1, box_size=10, border=2)
                    qr.add_data(url_qr)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    img.save("qr.png")
                    print("✅ QR generado como: qr.png")
                    print("📱 Descarga el archivo qr.png y escanéalo")
                except:
                    pass
                
                print("\n🔗 O usa este enlace en tu navegador:")
                print(url_qr)
                print("=" * 50 + "\n")
                
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

        print("\n" + "=" * 50)
        print("🤖 BOT MINI AURA")
        print("=" * 50)
        print("Iniciando conexión...")
        print("=" * 50 + "\n")

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
            logger.error(f"Error: {e}")

    async def ejecutar_comando(self, comando, args, remitente, mencion):
        try:
            if comando in ['menu', 'ayuda', 'help', 'start']:
                return self.menu_principal(mencion)
            elif comando in ['ping', 'test']:
                return "🏓 *Pong!* Bot activo"
            elif comando in ['info', 'bot']:
                return f"🤖 *BOT MINI AURA*\n\n📊 Versión: {VERSION}\n👑 Owner: +{OWNER_NUMBER}"
            elif comando in ['owner', 'dueño']:
                return f"👑 *OWNER*\n\n📱 Número: +{OWNER_NUMBER}"
            elif comando in ['dado', 'dice', 'roll']:
                return f"🎲 *{mencion}*\n\nSacaste: *{random.randint(1, 6)}*"
            elif comando in ['moneda', 'coin', 'cara']:
                return f"🪙 *{mencion}*\n\nResultado: *{random.choice(['Cara', 'Cruz'])}*"
            elif comando in ['8ball', 'bola']:
                return random.choice(["Sí ✅", "No ❌", "Quizás 🤔"])
            elif comando in ['calc', 'math']:
                try:
                    return f"🧮 *Resultado:* {eval(' '.join(args))}"
                except:
                    return "❌ Error"
            elif comando in ['fecha', 'date']:
                return f"📅 {datetime.now().strftime('%d/%m/%Y')}"
            elif comando in ['hora', 'time']:
                return f"⏰ {datetime.now().strftime('%H:%M:%S')}"
            elif comando in ['password', 'pass']:
                import string
                chars = string.ascii_letters + string.digits
                return f"🔑 `{''.join(random.choice(chars) for _ in range(12))}`"
            elif comando in ['dato', 'fact']:
                return random.choice(["🐙 Pulpos tienen 3 corazones", "🍯 La miel nunca caduca"])
            elif comando in ['chiste', 'joke']:
                return random.choice(["😂 ¿Por qué los pájaros no usan Facebook?", "😂 ¿Qué le dice un semáforo a otro?"])
            elif comando in ['frase', 'motivacion']:
                return random.choice(["🌟 El éxito es la suma de pequeños esfuerzos", "💪 Cree en ti"])
            elif comando in ['amor', 'love']:
                if len(args) >= 2:
                    return f"💑 {args[0]} + {args[1]} = {random.randint(50, 100)}%"
                return "❌ Uso: .amor nombre1 nombre2"
            elif comando in ['futuro', 'predecir']:
                return random.choice(["🔮 Veo éxito", "🌟 Algo bueno viene"])
            else:
                return f"❌ *{mencion}*\n\nComando no reconocido\n\nEscribe .menu"
        except Exception as e:
            logger.error(f"Error: {e}")
            return "⚠️ Error interno"

    def procesar_normal(self, texto, mencion):
        t = texto.lower()
        if 'hola' in t:
            return f"👋 ¡Hola {mencion}! Escribe .menu"
        elif 'gracias' in t:
            return "😊 ¡De nada!"
        elif 'adios' in t:
            return "👋 ¡Hasta luego!"
        return f"{mencion}, escribe .menu"

    def menu_principal(self, mencion):
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🤖 *BOT MINI AURA* 🤖   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👋 *Hola {mencion}*

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
└─ .password - Contraseña

🎭 *DIVERSIÓN*
├─ .dato - Dato curioso
├─ .chiste - Chiste
├─ .frase - Motivación
├─ .amor - Compatibilidad
└─ .futuro - Predecir

━━━━━━━━━━━━━━━━━━━━━━━━━━━
👑 Owner: +{OWNER_NUMBER}
        """

if __name__ == '__main__':
    bot = BotMiniAura()
    asyncio.run(bot.iniciar())