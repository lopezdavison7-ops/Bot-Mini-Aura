# -*- coding: utf-8 -*-

"""
💎 Comandos Exclusivos de BOT MINI AURA
Version: 3.0.0 - Comandos únicos que otros bots no tienen
"""

import random
import json
import re
from datetime import datetime, timedelta
from src.lib.database import Database
from config.settings import PREFIX, OWNER_NUMBER

db = Database()

# ==================== COMANDOS DE PREDICCIÓN ====================

def predecir_futuro(usuario, args):
    """🔮 Predecir el futuro del usuario"""
    try:
        predicciones = [
            "🌟 *Veo un futuro brillante* - Recibirás una sorpresa agradable esta semana",
            "💰 *El dinero llegará* - Una oportunidad financiera está cerca",
            "💑 *El amor tocará tu puerta* - Alguien especial aparecerá",
            "🚀 *Éxito profesional* - Un ascenso o reconocimiento laboral",
            "🎯 *Nuevos comienzos* - Un proyecto importante cambiará tu vida",
            "🌈 *Buena suerte* - Algo que esperabas por fin se dará",
            "🔥 *Cambios radicales* - Una decisión importante transformará todo",
            "⭐ *Reconocimiento* - Alguien valorará tu trabajo",
            "💎 *Premio inesperado* - Recibirás algo que no esperabas",
            "🌙 *Paz interior* - Encontrarás tranquilidad en algo nuevo"
        ]
        
        fecha = datetime.now()
        numero_suerte = random.randint(1, 99)
        color_suerte = random.choice(['🔴 Rojo', '🔵 Azul', '🟢 Verde', '🟡 Amarillo', '🟣 Morado', '🟠 Naranja'])
        
        prediccion = random.choice(predicciones)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔮 *PREDICCIÓN DEL FUTURO* 🔮  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📅 *Fecha:* {fecha.strftime('%d/%m/%Y')}

{prediccion}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔢 *Número de suerte:* {numero_suerte}
🎨 *Color de suerte:* {color_suerte}

💫 *Esta predicción es solo diversión*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def compatibilidad_nombres(args):
    """💑 Calcular compatibilidad detallada entre dos personas"""
    try:
        if len(args) < 2:
            return f"❌ *Uso:* {PREFIX}match [nombre1] [nombre2]\n\nEjemplo: {PREFIX}match Davison María"
        
        nombre1 = args[0].capitalize()
        nombre2 = args[1].capitalize()
        
        # Calcular compatibilidad basada en los nombres
        letras1 = set(nombre1.lower())
        letras2 = set(nombre2.lower())
        letras_comunes = letras1 & letras2
        
        # Factores de compatibilidad
        factor_letras = len(letras_comunes) * 10
        factor_longitud = min(len(nombre1), len(nombre2)) * 5
        factor_vocales = sum(1 for c in nombre1.lower() if c in 'aeiou') + sum(1 for c in nombre2.lower() if c in 'aeiou')
        
        compatibilidad = min(99, factor_letras + factor_longitud + factor_vocales)
        
        # Detalles adicionales
        if compatibilidad >= 80:
            nivel = "💑 *ALMAS GEMELAS*"
            consejo = "¡Están hechos el uno para el otro!"
        elif compatibilidad >= 60:
            nivel = "💖 *MUY COMPATIBLES*"
            consejo = "Tienen una conexión especial"
        elif compatibilidad >= 40:
            nivel = "😊 *COMPATIBLES*"
            consejo = "Pueden funcionar con esfuerzo"
        elif compatibilidad >= 20:
            nivel = "🤔 *REGULAR*"
            consejo = "Necesitan trabajar en la relación"
        else:
            nivel = "😅 *COMPLICADO*"
            consejo = "Quizás como amigos es mejor"
        
        # Categorías
        amor = min(99, compatibilidad + random.randint(-5, 5))
        amistad = min(99, compatibilidad + random.randint(-10, 10))
        trabajo = min(99, compatibilidad + random.randint(-8, 8))
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  💑 *MATCH PERFECTO* 💑  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👤 *{nombre1}* + 👤 *{nombre2}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 *COMPATIBILIDAD GENERAL:* {compatibilidad}%
{nivel}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💖 *Amor:* {amor}%
🤝 *Amistad:* {amistad}%
💼 *Trabajo:* {trabajo}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Consejo:* {consejo}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE PERSONALIDAD ====================

