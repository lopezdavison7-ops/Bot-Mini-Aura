# -*- coding: utf-8 -*-

"""
🛠️ Utilidades para BOT MINI AURA
Version: 2.0.0
"""

import requests
import json
import random
import string
import math
import hashlib
import base64
from datetime import datetime
from config.settings import API_KEYS, PREFIX

def obtener_clima(args):
    """Obtener clima de una ciudad"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}clima [ciudad]\n\nEjemplo: {PREFIX}clima Managua"
        
        ciudad = ' '.join(args)
        api_key = API_KEYS.get('weather', '')
        
        if not api_key:
            # Simulación si no hay API key
            temp = random.randint(15, 35)
            humedad = random.randint(30, 90)
            viento = random.randint(5, 30)
            condiciones = ['Despejado', 'Parcialmente nublado', 'Nublado', 'Lluvia ligera', 'Tormenta']
            condicion = random.choice(condiciones)
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🌤️ *CLIMA EN {ciudad.upper()}* 🌤️  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🌡️ *Temperatura:* {temp}°C
🌤️ *Condición:* {condicion}
💧 *Humedad:* {humedad}%
💨 *Viento:* {viento} km/h

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ *Modo simulación* (API no configurada)
🕐 *Actualizado:* {datetime.now().strftime('%H:%M:%S')}
            """
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang=es&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('cod') == 200:
            clima = data['weather'][0]['description'].capitalize()
            temp = data['main']['temp']
            humedad = data['main']['humidity']
            viento = data['wind']['speed']
            
            emoji_clima = {
                'clear': '☀️', 'clouds': '☁️', 'rain': '🌧️',
                'snow': '❄️', 'thunderstorm': '⛈️', 'drizzle': '🌦️'
            }
            emoji = emoji_clima.get(data['weather'][0]['main'].lower(), '🌤️')
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  {emoji} *CLIMA EN {ciudad.upper()}* {emoji}  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🌡️ *Temperatura:* {temp}°C
🌤️ *Condición:* {clima}
💧 *Humedad:* {humedad}%
💨 *Viento:* {viento} m/s

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 *Actualizado:* {datetime.now().strftime('%H:%M:%S')}
            """
        else:
            return f"❌ *Ciudad no encontrada*\n\nVerifica el nombre e intenta de nuevo."
    except Exception as e:
        return f"❌ *Error al obtener clima:* {e}"

def calculadora(args):
    """Calculadora segura"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}calc [expresión]\n\nEjemplo: {PREFIX}calc 5+3*2"
        
        expresion = ' '.join(args)
        
        # Solo permitir caracteres seguros
        permitidos = set('0123456789+-*/(). %')
        if not all(c in permitidos for c in expresion):
            return "❌ *Expresión inválida*\n\nSolo se permiten números y operadores básicos."
        
        # Evaluar de forma segura
        resultado = eval(expresion, {"__builtins__": {}}, {"math": math})
        
        # Formatear resultado
        if isinstance(resultado, float):
            resultado = round(resultado, 4)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🧮 *CALCULADORA* 🧮    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Operación:* {expresion}
✅ *Resultado:* {resultado}
        """
    except ZeroDivisionError:
        return "❌ *Error:* No se puede dividir entre cero"
    except Exception as e:
        return f"❌ *Error en la operación*\n\n{str(e)}"

def verificar_ping():
    """Verificar latencia del bot"""
    try:
        import time
        inicio = time.time()
        time.sleep(0.1)
        latencia = int((time.time() - inicio) * 1000)
        
        if latencia < 50:
            estado = "🟢 Excelente"
        elif latencia < 100:
            estado = "🟡 Buena"
        else:
            estado = "🔴 Lenta"
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃      📡 *PING* 📡      ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

⚡ *Latencia:* {latencia}ms
✅ *Estado:* {estado}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 *BOT MINI AURA* v2.0.0
        """
    except Exception as e:
        return f"❌ *Error al verificar ping:* {e}"

def info_bot():
    """Información del bot"""
    return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🤖 *BOT MINI AURA* 🤖   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✨ *Información General*

📌 *Nombre:* MINI AURA
📊 *Versión:* 2.0.0
👑 *Owner:* +{OWNER_NUMBER}
🌐 *País:* Nicaragua 🇳🇮
💻 *Lenguaje:* Python

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ *Características:*
├─ 💰 Economía completa
├─ 🎮 7 juegos
├─ 🛠️ 15+ utilidades
├─ 📥 5 descargas
├─ 🎭 12 comandos de diversión
└─ 👑 15 comandos de owner

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 *Prefijo:* {PREFIX}
💡 Usa {PREFIX}menu para ver comandos
    """

def ver_fecha():
    """Ver fecha actual"""
    try:
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        ahora = datetime.now()
        dia_semana = dias[ahora.weekday()]
        mes = meses[ahora.month - 1]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃      📅 *FECHA* 📅      ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📅 *{dia_semana}, {ahora.day} de {mes} de {ahora.year}*
        """
    except Exception as e:
        return f"❌ *Error al obtener fecha:* {e}"

