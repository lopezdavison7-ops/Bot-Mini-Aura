# -*- coding: utf-8 -*-

"""
📋 Sistema de Menús para BOT MINI AURA
Version: 2.0.0
"""

from config.settings import PREFIX, NOMBRE_BOT, VERSION, OWNER_NUMBER

def mostrar_menu_principal():
    """Menú principal del bot"""
    menu = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🤖 *{NOMBRE_BOT}* 🤖   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✨ *¡Hola! Soy MINI AURA* ✨
Tu bot multi-propósito para WhatsApp

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 *MENÚ PRINCIPAL*
━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ *COMANDOS GENERALES*
├─ {PREFIX}menu - Ver este menú
├─ {PREFIX}info - Información del bot
├─ {PREFIX}ping - Verificar latencia
├─ {PREFIX}perfil - Ver tu perfil
└─ {PREFIX}owner - Contactar al dueño

💰 *ECONOMÍA*
├─ {PREFIX}monedas - Ver tu balance
├─ {PREFIX}trabajar - Ganar monedas
├─ {PREFIX}top - Ranking de usuarios
├─ {PREFIX}robar - Robar monedas
├─ {PREFIX}depositar - Guardar monedas
├─ {PREFIX}retirar - Sacar monedas
└─ {PREFIX}regalar - Transferir monedas

🎮 *JUEGOS*
├─ {PREFIX}dado - Tirar un dado
├─ {PREFIX}moneda - Lanzar moneda
├─ {PREFIX}ppt - Piedra, papel o tijera
├─ {PREFIX}ahorcado - Jugar ahorcado
├─ {PREFIX}trivia - Preguntas y respuestas
├─ {PREFIX}ruleta - Ruleta rusa
└─ {PREFIX}loteria - Jugar lotería

🛠️ *UTILIDADES*
├─ {PREFIX}clima - Ver clima
├─ {PREFIX}calc - Calculadora
├─ {PREFIX}traducir - Traductor
├─ {PREFIX}password - Generar contraseña
├─ {PREFIX}fecha - Ver fecha actual
├─ {PREFIX}hora - Ver hora actual
├─ {PREFIX}binario - Texto a binario
├─ {PREFIX}hex - Texto a hexadecimal
├─ {PREFIX}base64 - Codificar texto
├─ {PREFIX}md5 - Hash MD5
└─ {PREFIX}reverso - Invertir texto

📥 *DESCARGAS*
├─ {PREFIX}yt - Descargar YouTube
├─ {PREFIX}tiktok - Descargar TikTok
├─ {PREFIX}ig - Descargar Instagram
├─ {PREFIX}fb - Descargar Facebook
└─ {PREFIX}tw - Descargar Twitter/X

🎭 *DIVERSIÓN*
├─ {PREFIX}dato - Dato curioso
├─ {PREFIX}chiste - Chiste aleatorio
├─ {PREFIX}frase - Frase motivacional
├─ {PREFIX}piropo - Piropo
├─ {PREFIX}8ball - Pregunta a la bola
├─ {PREFIX}amor - Calcular amor
├─ {PREFIX}edad - Calcular edad
├─ {PREFIX}nombre - Nombre aleatorio
├─ {PREFIX}color - Color aleatorio
└─ {PREFIX}emoji - Emoji aleatorio

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *TIP:* Usa {PREFIX}ayuda [comando] para más info
━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    return menu

def mostrar_menu_economia():
    """Menú de economía"""
    menu = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃      💰 *ECONOMÍA* 💰      ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

📊 *COMANDOS DE ECONOMÍA*

{PREFIX}monedas - Ver tu balance
{PREFIX}trabajar - Trabajar y ganar monedas
{PREFIX}top - Ver ranking de usuarios
{PREFIX}robar - Intentar robar a alguien
{PREFIX}depositar - Guardar monedas en el banco
{PREFIX}retirar - Retirar monedas del banco
{PREFIX}regalar - Transferir monedas a otro usuario

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Gana monedas trabajando cada hora*
    """
    return menu

def mostrar_menu_juegos():
    """Menú de juegos"""
    menu = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃      🎮 *JUEGOS* 🎮       ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🎲 *JUEGOS DISPONIBLES*

{PREFIX}dado - Tirar dado (1-6)
{PREFIX}moneda - Cara o cruz
{PREFIX}ppt - Piedra, papel o tijera
{PREFIX}ahorcado - Jugar ahorcado
{PREFIX}trivia - Preguntas y respuestas
{PREFIX}ruleta - Ruleta rusa
{PREFIX}loteria - Jugar lotería

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 *Gana monedas jugando*
    """
    return menu