def test_personalidad(usuario, args):
    """🧠 Test de personalidad rápido"""
    try:
        preguntas = [
            {
                'pregunta': '¿Prefieres...',
                'opciones': ['A) Salir con amigos', 'B) Quedarte en casa'],
                'tipo': 'social'
            },
            {
                'pregunta': '¿Cómo tomas decisiones?',
                'opciones': ['A) Con lógica', 'B) Con intuición'],
                'tipo': 'decision'
            },
            {
                'pregunta': '¿Qué te describe mejor?',
                'opciones': ['A) Organizado', 'B) Espontáneo'],
                'tipo': 'estilo'
            }
        ]
        
        # Simular test (en producción se haría paso a paso)
        personalidades = [
            {'tipo': '🎨 *CREATIVO*', 'descripcion': 'Tienes una mente innovadora y artística'},
            {'tipo': '📊 *ANALÍTICO*', 'descripcion': 'Eres lógico y metódico'},
            {'tipo': '🗣️ *COMUNICADOR*', 'descripcion': 'Destacas por tu carisma y sociabilidad'},
            {'tipo': '🏃 *ACTIVO*', 'descripcion': 'Eres enérgico y siempre en movimiento'},
            {'tipo': '🧘 *REFLEXIVO*', 'descripcion': 'Piensas antes de actuar, eres profundo'},
            {'tipo': '🌟 *LÍDER*', 'descripcion': 'Tienes habilidades naturales de liderazgo'}
        ]
        
        personalidad = random.choice(personalidades)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🧠 *TEST DE PERSONALIDAD* 🧠  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👤 *Tu personalidad es:*

{personalidad['tipo']}

📝 *{personalidad['descripcion']}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Tip:* Haz el test completo con {PREFIX}test
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE GENERACIÓN ====================

def generar_correo(args):
    """📧 Generar correo electrónico temporal"""
    try:
        dominios = ['@gmail.com', '@hotmail.com', '@yahoo.com', '@outlook.com', '@proton.me']
        nombres = ['user', 'mini', 'aura', 'bot', 'cool', 'super', 'mega', 'ultra', 'pro', 'max']
        
        nombre = random.choice(nombres)
        numero = random.randint(100, 9999)
        dominio = random.choice(dominios)
        
        correo = f"{nombre}{numero}{dominio}"
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📧 *CORREO GENERADO* 📧  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📨 *Correo:* {correo}

💡 *Correo temporal generado*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def generar_usuario_instagram(args):
    """📸 Generar nombre de usuario para Instagram"""
    try:
        prefijos = ['el', 'la', 'soy', 'sr', 'sra', 'don', 'dona', 'mr', 'ms', 'the']
        adjetivos = ['cool', 'pro', 'real', 'super', 'mega', 'ultra', 'dark', 'light', 'golden', 'silver']
        sustantivos = ['gamer', 'artist', 'boss', 'king', 'queen', 'star', 'hero', 'legend', 'master', 'pro']
        
        prefijo = random.choice(prefijos)
        adjetivo = random.choice(adjetivos)
        sustantivo = random.choice(sustantivos)
        
        opciones = [
            f"{prefijo}_{adjetivo}_{sustantivo}",
            f"{adjetivo}.{sustantivo}",
            f"{prefijo}{adjetivo}{sustantivo}",
            f"{sustantivo}_{adjetivo}_official",
            f"{adjetivo}{sustantivo}{random.randint(1, 99)}"
        ]
        
        usuario_ig = random.choice(opciones)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃ 📸 *USUARIO DE INSTAGRAM* 📸 ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✨ *Nombre sugerido:* @{usuario_ig}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Otros disponibles:*
{'@' + ' ' .join(random.choices(opciones, k=3))}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def generar_bio(args):
    """📝 Generar biografía para redes sociales"""
    try:
        bios = [
            "🌟 Vivir la vida sin arrepentimientos",
            "💫 Soñador profesional | Amante de la vida",
            "🔥 Creando mi propia historia",
            "✨ La vida es corta, sonríe siempre",
            "🌈 Persiguiendo mis sueños",
            "💪 Trabajando en mi mejor versión",
            "⭐ La actitud lo es todo",
            "🎯 Enfocado en mis metas",
            "🌙 Noches de insomnio y sueños grandes",
            "💎 Brillando con luz propia"
        ]
        
        bio = random.choice(bios)
        emoji = random.choice(['✨', '🌟', '💫', '🔥', '💎', '🌈', '⭐', '🎯'])
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📝 *BIO GENERADA* 📝  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{emoji} *{bio}* {emoji}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Perfecta para Instagram, Twitter, etc.*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE HORÓSCOPO ====================

