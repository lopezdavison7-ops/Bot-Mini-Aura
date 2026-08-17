# -*- coding: utf-8 -*-

"""
🎮 Sistema de Juegos para BOT MINI AURA
Version: 2.0.0
"""

import random
from src.lib.database import Database
from config.settings import PREFIX

db = Database()

def tirar_dado(usuario):
    """Tirar un dado"""
    try:
        resultado = random.randint(1, 6)
        premio = 0
        
        if resultado == 6:
            premio = 10
            db.actualizar_monedas(usuario, premio)
        
        dados = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
        
        mensaje = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🎲 *TIRADA DE DADO* 🎲   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{dados[resultado-1]} *Sacaste un {resultado}*
"""
        if premio > 0:
            mensaje += f"\n🎉 *¡BONUS!* Ganaste {premio} monedas"
        
        return mensaje
    except Exception as e:
        return f"❌ *Error al tirar dado:* {e}"

def lanzar_moneda(usuario):
    """Lanzar una moneda"""
    try:
        resultado = random.choice(['cara', 'cruz'])
        
        # Sistema de apuestas
        monedas_apostadas = 5
        db.actualizar_monedas(usuario, -monedas_apostadas)
        
        if random.random() < 0.5:
            premio = monedas_apostadas * 2
            db.actualizar_monedas(usuario, premio)
            resultado_mensaje = f"🎉 *¡GANASTE!* {premio} monedas"
        else:
            resultado_mensaje = f"😢 *Perdiste* {monedas_apostadas} monedas"
        
        emoji = '🪙' if resultado == 'cara' else '🔘'
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🪙 *LANZAMIENTO* 🪙    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{emoji} *Resultado:* {resultado.upper()}
{resultado_mensaje}
        """
    except Exception as e:
        return f"❌ *Error al lanzar moneda:* {e}"

def piedra_papel_tijera(usuario, args):
    """Juego de piedra, papel o tijera"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}ppt [piedra/papel/tijera]\n\nEjemplo: {PREFIX}ppt piedra"
        
        opcion_usuario = args[0].lower()
        opciones = ['piedra', 'papel', 'tijera']
        
        if opcion_usuario not in opciones:
            return f"❌ *Opción inválida*\n\nOpciones: piedra, papel, tijera"
        
        opcion_bot = random.choice(opciones)
        
        # Determinar ganador
        if opcion_usuario == opcion_bot:
            resultado = "🤝 *EMPATE*"
            premio = 2
        elif (opcion_usuario == 'piedra' and opcion_bot == 'tijera') or \
             (opcion_usuario == 'papel' and opcion_bot == 'piedra') or \
             (opcion_usuario == 'tijera' and opcion_bot == 'papel'):
            resultado = "🎉 *¡GANASTE!*"
            premio = 5
            db.actualizar_monedas(usuario, premio)
        else:
            resultado = "😢 *PERDISTE*"
            premio = 0
        
        emojis = {'piedra': '🪨', 'papel': '📄', 'tijera': '✂️'}
        
        mensaje = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  ✊ *PIEDRA, PAPEL O TIJERA* ✋  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{emojis[opcion_usuario]} *Tú:* {opcion_usuario}
{emojis[opcion_bot]} *Bot:* {opcion_bot}

*{resultado}*
"""
        if premio > 0:
            mensaje += f"\n💰 Ganaste *{premio}* monedas"
        
        return mensaje
    except Exception as e:
        return f"❌ *Error en el juego:* {e}"

def ahorcado(usuario):
    """Juego del ahorcado"""
    try:
        palabras = ['python', 'whatsapp', 'bot', 'programacion', 'juego', 
                   'computadora', 'internet', 'celular', 'teclado', 'monitor',
                   'auriculares', 'bateria', 'camara', 'pantalla', 'aplicacion']
        palabra = random.choice(palabras)
        letras_adivinadas = []
        intentos = 6
        
        # Guardar estado del juego
        db.guardar_juego(usuario, 'ahorcado', {
            'palabra': palabra,
            'letras': [],
            'intentos': intentos
        })
        
        palabra_oculta = ''.join([letra if letra in letras_adivinadas else '_' for letra in palabra])
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🎯 *AHORCADO* 🎯    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Palabra:* {palabra_oculta}
📏 *Letras:* {len(palabra)}
❤️ *Intentos restantes:* {intentos}

