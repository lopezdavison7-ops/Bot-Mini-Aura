# -*- coding: utf-8 -*-

"""
🎭 Comandos de Diversión para BOT MINI AURA
Version: 2.0.0
"""

import random
from datetime import datetime
from config.settings import PREFIX

def dato_curioso():
    """Dato curioso aleatorio"""
    datos = [
        "🐙 Los pulpos tienen 3 corazones y su sangre es azul.",
        "🍯 La miel nunca se echa a perder. Se han encontrado tarros de miel de 3000 años en perfecto estado.",
        "🦩 Los flamencos son rosados porque comen camarones.",
        "🌍 Un día en Venus dura más que un año completo en Venus.",
        "🐝 Las abejas pueden reconocer rostros humanos.",
        "🌙 La Luna se aleja de la Tierra 3.8 cm cada año.",
        "🐘 Los elefantes son los únicos animales que no pueden saltar.",
        "🍌 Las bananas son técnicamente bayas.",
        "🧠 El cerebro humano genera suficiente electricidad para encender un foco.",
        "🦈 Los tiburones existen desde antes que los árboles.",
        "🌞 El Sol es 333,000 veces más grande que la Tierra.",
        "🐧 Los pingüinos se arrodillan para proponer matrimonio.",
        "🦋 Las mariposas pueden saborear con sus patas.",
        "🐬 Los delfines se llaman por nombres únicos.",
        "🌟 Hay más estrellas en el universo que granos de arena en todas las playas de la Tierra."
    ]
    
    dato = random.choice(datos)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🤓 *DATO CURIOSO* 🤓    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{dato}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *¿Sabías algo nuevo hoy?*
    """

def chiste():
    """Chiste aleatorio"""
    chistes = [
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter. 🐦",
        "¿Qué le dice un semáforo a otro? No me mires, me estoy cambiando. 🚦",
        "¿Por qué el libro de matemáticas estaba triste? Porque tenía muchos problemas. 📚",
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba! 🐝",
        "¿Por qué los esqueletos no pelean? Porque no tienen agallas. 💀",
        "¿Qué le dice un árbol a otro? ¡Qué pasa, tronco! 🌳",
        "¿Por qué el mar está azul? Porque los peces hacen 'blue, blue' 🐟",
        "¿Qué le dice un gusano a otro gusano? Voy a dar una vuelta a la manzana. 🍎",
        "¿Cuál es el animal más antiguo? La cebra, porque está en blanco y negro. 🦓",
        "¿Por qué los programadores confunden Halloween con Navidad? Porque OCT 31 = DEC 25. 💻"
    ]
    
    chiste_elegido = random.choice(chistes)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃      😂 *CHISTE* 😂      ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{chiste_elegido}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
😄 *¡Espero que te haya hecho reír!*
    """

def frase_motivacional():
    """Frase motivacional aleatoria"""
    frases = [
        "🌟 *El éxito no es definitivo, el fracaso no es fatal: lo que cuenta es el coraje para continuar.*",
        "💪 *Cree en ti mismo y todo será posible.*",
        "🚀 *El único lugar donde el éxito viene antes que el trabajo es en el diccionario.*",
        "🎯 *No cuentes los días, haz que los días cuenten.*",
        "🌈 *Después de la tormenta, siempre sale el sol.*",
        "🔥 *Tu única limitación es tu mente.*",
        "⭐ *El futuro pertenece a quienes creen en sus sueños.*",
        "🏆 *La disciplina es el puente entre metas y logros.*",
        "💎 *Eres más fuerte de lo que crees.*",
        "🌻 *Cada día es una nueva oportunidad.*"
    ]
    
    frase = random.choice(frases)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🌟 *FRASE MOTIVACIONAL* 🌟  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{frase}
    """

def piropo():
    """Piropo aleatorio"""
    piropos = [
        "🌹 Si la belleza fuera tiempo, tú serías la eternidad.",
        "💫 ¿Eres un ángel? Porque caíste del cielo.",
        "🌟 Eres como el WiFi: no te veo, pero me conecto contigo.",
        "🌸 Si ser hermosa fuera delito, estarías en cadena perpetua.",
        "💎 Eres más valiosa que todas las joyas del mundo.",
        "🦋 Eres como una mariposa: hermosa y difícil de alcanzar.",
        "🌺 Las flores se marchitan, pero tu belleza es eterna.",
        "☀️ Tu sonrisa ilumina más que el sol.",
        "🌙 Eres como la luna: brillas en la oscuridad.",
        "💖 Mi corazón late más fuerte cuando te veo."
    ]
    
    piropo_elegido = random.choice(piropos)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃      💖 *PIROPO* 💖      ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{piropo_elegido}
    """