def horoscopo_diario(args):
    """⭐ Horóscopo diario"""
    try:
        signos = ['aries', 'tauro', 'geminis', 'cancer', 'leo', 'virgo',
                 'libra', 'escorpio', 'sagitario', 'capricornio', 'acuario', 'piscis']
        
        if not args:
            return f"❌ *Uso:* {PREFIX}horoscopo [signo]\n\nSignos: {', '.join(signos)}"
        
        signo = args[0].lower()
        
        if signo not in signos:
            return f"❌ *Signo inválido*\n\nSignos disponibles: {', '.join(signos)}"
        
        emojis_signos = {
            'aries': '♈', 'tauro': '♉', 'geminis': '♊', 'cancer': '♋',
            'leo': '♌', 'virgo': '♍', 'libra': '♎', 'escorpio': '♏',
            'sagitario': '♐', 'capricornio': '♑', 'acuario': '♒', 'piscis': '♓'
        }
        
        # Horóscopos por signo
        horoscopos = {
            'aries': "Hoy es un día para tomar la iniciativa. Tu energía estará por las nubes.",
            'tauro': "La paciencia será tu mejor aliada. Buen momento para finanzas.",
            'geminis': "Tu comunicación brillará. Aprovecha para resolver conflictos.",
            'cancer': "Las emociones estarán intensas. Dedica tiempo a tu familia.",
            'leo': "Tu carisma atraerá oportunidades. No tengas miedo de brillar.",
            'virgo': "La organización te dará paz. Ideal para ordenar tus ideas.",
            'libra': "El equilibrio llega a tu vida. Buenas noticias en el amor.",
            'escorpio': "Tu intuición está aguda. Confía en tus instintos.",
            'sagitario': "La aventura te llama. Aprovecha para explorar algo nuevo.",
            'capricornio': "Tu dedicación dará frutos. Reconocimiento profesional cerca.",
            'acuario': "Tu creatividad está en su punto. Comparte tus ideas.",
            'piscis': "Tu sensibilidad te guiará. Conectarás con alguien especial."
        }
        
        # Números y colores de suerte
        numero_suerte = random.randint(1, 99)
        colores = ['🔴 Rojo', '🔵 Azul', '🟢 Verde', '🟡 Amarillo', '🟣 Morado', '🟠 Naranja', '🩷 Rosa']
        color_suerte = random.choice(colores)
        
        emoji = emojis_signos.get(signo, '⭐')
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  {emoji} *HORÓSCOPO DIARIO* {emoji}  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y')}

