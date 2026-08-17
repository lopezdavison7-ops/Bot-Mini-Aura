# -*- coding: utf-8 -*-

"""
💎 Comandos Premium Exclusivos de BOT MINI AURA
Version: 3.0.0 - Comandos únicos en el mercado
"""

import random
import json
import re
import hashlib
from datetime import datetime, timedelta
from src.lib.database import Database
from config.settings import PREFIX

db = Database()

# ==================== COMANDOS DE GENERACIÓN AVANZADA ====================

def generar_tarjeta_credito(args):
    """💳 Generar tarjeta de crédito falsa (para pruebas)"""
    try:
        # Generar número de tarjeta (falso, solo para demostración)
        numero = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        numero_formateado = f"{numero[:4]} {numero[4:8]} {numero[8:12]} {numero[12:16]}"
        
        # Generar fecha de expiración
        mes = random.randint(1, 12)
        año = random.randint(2025, 2030)
        
        # Generar CVV
        cvv = random.randint(100, 999)
        
        # Tipo de tarjeta
        tipos = ['Visa', 'Mastercard', 'American Express', 'Discover']
        tipo = random.choice(tipos)
        
        emojis_tarjeta = {
            'Visa': '💳', 'Mastercard': '💳', 
            'American Express': '💎', 'Discover': '💳'
        }
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  {emojis_tarjeta.get(tipo, '💳')} *TARJETA GENERADA* {emojis_tarjeta.get(tipo, '💳')}  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🏦 *Tipo:* {tipo}
💳 *Número:* {numero_formateado}
📅 *Expira:* {mes:02d}/{año}
🔒 *CVV:* {cvv}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ *ADVERTENCIA:*
Esta tarjeta es *FALSA*
Solo para fines educativos y de prueba
❌ *NO INTENTAR USARLA*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def generar_datos_persona(args):
    """👤 Generar identidad ficticia completa"""
    try:
        nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Pedro', 'Laura', 'Miguel', 'Sofía']
        apellidos = ['García', 'López', 'Martínez', 'Rodríguez', 'Hernández', 'Pérez']
        ciudades = ['Managua', 'León', 'Granada', 'Masaya', 'Matagalpa', 'Estelí']
        paises = ['Nicaragua', 'Costa Rica', 'Honduras', 'Guatemala', 'El Salvador']
        
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        ciudad = random.choice(ciudades)
        pais = random.choice(paises)
        
        # Generar teléfono
        telefono = f"+505 {random.randint(7000, 8999)} {random.randint(1000, 9999)}"
        
        # Generar email
        email = f"{nombre.lower()}{apellido.lower()}{random.randint(1, 99)}@gmail.com"
        
        # Generar edad
        edad = random.randint(18, 65)
        
        # Generar profesión
        profesiones = ['Ingeniero', 'Doctor', 'Profesor', 'Arquitecto', 'Abogado',
                      'Diseñador', 'Programador', 'Contador', 'Chef', 'Artista']
        profesion = random.choice(profesiones)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  👤 *IDENTIDAD GENERADA* 👤  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

👤 *Nombre:* {nombre} {apellido}
📅 *Edad:* {edad} años
💼 *Profesión:* {profesion}
📱 *Teléfono:* {telefono}
📧 *Email:* {email}
📍 *Ubicación:* {ciudad}, {pais}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ *Identidad ficticia*
Solo para fines creativos
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def generar_empresa(args):
    """🏢 Generar nombre de empresa"""
    try:
        prefijos = ['Tech', 'Soft', 'Digital', 'Smart', 'Mega', 'Super', 'Ultra', 'Cyber', 'Data', 'Cloud']
        sufijos = ['Solutions', 'Systems', 'Labs', 'Group', 'Corp', 'Inc', 'Tech', 'Soft', 'Digital', 'Net']
        
        nombre = f"{random.choice(prefijos)}{random.choice(sufijos)}"
        
        # Generar slogan
        slogans = [
            "Innovación para el futuro",
            "Tecnología que transforma",
            "Soluciones inteligentes",
            "El futuro es ahora",
            "Calidad y confianza"
        ]
        slogan = random.choice(slogans)
        
        # Generar dominio
        dominio = f"www.{nombre.lower().replace(' ', '')}.com"
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🏢 *EMPRESA GENERADA* 🏢  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🏢 *Nombre:* {nombre}
📝 *Slogan:* {slogan}
🌐 *Dominio:* {dominio}

💡 *Ideal para startups*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE ANÁLISIS ====================