def bola_ocho(args):
    """Bola mágica 8"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}8ball [pregunta]\n\nEjemplo: {PREFIX}8ball ¿Seré rico?"
        
        respuestas = [
            "✅ *Sí, definitivamente*",
            "💫 *Sin duda alguna*",
            "🌟 *Todo apunta a que sí*",
            "🤔 *Pregunta de nuevo más tarde*",
            "❓ *No estoy seguro*",
            "😕 *No cuentes con ello*",
            "❌ *Mi respuesta es no*",
            "💭 *Concéntrate y pregunta de nuevo*",
            "✨ *Las estrellas dicen que sí*",
            "🌙 *Mejor no te lo digo ahora*"
        ]
        
        respuesta = random.choice(respuestas)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🎱 *BOLA MÁGICA 8* 🎱    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

❓ *Pregunta:* {' '.join(args)}

{respuesta}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def calcular_amor(args):
    """Calcular compatibilidad de amor"""
    try:
        if len(args) < 2:
            return f"❌ *Uso:* {PREFIX}amor [nombre1] [nombre2]\n\nEjemplo: {PREFIX}amor Juan María"
        
        nombre1 = args[0]
        nombre2 = args[1]
        
        # Generar porcentaje basado en los nombres
        seed = sum(ord(c) for c in nombre1 + nombre2)
        random.seed(seed)
        porcentaje = random.randint(50, 100)
        
        if porcentaje >= 90:
            mensaje = "💑 *¡Almas gemelas!*"
        elif porcentaje >= 75:
            mensaje = "💖 *¡Muy compatible!*"
        elif porcentaje >= 60:
            mensaje = "😊 *Buena compatibilidad*"
        elif porcentaje >= 50:
            mensaje = "🤔 *Puede funcionar*"
        else:
            mensaje = "😅 *Solo amigos*"
        
        barra = '❤️' * (porcentaje // 10) + '🖤' * (10 - porcentaje // 10)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    💕 *CALCULADORA DE AMOR* 💕    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👤 *{nombre1}* + 👤 *{nombre2}*

💖 *Compatibilidad:* {porcentaje}%
{barra}

{mensaje}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def calcular_edad(args):
    """Calcular edad desde año de nacimiento"""
    try:
        if not args or not args[0].isdigit():
            return f"❌ *Uso:* {PREFIX}edad [año]\n\nEjemplo: {PREFIX}edad 2000"
        
        año_nacimiento = int(args[0])
        año_actual = datetime.now().year
        
        if año_nacimiento < 1900 or año_nacimiento > año_actual:
            return f"❌ *Año inválido*\n\nDebe estar entre 1900 y {año_actual}"
        
        edad = año_actual - año_nacimiento
        
        if edad < 0:
            return "❌ *Aún no has nacido* 😅"
        elif edad < 13:
            categoria = "👶 *Niño/a*"
        elif edad < 18:
            categoria = "🧑 *Adolescente*"
        elif edad < 30:
            categoria = "👨 *Joven adulto*"
        elif edad < 60:
            categoria = "👨‍💼 *Adulto*"
        else:
            categoria = "👴 *Adulto mayor*"
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🎂 *CALCULAR EDAD* 🎂    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📅 *Año de nacimiento:* {año_nacimiento}
🎂 *Edad:* {edad} años
👤 *Categoría:* {categoria}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def generar_nombre():
    """Generar nombre aleatorio"""
    nombres = [
        "Alejandro", "María", "Carlos", "Ana", "José", "Laura",
        "Diego", "Sofía", "Javier", "Valentina", "Miguel", "Isabella",
        "Andrés", "Camila", "Fernando", "Daniela", "Ricardo", "Lucía",
        "Gabriel", "Fernanda", "Rafael", "Paula", "Antonio", "Elena",
        "Manuel", "Carmen", "Pedro", "Gloria", "Luis", "Rosa"
    ]
    
    apellidos = [
        "García", "Rodríguez", "Martínez", "López", "Hernández",
        "González", "Pérez", "Sánchez", "Ramírez", "Torres",
        "Flores", "Rivera", "Gómez", "Díaz", "Cruz",
        "Morales", "Reyes", "Gutiérrez", "Ortiz", "Chávez"
    ]
    
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🎭 *NOMBRE ALEATORIO* 🎭  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👤 *Nombre generado:*
*{nombre} {apellido}*
    """

def color_aleatorio():
    """Generar color aleatorio"""
    colores = [
        "🔴 Rojo", "🔵 Azul", "🟢 Verde", "🟡 Amarillo", "🟣 Morado",
        "🟠 Naranja", "🟤 Café", "⚫ Negro", "⚪ Blanco", "🔘 Gris",
        "🌸 Rosa", "🩵 Celeste", "🩷 Rosado", "🫒 Oliva", "🏵️ Dorado"
    ]
    
    color = random.choice(colores)
    hex_color = f"#{random.randint(0, 0xFFFFFF):06X}"
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🎨 *COLOR ALEATORIO* 🎨  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{color}
🎨 *Hex:* {hex_color}
    """

def emoji_aleatorio():
    """Emoji aleatorio"""
    emojis = [
        "😀", "😂", "🤣", "😊", "😍", "🤩", "😎", "🥳", "🤗", "🤔",
        "😅", "😉", "😘", "🥰", "😜", "🤪", "😇", "🤠", "🤡", "👻",
        "💀", "👽", "🤖", "🎃", "😺", "🐶", "🦊", "🐼", "🦁", "🐸",
        "🦄", "🐙", "🦋", "🌈", "⭐", "🌟", "💫", "🔥", "💯", "❤️"
    ]
    
    emoji = random.choice(emojis)
    
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🎯 *EMOJI ALEATORIO* 🎯  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{emoji} *¡Aquí tienes tu emoji!*
    """