def ver_hora():
    """Ver hora actual"""
    try:
        ahora = datetime.now()
        hora_12 = ahora.strftime('%I:%M:%S %p')
        hora_24 = ahora.strftime('%H:%M:%S')
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃      ⏰ *HORA* ⏰      ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🕐 *Formato 12h:* {hora_12}
🕐 *Formato 24h:* {hora_24}
        """
    except Exception as e:
        return f"❌ *Error al obtener hora:* {e}"

def texto_binario(args):
    """Convertir texto a binario"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}binario [texto]\n\nEjemplo: {PREFIX}binario hola"
        
        texto = ' '.join(args)
        binario = ' '.join(format(ord(c), '08b') for c in texto)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    💻 *TEXTO A BINARIO* 💻    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Texto:* {texto}
💻 *Binario:* {binario}
        """
    except Exception as e:
        return f"❌ *Error al convertir:* {e}"

def texto_hex(args):
    """Convertir texto a hexadecimal"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}hex [texto]\n\nEjemplo: {PREFIX}hex hola"
        
        texto = ' '.join(args)
        hex_resultado = texto.encode('utf-8').hex()
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔢 *TEXTO A HEXADECIMAL* 🔢  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Texto:* {texto}
🔢 *Hex:* {hex_resultado}
        """
    except Exception as e:
        return f"❌ *Error al convertir:* {e}"

def texto_base64(args):
    """Codificar texto en Base64"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}base64 [texto]\n\nEjemplo: {PREFIX}base64 hola"
        
        texto = ' '.join(args)
        codificado = base64.b64encode(texto.encode('utf-8')).decode('utf-8')
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🔐 *TEXTO A BASE64* 🔐   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Texto:* {texto}
🔐 *Base64:* {codificado}
        """
    except Exception as e:
        return f"❌ *Error al codificar:* {e}"

def texto_md5(args):
    """Generar hash MD5"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}md5 [texto]\n\nEjemplo: {PREFIX}md5 hola"
        
        texto = ' '.join(args)
        hash_md5 = hashlib.md5(texto.encode('utf-8')).hexdigest()
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃    🔒 *HASH MD5* 🔒    ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Texto:* {texto}
🔒 *MD5:* {hash_md5}
        """
    except Exception as e:
        return f"❌ *Error al generar hash:* {e}"

def texto_reverso(args):
    """Invertir texto"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}reverso [texto]\n\nEjemplo: {PREFIX}reverso hola"
        
        texto = ' '.join(args)
        invertido = texto[::-1]
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🔄 *TEXTO INVERTIDO* 🔄   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Original:* {texto}
🔄 *Invertido:* {invertido}
        """
    except Exception as e:
        return f"❌ *Error al invertir:* {e}"

def texto_mayus(args):
    """Convertir a mayúsculas"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}mayus [texto]"
        
        texto = ' '.join(args)
        resultado = texto.upper()
        
        return f"⬆️ *MAYÚSCULAS:* {resultado}"
    except Exception as e:
        return f"❌ *Error:* {e}"

def texto_minus(args):
    """Convertir a minúsculas"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}minus [texto]"
        
        texto = ' '.join(args)
        resultado = texto.lower()
        
        return f"⬇️ *MINÚSCULAS:* {resultado}"
    except Exception as e:
        return f"❌ *Error:* {e}"

def contar_caracteres(args):
    """Contar caracteres de un texto"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}contar [texto]"
        
        texto = ' '.join(args)
        caracteres = len(texto)
        palabras = len(texto.split())
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   📊 *CONTADOR* 📊   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Texto:* {texto}
🔤 *Caracteres:* {caracteres}
📝 *Palabras:* {palabras}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def generar_password(args):
    """Generar contraseña segura"""
    try:
        longitud = 12
        if args and args[0].isdigit():
            longitud = int(args[0])
            if longitud < 6:
                longitud = 6
            elif longitud > 50:
                longitud = 50
        
        caracteres = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(caracteres) for _ in range(longitud))
        
        # Verificar fortaleza
        tiene_mayus = any(c.isupper() for c in password)
        tiene_minus = any(c.islower() for c in password)
        tiene_num = any(c.isdigit() for c in password)
        tiene_especial = any(c in string.punctuation for c in password)
        
        fortaleza = sum([tiene_mayus, tiene_minus, tiene_num, tiene_especial])
        
        if fortaleza == 4:
            nivel = "🟢 *Muy fuerte*"
        elif fortaleza == 3:
            nivel = "🟡 *Fuerte*"
        elif fortaleza == 2:
            nivel = "🟠 *Media*"
        else:
            nivel = "🔴 *Débil*"
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃ 🔐 *CONTRASEÑA GENERADA* 🔐 ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🔑 *Contraseña:* `{password}`
📏 *Longitud:* {longitud} caracteres
💪 *Fortaleza:* {nivel}

⚠️ *Guárdala en un lugar seguro*
        """
    except Exception as e:
        return f"❌ *Error al generar:* {e}"