def analizar_texto(args):
    """📊 Analizar texto detalladamente"""
    try:
        if not args:
            return f"❌ *Uso:* {PREFIX}analizar [texto]"
        
        texto = ' '.join(args)
        
        # Análisis
        caracteres = len(texto)
        palabras = len(texto.split())
        oraciones = len([s for s in texto.split('.') if s.strip()])
        vocales = sum(1 for c in texto.lower() if c in 'aeiouáéíóú')
        consonantes = sum(1 for c in texto.lower() if c.isalpha() and c not in 'aeiouáéíóú')
        numeros = sum(1 for c in texto if c.isdigit())
        espacios = sum(1 for c in texto if c.isspace())
        
        # Palabras más comunes
        palabras_lista = texto.lower().split()
        palabras_unicas = len(set(palabras_lista))
        
        # Tiempo estimado de lectura
        tiempo_lectura = max(1, palabras // 200)  # 200 palabras por minuto
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📊 *ANÁLISIS DE TEXTO* 📊  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Texto:* {texto[:50]}{'...' if len(texto) > 50 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 *ESTADÍSTICAS:*
├─ 🔤 Caracteres: {caracteres}
├─ 📝 Palabras: {palabras}
├─ 📄 Oraciones: {oraciones}
├─ 🔡 Vocales: {vocales}
├─ 🔤 Consonantes: {consonantes}
├─ 🔢 Números: {numeros}
├─ ⬜ Espacios: {espacios}
└─ 💎 Palabras únicas: {palabras_unicas}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ *Tiempo de lectura:* {tiempo_lectura} min
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def analizar_numero(args):
    """🔢 Analizar número detalladamente"""
    try:
        if not args or not args[0].isdigit():
            return f"❌ *Uso:* {PREFIX}numero [número]\n\nEjemplo: {PREFIX}numero 12345"
        
        numero = int(args[0])
        
        # Análisis
        es_par = numero % 2 == 0
        es_primo = True
        if numero < 2:
            es_primo = False
        else:
            for i in range(2, int(numero ** 0.5) + 1):
                if numero % i == 0:
                    es_primo = False
                    break
        
        # Factores
        factores = []
        for i in range(1, numero + 1):
            if numero % i == 0:
                factores.append(i)
        
        # Binario y hex
        binario = bin(numero)[2:]
        hexadecimal = hex(numero)[2:]
        
        # Suma de dígitos
        suma_digitos = sum(int(d) for d in str(numero))
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔢 *ANÁLISIS DE NÚMERO* 🔢  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🔢 *Número:* {numero}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 *PROPIEDADES:*
├─ {'✅' if es_par else '❌'} Es par
├─ {'✅' if es_primo else '❌'} Es primo
├─ 🔢 Binario: {binario}
├─ 🔢 Hex: {hexadecimal}
└─ ➕ Suma dígitos: {suma_digitos}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📐 *Factores ({len(factores)}):*
{', '.join(map(str, factores[:10]))}
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE CONVERSIÓN ====================

def convertir_temperatura(args):
    """🌡️ Convertir temperatura"""
    try:
        if len(args) < 2:
            return f"❌ *Uso:* {PREFIX}temp [valor] [c/f]\n\nEjemplo: {PREFIX}temp 25 c"
        
        valor = float(args[0])
        unidad = args[1].lower()
        
        if unidad in ['c', 'celsius']:
            # Celsius a Fahrenheit
            fahrenheit = (valor * 9/5) + 32
            kelvin = valor + 273.15
            
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🌡️ *CONVERSIÓN DE TEMP* 🌡️  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🌡️ *{valor}°C es igual a:*
├─ 🌡️ {fahrenheit:.1f}°F
└─ 🌡️ {kelvin:.2f}K
            """
        elif unidad in ['f', 'fahrenheit']:
            # Fahrenheit a Celsius
            celsius = (valor - 32) * 5/9
            kelvin = celsius + 273.15
            
            return f"""
🌡️ *{valor}°F es igual a:*
├─ 🌡️ {celsius:.1f}°C
└─ 🌡️ {kelvin:.2f}K
            """
        else:
            return "❌ *Unidad inválida*\n\nUsa 'c' para Celsius o 'f' para Fahrenheit"
    except Exception as e:
        return f"❌ *Error:* {e}"

def convertir_moneda(args):
    """💱 Convertir moneda (simulación)"""
    try:
        if len(args) < 2:
            return f"❌ *Uso:* {PREFIX}moneda [cantidad] [moneda]\n\nEjemplo: {PREFIX}moneda 100 usd"
        
        cantidad = float(args[0])
        moneda = args[1].upper()
        
        # Tasas de cambio aproximadas (simuladas)
        tasas = {
            'USD': {'EUR': 0.85, 'NIO': 36.5, 'MXN': 17.5, 'COP': 4000},
            'EUR': {'USD': 1.18, 'NIO': 43, 'MXN': 20.5},
            'NIO': {'USD': 0.027, 'EUR': 0.023},
        }
        
        if moneda not in tasas:
            return f"❌ *Moneda no soportada*\n\nSoportadas: USD, EUR, NIO"
        
        conversiones = tasas[moneda]
        
        resultado = []
        for moneda_destino, tasa in conversiones.items():
            resultado.append(f"├─ 💱 {cantidad * tasa:.2f} {moneda_destino}")
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  💱 *CONVERSIÓN MONEDA* 💱  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

💰 *{cantidad} {moneda} es igual a:*
{chr(10).join(resultado)}

⚠️ *Tasas aproximadas*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def convertir_distancia(args):
    """📏 Convertir distancia"""
    try:
        if len(args) < 2:
            return f"❌ *Uso:* {PREFIX}distancia [valor] [unidad]\n\nEjemplo: {PREFIX}distancia 5 km"
        
        valor = float(args[0])
        unidad = args[1].lower()
        
        if unidad in ['km', 'kilometros']:
            metros = valor * 1000
            millas = valor * 0.621371
            
            return f"""
📏 *{valor} km es igual a:*
├─ 📏 {metros:,.0f} metros
└─ 📏 {millas:.2f} millas
            """
        elif unidad in ['m', 'metros']:
            km = valor / 1000
            millas = valor * 0.000621371
            
            return f"""
📏 *{valor} metros es igual a:*
├─ 📏 {km:.3f} km
└─ 📏 {millas:.3f} millas
            """
        else:
            return "❌ *Unidad inválida*"
    except Exception as e:
        return f"❌ *Error:* {e}"

# ==================== COMANDOS DE DIVERSIÓN AVANZADA ====================

def generar_historia(args):
    """📖 Generar historia corta aleatoria"""
    try:
        inicios = [
            "En un mundo donde la tecnología dominaba todo",
            "Una noche oscura y tormentosa",
            "En un pequeño pueblo lejano",
            "Cuando el reloj marcó la medianoche",
            "En el año 3000, la humanidad"
        ]
        
        desarrollos = [
            "un héroe inesperado apareció para salvar el día",
            "un misterio sin resolver cambió todo",
            "una amistad improbable surgió",
            "un descubrimiento asombroso fue revelado",
            "una aventura épica comenzó"
        ]
        
        finales = [
            "y todos vivieron felices para siempre.",
            "y el mundo nunca volvió a ser igual.",
            "y una lección valiosa fue aprendida.",
            "y la esperanza renació.",
            "y el futuro brilló más que nunca."
        ]
        
        historia = f"{random.choice(inicios)}, {random.choice(desarrollos)} {random.choice(finales)}"
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📖 *HISTORIA ALEATORIA* 📖  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{historia}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ *Historia generada por IA*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def generar_poema(args):
    """📝 Generar poema corto"""
    try:
        poemas = [
            """🌟 *El sol brilla en lo alto*
💫 *Las estrellas en la noche*
💖 *Y en mi corazón*
✨ *Siempre hay un destello de esperanza*""",
            
            """🌙 *La luna me sonríe*
🌊 *Las olas me saludan*
🍃 *El viento me susurra*
💕 *Y el amor me rodea*""",
            
            """🌸 *Flores en primavera*
🦋 *Mariposas en el aire*
🌈 *Colores en el cielo*
💎 *Y belleza en todas partes*"""
        ]
        
        poema = random.choice(poemas)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📝 *POEMA GENERADO* 📝  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{poema}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💫 *Arte generado por IA*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def generar_consejo(args):
    """💡 Generar consejo aleatorio"""
    try:
        consejos = [
            "💡 *Nunca dejes de aprender* - El conocimiento es poder",
            "🌟 *Sonríe más* - La felicidad atrae cosas buenas",
            "💪 *No te rindas* - El éxito está más cerca de lo que crees",
            "🎯 *Establece metas* - Lo que no se mide, no se logra",
            "🌅 *Agradece cada día* - La gratitud transforma",
            "🚀 *Arriésgate* - Los grandes logros requieren valentía",
            "💎 *Valora tu tiempo* - Es el recurso más valioso",
            "🌈 *Mantén la esperanza* - Después de la tormenta sale el sol",
            "🔥 *Persigue tus sueños* - Nadie más lo hará por ti",
            "🌻 *Cuida tu mente* - Es el jardín de tu vida"
        ]
        
        consejo = random.choice(consejos)
        
        return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  💡 *CONSEJO DEL DÍA* 💡  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{consejo}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💫 *Comparte este consejo*
        """
    except Exception as e:
        return f"❌ *Error:* {e}"

def juego_palabras(args):
    """🎯 Juego de palabras encadenadas"""
    try:
        palabras = ['auto', 'tren', 'nube', 'elefante', 'estrella', 'árbol', 'libro', 'oso', 'ola', 'ave']
        
        if not args:
            return f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🎯 *PALABRAS ENCADENADAS* 🎯  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📝 *Reglas:*
Di una palabra que empiece con la última letra de la palabra anterior

🎮 *Empiezo yo:* {random.choice(palabras)}

💡 *Tu turno:*
        """
        
        palabra_anterior = args[0].lower()
        ultima_letra = palabra_anterior[-1]
        
        palabras_validas = [p for p in palabras if p.startswith(ultima_letra)]
        
        if not palabras_validas:
            return f"""
🎮 *¡Ganaste!* No tengo palabras con '{ultima_letra}'

🏆 *Eres un crack en las palabras*
            """
        
        respuesta = random.choice(palabras_validas)
        
        return f"""
🎮 *Mi palabra:* {respuesta}

📝 *Tu turno:*
    """
    except Exception as e:
        return f"❌ *Error:* {e}"