{horoscopos[signo]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔢 *Número de suerte:* {numero_suerte}
🎨 *Color de suerte:* {color_suerte}

💫 *Que tengas un excelente día*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE CÁLCULO ====================

def calcular_imc(args):
    """⚖️ Calcular Índice de Masa Corporal"""
    try:
        if len(args) < 2:
            return f"❌ *Uso:* {PREFIX}imc [peso_kg] [altura_m]\n\nEjemplo: {PREFIX}imc 70 1.75"
        
        peso = float(args[0])
        altura = float(args[1])
        
        if peso <= 0 or altura <= 0:
            return "❌ *Valores inválidos*"
        
        imc = peso / (altura * altura)
        
        if imc < 18.5:
            categoria = "🔵 *Bajo peso*"
            consejo = "Consulta con un nutricionista"
        elif imc < 25:
            categoria = "🟢 *Peso normal*"
            consejo = "¡Excelente! Mantén tu estilo de vida"
        elif imc < 30:
            categoria = "🟡 *Sobrepeso*"
            consejo = "Considera hacer ejercicio regularmente"
        else:
            categoria = "🔴 *Obesidad*"
            consejo = "Recomendable consultar con un médico"
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ⚖️ *CALCULADORA IMC* ⚖️   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📏 *Peso:* {peso} kg
📐 *Altura:* {altura} m

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 *IMC:* {imc:.1f}
{categoria}

💡 *{consejo}*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def calcular_regla_tres(args):
    """📐 Regla de tres simple"""
    try:
        if len(args) < 3:
            return f"❌ *Uso:* {PREFIX}regla3 [valor1] [valor2] [valor3]\n\nSi {PREFIX}regla3 10 20 5 = 10 es a 20 como 5 es a X"
        
        v1 = float(args[0])
        v2 = float(args[1])
        v3 = float(args[2])
        
        if v1 == 0:
            return "❌ *El primer valor no puede ser 0*"
        
        resultado = (v2 * v3) / v1
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📐 *REGLA DE TRES* 📐  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Problema:*
{v1} es a {v2}
como {v3} es a *X*

━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ *Resultado:* X = {resultado:.2f}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def calcular_descuento(args):
    """🏷️ Calcular descuento"""
    try:
        if len(args) < 2:
            return f"❌ *Uso:* {PREFIX}descuento [precio] [porcentaje]\n\nEjemplo: {PREFIX}descuento 100 20"
        
        precio = float(args[0])
        descuento = float(args[1])
        
        if precio < 0 or descuento < 0 or descuento > 100:
            return "❌ *Valores inválidos*"
        
        ahorro = precio * (descuento / 100)
        precio_final = precio - ahorro
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🏷️ *CALCULAR DESCUENTO* 🏷️  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

💰 *Precio original:* ${precio:.2f}
🔖 *Descuento:* {descuento}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💸 *Ahorras:* ${ahorro:.2f}
✅ *Precio final:* ${precio_final:.2f}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE TIEMPO ====================

def cuenta_regresiva(args):
    """⏰ Cuenta regresiva a una fecha"""
    try:
        if len(args) < 3:
            return f"❌ *Uso:* {PREFIX}cuenta [día] [mes] [año]\n\nEjemplo: {PREFIX}cuenta 25 12 2024"
        
        dia = int(args[0])
        mes = int(args[1])
        año = int(args[2])
        
        fecha_objetivo = datetime(año, mes, dia)
        ahora = datetime.now()
        
        if fecha_objetivo < ahora:
            return "❌ *La fecha ya pasó*"
        
        diferencia = fecha_objetivo - ahora
        dias = diferencia.days
        horas = diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  ⏰ *CUENTA REGRESIVA* ⏰  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📅 *Fecha objetivo:* {dia}/{mes}/{año}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ *Faltan:*
📆 {dias} días
⏰ {horas} horas
⏱️ {minutos} minutos

💫 *¡El tiempo vuela!*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def edad_exacta(args):
    """🎂 Calcular edad exacta"""
    try:
        if len(args) < 3:
            return f"❌ *Uso:* {PREFIX}edadexacta [día] [mes] [año]\n\nEjemplo: {PREFIX}edadexacta 15 08 2000"
        
        dia = int(args[0])
        mes = int(args[1])
        año = int(args[2])
        
        fecha_nacimiento = datetime(año, mes, dia)
        ahora = datetime.now()
        
        años = ahora.year - fecha_nacimiento.year
        meses = ahora.month - fecha_nacimiento.month
        dias = ahora.day - fecha_nacimiento.day
        
        if dias < 0:
            meses -= 1
            dias += 30
        if meses < 0:
            años -= 1
            meses += 12
        
        # Calcular total de días vividos
        total_dias = (ahora - fecha_nacimiento).days
        total_horas = total_dias * 24
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🎂 *EDAD EXACTA* 🎂  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📅 *Nacimiento:* {dia}/{mes}/{año}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 *Tienes exactamente:*
📆 {años} años, {meses} meses y {dias} días

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 *Total:*
├─ {total_dias:,} días vividos
├─ {total_horas:,} horas vividas
└─ {total_dias * 1440:,} minutos vividos

💫 *¡Cada segundo cuenta!*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE TEXTO ====================

def texto_leet(args):
    """🔡 Convertir texto a lenguaje Leet (1337)"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}leet [texto]\n\nEjemplo: {PREFIX}leet hola"
        
        texto = ' '.join(args)
        
        leet_dict = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0',
            's': '5', 't': '7', 'b': '8', 'g': '9'
        }
        
        resultado = ''
        for letra in texto.lower():
            resultado += leet_dict.get(letra, letra)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔡 *TEXTO A LEET* 🔡  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Original:* {texto}
🔡 *Leet:* {resultado}

💡 *El lenguaje de los hackers*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def texto_morse(args):
    """📡 Convertir texto a código Morse"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}morse [texto]\n\nEjemplo: {PREFIX}morse SOS"
        
        texto = ' '.join(args).upper()
        
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
            'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----',
            '2': '..---', '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..', '9': '----.',
            ' ': '/'
        }
        
        morse = ' '.join(morse_dict.get(c, '?') for c in texto)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📡 *TEXTO A MORSE* 📡  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Texto:* {texto}
📡 *Morse:* {morse}

💡 *Código Morse internacional*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def texto_emoji(args):
    """😀 Convertir texto a emojis"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}textemoji [texto]\n\nEjemplo: {PREFIX}textemoji amor"
        
        texto = ' '.join(args).lower()
        
        emoji_dict = {
            'a': '🅰️', 'b': '🅱️', 'c': '🌜', 'd': '🌛',
            'e': '📧', 'f': '🎏', 'g': '🌀', 'h': '♓',
            'i': 'ℹ️', 'j': '🎷', 'k': '🎋', 'l': '👢',
            'm': '♏', 'n': '♑', 'o': '⭕', 'p': '🅿️',
            'q': '🔍', 'r': '®️', 's': '💲', 't': '✝️',
            'u': '⛎', 'v': '✌️', 'w': '〰️', 'x': '❌',
            'y': '🍸', 'z': '💤', ' ': '⏺️'
        }
        
        resultado = ' '.join(emoji_dict.get(c, c) for c in texto)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  😀 *TEXTO A EMOJIS* 😀  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Texto:* {texto}

{resultado}

💡 *¡Mensaje con estilo!*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"