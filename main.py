import asyncio
import random
import logging
from datetime import datetime
from flask import Flask, render_template_string

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

app = Flask(__name__)
qr_url_global = ""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BOT MINI AURA - QR</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #1a1a1a; color: white; font-family: Arial; text-align: center; padding: 20px; }
        .qr-box { background: white; padding: 20px; display: inline-block; border-radius: 10px; margin: 20px; }
        img { width: 300px; height: 300px; }
        h1 { color: #25D366; }
        .info { margin: 20px; }
        .btn { background: #25D366; color: white; padding: 15px 30px; border-radius: 5px; text-decoration: none; display: inline-block; margin: 10px; }
    </style>
</head>
<body>
    <h1>🤖 BOT MINI AURA</h1>
    <p>📱 Número a vincular: +{{ numero }}</p>
    <div class="qr-box">
        <img src="{{ qr_data }}" alt="QR">
    </div>
    <p>📱 Abre WhatsApp en tu teléfono</p>
    <p>→ Ajustes → Dispositivos vinculados</p>
    <p>→ Vincular dispositivo</p>
    <p>→ Escanea el QR</p>
    <p style="color: yellow;">⚠️ El QR expira en 60 segundos</p>
</body>
</html>
"""

@app.route('/qr')
def mostrar_qr():
    global qr_url_global
    if qr_url_global:
        return render_template_string(HTML_TEMPLATE, qr_data=qr_url_global, numero=NUMERO_VINCULAR)
    return "QR no disponible aún. Espera..."

class BotMiniAura:
    def __init__(self):
        self.sock = None
        self.mensajes_procesados = set()

    async def iniciar(self):
        global qr_url_global
        
        config = default_connection_config()
        config['auth'] = {'creds': init_auth_creds(), 'keys': {}}
        config['browser'] = Browsers.macOS('Safari')
        config['logger'].level = 'info'

        self.sock = make_socket(config)
        ev = self.sock['ev']

        async def on_conn(update):
            global qr_url_global
            if update.get('qr'):
                qr_url_global = update['qr']
                print("\n" + "=" * 50)
                print("📱 ESCANEA EL QR AQUÍ:")
                print("=" * 50 + "\n")
                print(f"http://localhost:5000/qr")
                print("\n" + "=" * 50)
                print("Abre esa URL en tu navegador")
                print("=" * 50 + "\n")
                
            if update.get('connection') == 'open':
                qr_url_global = ""
                print("\n" + "=" * 50)
                print("✅ ¡BOT MINI AURA CONECTADO!")
                print(f"👑 Owner: +{OWNER_NUMBER}")
                print("=" * 50 + "\n")

        async def on_message(message):
            await self.procesar_mensaje(message)

        ev.on('connection.update', lambda u: asyncio.ensure_future(on_conn(u)))
        ev.on('messages.upsert', lambda m: asyncio.ensure_future(on_message(m)))

        print("\n" + "=" * 50)
        print("🤖 BOT MINI AURA")
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
    
    # Ejecutar Flask en un hilo
    import threading
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    # Ejecutar bot
    asyncio.run(bot.iniciar())