def mostrar_menu_utilidades():
    """Menú de utilidades"""
    menu = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🛠️ *UTILIDADES* 🛠️     ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🔧 *HERRAMIENTAS ÚTILES*

{PREFIX}clima [ciudad] - Ver clima
{PREFIX}calc [expresión] - Calculadora
{PREFIX}traducir [texto] - Traducir texto
{PREFIX}password - Generar contraseña
{PREFIX}fecha - Ver fecha actual
{PREFIX}hora - Ver hora actual
{PREFIX}binario [texto] - Texto a binario
{PREFIX}hex [texto] - Texto a hexadecimal
{PREFIX}base64 [texto] - Codificar en Base64
{PREFIX}md5 [texto] - Generar hash MD5
{PREFIX}reverso [texto] - Invertir texto
{PREFIX}mayus [texto] - Convertir a mayúsculas
{PREFIX}minus [texto] - Convertir a minúsculas
{PREFIX}contar [texto] - Contar caracteres

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Todos los comandos son gratuitos*
    """
    return menu

def mostrar_menu_diversion():
    """Menú de diversión"""
    menu = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   🎭 *DIVERSIÓN* 🎭       ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🎪 *COMANDOS DIVERTIDOS*

{PREFIX}dato - Dato curioso aleatorio
{PREFIX}chiste - Chiste aleatorio
{PREFIX}frase - Frase motivacional
{PREFIX}piropo - Recibir un piropo
{PREFIX}8ball [pregunta] - Pregunta a la bola mágica
{PREFIX}amor [nombre1] [nombre2] - Calcular compatibilidad
{PREFIX}edad [año] - Calcular edad
{PREFIX}nombre - Generar nombre aleatorio
{PREFIX}color - Color aleatorio
{PREFIX}emoji - Emoji aleatorio

━━━━━━━━━━━━━━━━━━━━━━━━━━━
😄 *¡Diviértete!*
    """
    return menu

def mostrar_ayuda_comando(comando):
    """Ayuda específica de cada comando"""
    ayudas = {
        's': f"📝 *COMANDO STICKER*\n\nUso: {PREFIX}s\nDescripción: Convierte una imagen en sticker\n\nEnvía una imagen con el comando {PREFIX}s",
        'yt': f"📝 *COMANDO YOUTUBE*\n\nUso: {PREFIX}yt [enlace]\nDescripción: Descarga videos de YouTube\n\nEjemplo: {PREFIX}yt https://youtube.com/watch?v=...",
        'tiktok': f"📝 *COMANDO TIKTOK*\n\nUso: {PREFIX}tiktok [enlace]\nDescripción: Descarga videos de TikTok sin marca de agua\n\nEjemplo: {PREFIX}tiktok https://tiktok.com/...",
        'monedas': f"📝 *COMANDO MONEDAS*\n\nUso: {PREFIX}monedas\nDescripción: Muestra tu balance actual de monedas",
        'trabajar': f"📝 *COMANDO TRABAJAR*\n\nUso: {PREFIX}trabajar\nDescripción: Trabaja para ganar monedas\n\nGanas entre 10-50 monedas por trabajo",
        'dado': f"📝 *COMANDO DADO*\n\nUso: {PREFIX}dado\nDescripción: Tira un dado de 6 caras\n\nSi sacas 6, ganas monedas extra",
        'clima': f"📝 *COMANDO CLIMA*\n\nUso: {PREFIX}clima [ciudad]\nDescripción: Muestra el clima actual\n\nEjemplo: {PREFIX}clima Managua",
        'calc': f"📝 *COMANDO CALCULADORA*\n\nUso: {PREFIX}calc [expresión]\nDescripción: Realiza operaciones matemáticas\n\nEjemplo: {PREFIX}calc 5+3*2",
        'robar': f"📝 *COMANDO ROBAR*\n\nUso: {PREFIX}robar [número]\nDescripción: Intenta robar monedas\n\nProbabilidad de éxito: 30%",
        '8ball': f"📝 *COMANDO BOLA MÁGICA*\n\nUso: {PREFIX}8ball [pregunta]\nDescripción: Haz una pregunta y la bola responderá\n\nEjemplo: {PREFIX}8ball ¿Seré rico?",
    }
    
    return ayudas.get(comando, f"❌ No hay ayuda disponible para este comando.\n\nEscribe {PREFIX}menu para ver todos los comandos.")