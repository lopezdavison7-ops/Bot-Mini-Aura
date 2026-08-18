import asyncio
import random
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MINI-AURA')

from WAeys.Defaults.index import default_connection_config
from WAeys.Utils.auth_utils import init_auth_creds
from WAeys.Utils.browser_utils import Browsers
from WAeys.Socket.socket import make_socket

PREFIX = "."
OWNER_NUMBER = "50578391933"
VERSION = "4.0.0"

class BotMiniAura:
    def __init__(self):
        self.sock = None
        self.mensajes_procesados = set()
        self.bot_vinculado = False

    async def iniciar(self):
        config = default_connection_config()
        config['auth'] = {'creds': init_auth_creds(), 'keys': {}}
        config['browser'] = Browsers.macOS('Safari')
        config['logger'].level = 'info'

        self.sock = make_socket(config)
        ev = self.sock['ev']

        async def on_conn(update):
            if update.get('qr'):
                print("\n" + "=" * 50)
                print("🔗 *OPCIÓN 2: ESCANEA ESTE QR*")
                print("=" * 50 + "\n")
                print(update['qr'])
                print("\n" + "=" * 50)
            if update.get('connection') == 'open':
                print("\n✅ ¡BOT CONECTADO!")
                print(f"👑 Owner: +{OWNER_NUMBER}")
                print("=" * 50 + "\n")

        async def on_message(message):
            await self.procesar_mensaje(message)

        ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))
        ev.on('messages.upsert', lambda m: asyncio.ensure_future(on_message(m)))

        print("\n" + "=" * 50)
        print("🤖 BOT MINI AURA")
        print("=" * 50)
        print("\n¿Cómo deseas vincular el bot?\n")
        print("1️⃣ Código de 8 dígitos")
        print("   Escribe: 1")
        print("2️⃣ QR")
        print("   Escribe: 2")
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

            if texto == '1' and not self.bot_vinculado:
                print("\n📱 Escribe el número a vincular:")
                print("Ejemplo: 50578391933\n")
                return

            if texto == '2' and not self.bot_vinculado:
                print("\n📱 ESCANEA EL QR QUE APARECE ARRIBA\n")
                return

            if texto.startswith(PREFIX):
                comando = texto[len(PREFIX):].split(' ')[0].lower()
                args = texto.split(' ')[1:] if ' ' in texto else []
                respuesta = await self.ejecutar_comando(comando, args, remitente, mencion)
            else:
                respuesta = self.procesar_normal(texto, mencion)

            if respuesta:
                await self.sock['sendMessage'](remitente, {'text': respuesta})

        except Exception as e:
            logger.error(f"Error procesando: {e}")

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
            elif comando in ['ppt', 'piedra']:
                if not args:
                    return "✊ Uso: .ppt piedra/papel/tijera"
                opciones = ['piedra', 'papel', 'tijera']
                bot_opcion = random.choice(opciones)
                user_opcion = args[0].lower()
                if user_opcion not in opciones:
                    return "❌ Opción inválida"
                if user_opcion == bot_opcion:
                    return f"🤝 *Empate!*\n\nBot: {bot_opcion}\nTú: {user_opcion}"
                elif (user_opcion == 'piedra' and bot_opcion == 'tijera') or (user_opcion == 'papel' and bot_opcion == 'piedra') or (user_opcion == 'tijera' and bot_opcion == 'papel'):
                    return f"🎉 *¡GANASTE!*\n\nBot: {bot_opcion}\nTú: {user_opcion}"
                else:
                    return f"😢 *Perdiste*\n\nBot: {bot_opcion}\nTú: {user_opcion}"
            elif comando in ['8ball', 'bola']:
                return random.choice(["Sí ✅", "No ❌", "Quizás 🤔", "Definitivamente 💯"])
            elif comando in ['calc', 'math']:
                try:
                    return f"🧮 *Resultado:* {eval(' '.join(args))}"
                except:
                    return "❌ Error en la operación"
            elif comando in ['fecha', 'date']:
                return f"📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y')}"
            elif comando in ['hora', 'time']:
                return f"⏰ *Hora:* {datetime.now().strftime('%H:%M:%S')}"
            elif comando in ['password', 'pass']:
                import string
                chars = string.ascii_letters + string.digits
                return f"🔑 *Contraseña:* `{''.join(random.choice(chars) for _ in range(12))}`"
            elif comando in ['reverso', 'reverse']:
                if args:
                    return f"🔄 *Invertido:* {' '.join(args)[::-1]}"
                return "❌ Uso: .reverso texto"
            elif comando in ['mayus', 'upper']:
                if args:
                    return f"⬆️ *Mayúsculas:* {' '.join(args).upper()}"
                return "❌ Uso: .mayus texto"
            elif comando in ['minus', 'lower']:
                if args:
                    return f"⬇️ *Minúsculas:* {' '.join(args).lower()}"
                return "❌ Uso: .minus texto"
            elif comando in ['contar', 'count']:
                if args:
                    return f"📊 *Caracteres:* {len(' '.join(args))}"
                return "❌ Uso: .contar texto"
            elif comando in ['morse', 'codigomorse']:
                if args:
                    morse_dict = {'A': '.-', 'B': '-...', 'C': '-.-.', 'S': '...', 'O': '---', 'H': '....', 'L': '.-..'}
                    resultado = ' '.join(morse_dict.get(c.upper(), '?') for c in ' '.join(args))
                    return f"📡 *Morse:* {resultado}"
                return "❌ Uso: .morse texto"
            elif comando in ['leet', '1337']:
                if args:
                    leet_dict = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
                    resultado = ''.join(leet_dict.get(c.lower(), c) for c in ' '.join(args))
                    return f"🔡 *Leet:* {resultado}"
                return "❌ Uso: .leet texto"
            elif comando in ['dato', 'fact']:
                return random.choice(["🐙 Los pulpos tienen 3 corazones", "🍯 La miel nunca caduca", "🦩 Los flamencos son rosados por su comida"])
            elif comando in ['chiste', 'joke']:
                return random.choice(["😂 ¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter", "😂 ¿Qué le dice un semáforo a otro? No me mires, me estoy cambiando"])
            elif comando in ['frase', 'motivacion']:
                return random.choice(["🌟 El éxito es la suma de pequeños esfuerzos", "💪 Cree en ti y todo será posible"])
            elif comando in ['amor', 'love']:
                if len(args) >= 2:
                    return f"💑 *Compatibilidad*\n\n{args[0]} + {args[1]} = *{random.randint(50, 100)}%*"
                return "❌ Uso: .amor nombre1 nombre2"
            elif comando in ['futuro', 'predecir']:
                return random.choice(["🔮 Veo éxito en tu futuro", "🌟 Algo bueno viene pronto", "💫 Una sorpresa te espera"])
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
├─ .ppt - Piedra papel tijera
└─ .8ball - Bola mágica

🛠️ *UTILIDADES*
├─ .calc - Calculadora
├─ .fecha - Fecha
├─ .hora - Hora
├─ .password - Contraseña
├─ .reverso - Invertir
├─ .mayus - Mayúsculas
├─ .minus - Minúsculas
├─ .contar - Contar
├─ .morse - Morse
└─ .leet - Leet

🎭 *DIVERSIÓN*
├─ .dato - Dato curioso
├─ .chiste - Chiste
├─ .frase - Motivación
├─ .amor - Compatibilidad
└─ .futuro - Predecir

━━━━━━━━━━━━━━━━━━━━━━━━━━━
👑 Owner: +{OWNER_NUMBER}
📊 Versión: {VERSION}
        """

if __name__ == '__main__':
    bot = BotMiniAura()
    asyncio.run(bot.iniciar())