Envía letras para adivinar
💡 *Tip:* La palabra tiene {len(palabra)} letras
        """
    except Exception as e:
        return f"❌ *Error en el juego:* {e}"

def trivia(usuario):
    """Juego de trivia"""
    try:
        preguntas = [
            {
                'pregunta': '¿Cuál es la capital de Francia?',
                'opciones': ['A) Madrid', 'B) París', 'C) Londres'],
                'respuesta': 'B'
            },
            {
                'pregunta': '¿Cuántos planetas hay en el sistema solar?',
                'opciones': ['A) 7', 'B) 8', 'C) 9'],
                'respuesta': 'B'
            },
            {
                'pregunta': '¿Quién creó Python?',
                'opciones': ['A) Guido van Rossum', 'B) Bill Gates', 'C) Steve Jobs'],
                'respuesta': 'A'
            },
            {
                'pregunta': '¿Cuál es el animal más grande del mundo?',
                'opciones': ['A) Elefante', 'B) Ballena azul', 'C) Jirafa'],
                'respuesta': 'B'
            },
            {
                'pregunta': '¿En qué año llegó el hombre a la Luna?',
                'opciones': ['A) 1965', 'B) 1969', 'C) 1972'],
                'respuesta': 'B'
            }
        ]
        
        pregunta = random.choice(preguntas)
        
        # Guardar estado
        db.guardar_juego(usuario, 'trivia', {'respuesta': pregunta['respuesta']})
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🧠 *TRIVIA* 🧠    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *{pregunta['pregunta']}*

{chr(10).join(pregunta['opciones'])}

Responde con la letra correcta (A, B o C)
💡 *Premio:* 10 monedas si aciertas
        """
    except Exception as e:
        return f"❌ *Error en el juego:* {e}"

def ruleta_rusa(usuario):
    """Juego de ruleta rusa"""
    try:
        # Sistema de apuestas
        costo = 10
        db.actualizar_monedas(usuario, -costo)
        
        # 1 de 6 probabilidad de "perder"
        if random.random() < 0.17:  # 17% de probabilidad
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🔫 *RULETA RUSA* 🔫    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

💥 *¡BANG!* Has perdido
😵 Perdiste {costo} monedas

¡Qué mala suerte!
            """
        else:
            premio = random.randint(20, 50)
            db.actualizar_monedas(usuario, premio)
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🔫 *RULETA RUSA* 🔫    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🔫 *¡Click!* Has sobrevivido
🎉 Ganaste *{premio}* monedas

¡Qué valiente!
            """
    except Exception as e:
        return f"❌ *Error en el juego:* {e}"

def loteria(usuario):
    """Juego de lotería"""
    try:
        # Costo del boleto
        costo = 5
        db.actualizar_monedas(usuario, -costo)
        
        # Generar números
        numeros_usuario = random.sample(range(1, 50), 3)
        numeros_ganadores = random.sample(range(1, 50), 3)
        
        # Verificar aciertos
        aciertos = len(set(numeros_usuario) & set(numeros_ganadores))
        
        if aciertos == 3:
            premio = 500
            mensaje = "🎉 *¡JACKPOT!* ¡Ganaste el premio mayor!"
        elif aciertos == 2:
            premio = 100
            mensaje = "🌟 *¡Muy bien!* ¡Dos aciertos!"
        elif aciertos == 1:
            premio = 10
            mensaje = "👍 *Un acierto*"
        else:
            premio = 0
            mensaje = "😢 *Sin aciertos*"
        
        if premio > 0:
            db.actualizar_monedas(usuario, premio)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🎰 *LOTERÍA* 🎰    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🎫 *Tus números:* {', '.join(map(str, numeros_usuario))}
🏆 *Números ganadores:* {', '.join(map(str, numeros_ganadores))}

{mensaje}
💰 *Premio:* {premio} monedas
        """
    except Exception as e:
        return f"❌ *Error en el juego:* {e}"