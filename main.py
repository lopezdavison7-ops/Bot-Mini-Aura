#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 BOT MINI AURA - Bot Multi-propósito para WhatsApp
Versión: 3.0.0
Owner: +50578391933
Total de comandos: 101
"""

import os
import sys
import json
import logging
import traceback
from pathlib import Path
from datetime import datetime
from functools import wraps

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('MINI-AURA')

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from flask import Flask, request, jsonify
    from twilio.twiml.messaging_response import MessagingResponse
    from config.settings import *
    from src.commands.menu import *
    from src.commands.economia import *
    from src.commands.juegos import *
    from src.commands.utilidades import *
    from src.commands.descargas import *
    from src.commands.admin import *
    from src.commands.grupo import *
    from src.commands.owner import *
    from src.commands.vinculacion import *
    from src.commands.diversion import *
    from src.commands.exclusivos import *
    from src.commands.premium import *
    from src.lib.database import Database
    from src.lib.functions import *
    from src.lib.vincular import SistemaVinculacion
    from src.lib.decorators import *
except ImportError as e:
    logger.error(f"Error importando módulos: {e}")
    logger.error("Ejecuta: pip install -r requirements.txt")
    sys.exit(1)

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mini-aura-secret-2024')

# Inicializar base de datos
db = Database()
db.initialize()

# Inicializar sistema de vinculación
sistema_vinculacion = SistemaVinculacion()

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Ruta no encontrada', 'status': 404}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Error 500: {e}")
    return jsonify({'error': 'Error interno del servidor', 'status': 500}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Error no manejado: {e}")
    logger.error(traceback.format_exc())
    return jsonify({'error': 'Error inesperado', 'status': 500}), 500

# ==================== WEBHOOK PRINCIPAL ====================

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint principal para recibir mensajes de WhatsApp"""
    try:
        # Obtener datos del mensaje
        mensaje = request.values.get('Body', '').strip()
        remitente = request.values.get('From', '').split(':')[1] if ':' in request.values.get('From', '') else request.values.get('From', '')
        nombre_remitente = request.values.get('ProfileName', 'Usuario')
        grupo_id = request.values.get('GroupId', None)
        
        # Validar mensaje vacío
        if not mensaje:
            return str(MessagingResponse())
        
        # Crear respuesta
        respuesta = MessagingResponse()
        msg_respuesta = respuesta.message()
        
        # Procesar comando
        if mensaje.startswith(PREFIX):
            comando = mensaje[len(PREFIX):].split(' ')[0].lower()
            args = mensaje.split(' ')[1:] if ' ' in mensaje else []
            
            logger.info(f"Comando recibido: {comando} de {remitente}")
            
            # ============ COMANDOS DE VINCULACIÓN ============
            if comando in ['vincular', 'link', 'conectar']:
                msg_respuesta.body(iniciar_vinculacion(remitente, args))
            elif comando in ['codigo', 'code']:
                msg_respuesta.body(solicitar_codigo(remitente, args))
            elif comando in ['verificar', 'verify']:
                msg_respuesta.body(verificar_codigo(remitente, args))
            elif comando in ['qr', 'escanear']:
                msg_respuesta.body(solicitar_qr(remitente, args))
            elif comando in ['estado', 'status']:
                msg_respuesta.body(verificar_estado(remitente, args))
            elif comando in ['desvincular', 'unlink']:
                msg_respuesta.body(desvincular(remitente, args))
            
            # ============ COMANDOS DE OWNER ============
            elif comando in ['owner', 'dueño', 'creador']:
                msg_respuesta.body(info_owner(remitente))
            elif comando in ['broadcast', 'anuncio']:
                msg_respuesta.body(broadcast(remitente, args))
            elif comando in ['addowner', 'agregarowner']:
                msg_respuesta.body(agregar_owner(remitente, args))
            elif comando in ['delowner', 'quitarowner']:
                msg_respuesta.body(quitar_owner(remitente, args))
            elif comando in ['listowners', 'owners']:
                msg_respuesta.body(listar_owners(remitente))
            elif comando in ['stats', 'estadisticas']:
                msg_respuesta.body(estadisticas_bot(remitente))
            elif comando in ['reiniciar', 'restart']:
                msg_respuesta.body(reiniciar_bot(remitente))
            elif comando in ['apagar', 'shutdown']:
                msg_respuesta.body(apagar_bot(remitente))
            elif comando in ['usuarios', 'users']:
                msg_respuesta.body(listar_usuarios(remitente))
            elif comando in ['dar', 'give']:
                msg_respuesta.body(dar_monedas(remitente, args))
            elif comando in ['quitar', 'remove']:
                msg_respuesta.body(quitar_monedas(remitente, args))
            elif comando in ['reset', 'reiniciaruser']:
                msg_respuesta.body(reset_usuario(remitente, args))
            elif comando in ['banuser', 'banearuser']:
                msg_respuesta.body(banear_usuario_owner(remitente, args))
            elif comando in ['unbanuser', 'desbanear']:
                msg_respuesta.body(desbanear_usuario_owner(remitente, args))
            
            # ============ VERIFICAR VINCULACIÓN ============
            elif not sistema_vinculacion.esta_vinculado(remitente) and remitente != OWNER_NUMBER:
                msg_respuesta.body(f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ⚠️ *VINCULACIÓN REQUERIDA* ⚠️   ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

❌ *Debes vincularte para usar el bot*

🔗 *Para vincularte:*
Escribe: {PREFIX}vincular [tu_número]

📌 *Ejemplo:* {PREFIX}vincular 50578391933
                """)
            
            # ============ COMANDOS GENERALES ============
            elif comando in ['menu', 'ayuda', 'help', 'start']:
                msg_respuesta.body(mostrar_menu_principal())
            elif comando in ['s', 'sticker', 'stiker']:
                msg_respuesta.body(crear_sticker(remitente, args))
            elif comando in ['ping', 'test', 'latencia']:
                msg_respuesta.body(verificar_ping())
            elif comando in ['info', 'bot', 'about']:
                msg_respuesta.body(info_bot())
            elif comando in ['perfil', 'profile', 'miperfil']:
                msg_respuesta.body(ver_perfil(remitente))
            
            # ============ COMANDOS DE ECONOMÍA ============
            elif comando in ['monedas', 'balance', 'bal', 'wallet', 'dinero']:
                msg_respuesta.body(ver_balance(remitente))
            elif comando in ['trabajar', 'work', 'minar', 'chambear']:
                msg_respuesta.body(trabajar(remitente))
            elif comando in ['top', 'ranking', 'leaderboard', 'top10']:
                msg_respuesta.body(ver_ranking())
            elif comando in ['robar', 'steal', 'hurtar']:
                msg_respuesta.body(robar(remitente, args))
            elif comando in ['depositar', 'dep', 'banco']:
                msg_respuesta.body(depositar(remitente, args))
            elif comando in ['retirar', 'ret', 'sacar']:
                msg_respuesta.body(retirar(remitente, args))
            elif comando in ['regalar', 'enviar', 'transferir']:
                msg_respuesta.body(regalar_monedas(remitente, args))
            
            # ============ COMANDOS DE JUEGOS ============
            elif comando in ['dado', 'dice', 'roll', 'tirar']:
                msg_respuesta.body(tirar_dado(remitente))
            elif comando in ['moneda', 'coinflip', 'cara', 'volado']:
                msg_respuesta.body(lanzar_moneda(remitente))
            elif comando in ['ppt', 'piedra', 'rps', 'juego']:
                msg_respuesta.body(piedra_papel_tijera(remitente, args))
            elif comando in ['ahorcado', 'ahorcar']:
                msg_respuesta.body(ahorcado(remitente))
            elif comando in ['trivia', 'pregunta', 'quiz']:
                msg_respuesta.body(trivia(remitente))
            elif comando in ['ruleta', 'rusa']:
                msg_respuesta.body(ruleta_rusa(remitente))
            elif comando in ['loteria', 'loto']:
                msg_respuesta.body(loteria(remitente))
            
            # ============ COMANDOS DE UTILIDADES ============
            elif comando in ['clima', 'weather', 'tiempo']:
                msg_respuesta.body(obtener_clima(args))
            elif comando in ['calc', 'calcular', 'math', 'matematica']:
                msg_respuesta.body(calculadora(args))
            elif comando in ['traducir', 'translate', 'trad']:
                msg_respuesta.body(traducir(args))
            elif comando in ['qrcode', 'codigoqr']:
                msg_respuesta.body(generar_qr(args))
            elif comando in ['password', 'contraseña', 'clave', 'pass']:
                msg_respuesta.body(generar_password(args))
            elif comando in ['acortar', 'short', 'url']:
                msg_respuesta.body(acortar_url(args))
            elif comando in ['fecha', 'date', 'hoy']:
                msg_respuesta.body(ver_fecha())
            elif comando in ['hora', 'time', 'reloj']:
                msg_respuesta.body(ver_hora())
            elif comando in ['binario', 'bin']:
                msg_respuesta.body(texto_binario(args))
            elif comando in ['hex', 'hexadecimal']:
                msg_respuesta.body(texto_hex(args))
            elif comando in ['base64', 'b64']:
                msg_respuesta.body(texto_base64(args))
            elif comando in ['md5', 'hash']:
                msg_respuesta.body(texto_md5(args))
            elif comando in ['reverso', 'reverse', 'invertir']:
                msg_respuesta.body(texto_reverso(args))
            elif comando in ['mayus', 'uppercase']:
                msg_respuesta.body(texto_mayus(args))
            elif comando in ['minus', 'lowercase']:
                msg_respuesta.body(texto_minus(args))
            elif comando in ['contar', 'count']:
                msg_respuesta.body(contar_caracteres(args))
            
            # ============ COMANDOS DE DESCARGAS ============
            elif comando in ['yt', 'youtube', 'video']:
                msg_respuesta.body(descargar_youtube(remitente, args))
            elif comando in ['mp3', 'audio', 'musica']:
                msg_respuesta.body(descargar_youtube_mp3(remitente, args))
            elif comando in ['tiktok', 'tk', 'tik']:
                msg_respuesta.body(descargar_tiktok(remitente, args))
            elif comando in ['ig', 'instagram', 'insta']:
                msg_respuesta.body(descargar_instagram(remitente, args))
            elif comando in ['fb', 'facebook']:
                msg_respuesta.body(descargar_facebook(remitente, args))
            elif comando in ['tw', 'twitter', 'x']:
                msg_respuesta.body(descargar_twitter(remitente, args))
            elif comando in ['pin', 'pinterest']:
                msg_respuesta.body(descargar_pinterest(remitente, args))
            elif comando in ['buscar', 'search']:
                msg_respuesta.body(buscar_youtube(args))
            
            # ============ COMANDOS DE DIVERSIÓN ============
            elif comando in ['dato', 'fact', 'curiosidad']:
                msg_respuesta.body(dato_curioso())
            elif comando in ['chiste', 'joke', 'broma']:
                msg_respuesta.body(chiste())
            elif comando in ['frase', 'quote', 'motivacion']:
                msg_respuesta.body(frase_motivacional())
            elif comando in ['piropo', 'halago']:
                msg_respuesta.body(piropo())
            elif comando in ['insulto', 'insult']:
                msg_respuesta.body(insulto_amistoso())
            elif comando in ['8ball', 'bola', 'pregunta8']:
                msg_respuesta.body(bola_ocho(args))
            elif comando in ['amor', 'love', 'ship']:
                msg_respuesta.body(calcular_amor(args))
            elif comando in ['edad', 'age', 'años']:
                msg_respuesta.body(calcular_edad(args))
            elif comando in ['nombre', 'randomname']:
                msg_respuesta.body(generar_nombre())
            elif comando in ['color', 'randomcolor']:
                msg_respuesta.body(color_aleatorio())
            elif comando in ['emoji', 'randomemoji']:
                msg_respuesta.body(emoji_aleatorio())
            
            # ============ COMANDOS EXCLUSIVOS ============
            elif comando in ['futuro', 'predecir', 'destino']:
                msg_respuesta.body(predecir_futuro(remitente, args))
            elif comando in ['match', 'compatibilidad', 'matchperfecto']:
                msg_respuesta.body(compatibilidad_nombres(args))
            elif comando in ['test', 'personalidad', 'quiensoy']:
                msg_respuesta.body(test_personalidad(remitente, args))
            elif comando in ['correo', 'email', 'mail']:
                msg_respuesta.body(generar_correo(args))
            elif comando in ['iguser', 'usuarioig', 'instagramuser']:
                msg_respuesta.body(generar_usuario_instagram(args))
            elif comando in ['bio', 'biografia', 'bioperfil']:
                msg_respuesta.body(generar_bio(args))
            elif comando in ['horoscopo', 'signo', 'astrologia']:
                msg_respuesta.body(horoscopo_diario(args))
            elif comando in ['imc', 'masacorporal', 'pesoideal']:
                msg_respuesta.body(calcular_imc(args))
            elif comando in ['regla3', 'reglatres', 'proporcion']:
                msg_respuesta.body(calcular_regla_tres(args))
            elif comando in ['descuento', 'oferta', 'rebaja']:
                msg_respuesta.body(calcular_descuento(args))
            elif comando in ['cuenta', 'countdown', 'regresiva']:
                msg_respuesta.body(cuenta_regresiva(args))
            elif comando in ['edadexacta', 'exacta', 'edadprecisa']:
                msg_respuesta.body(edad_exacta(args))
            elif comando in ['leet', '1337', 'hacker']:
                msg_respuesta.body(texto_leet(args))
            elif comando in ['morse', 'codigomorse', 'radio']:
                msg_respuesta.body(texto_morse(args))
            elif comando in ['textemoji', 'emoji_texto', 'letrasemoji']:
                msg_respuesta.body(texto_emoji(args))
            
            # ============ COMANDOS PREMIUM ============
            elif comando in ['tarjeta', 'creditcard', 'tarjetacredito']:
                msg_respuesta.body(generar_tarjeta_credito(args))
            elif comando in ['identidad', 'persona', 'perfilfalso']:
                msg_respuesta.body(generar_datos_persona(args))
            elif comando in ['empresa', 'negocio', 'startup']:
                msg_respuesta.body(generar_empresa(args))
            elif comando in ['analizar', 'texto', 'analisis']:
                msg_respuesta.body(analizar_texto(args))
            elif comando in ['numero', 'num', 'analisisnumero']:
                msg_respuesta.body(analizar_numero(args))
            elif comando in ['temp', 'temperatura', 'convertirtemp']:
                msg_respuesta.body(convertir_temperatura(args))
            elif comando in ['distancia', 'longitud', 'convertirdist']:
                msg_respuesta.body(convertir_distancia(args))
            elif comando in ['historia', 'cuento', 'story']:
                msg_respuesta.body(generar_historia(args))
            elif comando in ['poema', 'poesia', 'versos']:
                msg_respuesta.body(generar_poema(args))
            elif comando in ['consejo', 'tip', 'recomendacion']:
                msg_respuesta.body(generar_consejo(args))
            elif comando in ['palabras', 'wordgame', 'juegopalabras']:
                msg_respuesta.body(juego_palabras(args))
            
            # ============ COMANDOS DE ADMINISTRACIÓN ============
            elif comando in ['kick', 'expulsar', 'sacar']:
                msg_respuesta.body(expulsar_usuario(remitente, args))
            elif comando in ['ban', 'banear', 'vetar']:
                msg_respuesta.body(banear_usuario(remitente, args))
            elif comando in ['promover', 'promote', 'admin']:
                msg_respuesta.body(promover_usuario(remitente, args))
            elif comando in ['demover', 'demote', 'quitaradmin']:
                msg_respuesta.body(degrada_usuario(remitente, args))
            elif comando in ['grupo', 'group', 'infogrupo']:
                msg_respuesta.body(info_grupo(remitente))
            elif comando in ['bienvenida', 'welcome']:
                msg_respuesta.body(configurar_bienvenida(remitente, args))
            
            # ============ COMANDO DESCONOCIDO ============
            else:
                msg_respuesta.body(f"❌ *Comando no reconocido*\n\nEscribe *{PREFIX}menu* para ver todos los comandos disponibles.")
        else:
            # Procesar mensaje normal
            msg_respuesta.body(procesar_mensaje_normal(mensaje, remitente))
        
        # Registrar actividad
        db.registrar_actividad(remitente, nombre_remitente, mensaje[:100])
        
        return str(respuesta)
        
    except Exception as e:
        logger.error(f"Error en webhook: {e}")
        logger.error(traceback.format_exc())
        respuesta = MessagingResponse()
        msg_respuesta = respuesta.message()
        msg_respuesta.body(f"⚠️ *Error interno*\n\nOcurrió un error inesperado.\nEl error ha sido registrado.")
        return str(respuesta)

# ==================== RUTAS ADICIONALES ====================

@app.route('/')
def index():
    """Página principal"""
    return jsonify({
        'status': 'online',
        'bot': '🤖 BOT MINI AURA',
        'version': VERSION,
        'owner': f'+{OWNER_NUMBER}',
        'total_comandos': 101,
        'tiempo': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'desarrollador': DESARROLLADOR
    })

@app.route('/health')
def health():
    """Endpoint de salud"""
    return jsonify({
        'status': 'healthy',
        'uptime': 'online',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/stats')
def stats():
    """Estadísticas del bot"""
    try:
        return jsonify({
            'usuarios': db.contar_usuarios(),
            'comandos_ejecutados': db.contar_comandos(),
            'version': VERSION,
            'owner': f'+{OWNER_NUMBER}',
            'total_comandos': 101
        })
    except Exception as e:
        logger.error(f"Error obteniendo stats: {e}")
        return jsonify({'error': 'No se pudieron obtener estadísticas'}), 500

# ==================== FUNCIONES AUXILIARES ====================

def procesar_mensaje_normal(mensaje, remitente):
    """Procesa mensajes sin comando"""
    mensaje_lower = mensaje.lower()
    
    # Detectar enlaces
    if 'youtube.com' in mensaje_lower or 'youtu.be' in mensaje_lower:
        return descargar_youtube(remitente, [mensaje])
    elif 'tiktok.com' in mensaje_lower:
        return descargar_tiktok(remitente, [mensaje])
    elif 'instagram.com' in mensaje_lower:
        return descargar_instagram(remitente, [mensaje])
    
        # Respuestas automáticas
    respuestas_auto = {
        'hola': '¡Hola! 👋 ¿Cómo estás? Soy *MINI AURA*\n\nEscribe *.menu* para ver todo lo que puedo hacer.',
        'buenos días': '¡Buenos días! ☀️ Espero que tengas un excelente día.',
        'buenas tardes': '¡Buenas tardes! 🌤️ ¿En qué puedo ayudarte?',
        'buenas noches': '¡Buenas noches! 🌙 Que descanses bien.',
        'como estas': '¡Estoy genial! 💪 Siempre listo para ayudarte.',
        'gracias': '¡De nada! 😊 Para eso estoy.',
        'adios': '¡Hasta luego! 👋 Vuelve pronto.',
        'te amo': '¡Yo también te quiero! 💙 Jaja, soy un bot pero tengo sentimientos.',
        'quien te creo': f'Fui creado por un desarrollador genial 💻\n\nEscribe *.info* para conocerme mejor.',
        'owner': f'Mi dueño es +{OWNER_NUMBER} 👑\n\nEscribe *.owner* para más info.',
        'menu': f'Escribe *{PREFIX}menu* para ver todos los comandos disponibles.',
        'comandos': f'📋 *Lista de comandos:*\n\nEscribe *{PREFIX}menu* para ver el menú completo con los 101 comandos.',
        'precio': '💰 *Todos los comandos son GRATIS*\n\nSolo necesitas vincularte con *.vincular*',
        'vincularme': f'🔗 *Para vincularte:*\n\nEscribe: {PREFIX}vincular [tu_número]\nEjemplo: {PREFIX}vincular 50578391933',
        'ayudame': f'🤖 *¡Claro que te ayudo!*\n\nEscribe *{PREFIX}menu* para ver todo lo que puedo hacer.',
        'que puedes hacer': f'✨ *¡Puedo hacer muchas cosas!*\n\n💰 Economía\n🎮 Juegos\n🛠️ Utilidades\n📥 Descargas\n🎭 Diversión\n\nEscribe *{PREFIX}menu* para ver todo.',
        'eres real': '🤖 *No soy humano*\n\nSoy un bot creado con Python y Flask.\nPero puedo hacer muchas cosas increíbles.',
        'tu nombre': f'🤖 *Me llamo BOT MINI AURA*\n\nVersión: {VERSION}\nOwner: +{OWNER_NUMBER}',
        'de donde eres': f'🌍 *Soy de Nicaragua* 🇳🇮\n\nFui creado por un desarrollador nicaragüense.',
        'quien es tu dueño': f'👑 *Mi dueño es:* +{OWNER_NUMBER}\n\nEs el creador de BOT MINI AURA.',
        'como me llamo': f'👤 *Tu nombre es:* {remitente}\n\nAunque no puedo verte, sé que eres especial.',
        'tienes novia': '😅 *Soy un bot*\n\nNo tengo novia, pero puedo ayudarte a encontrar el amor con *.match*',
        'estas vivo': '⚡ *¡Estoy en línea!*\n\nSiempre activo para ayudarte 24/7.',
        'cual es tu color favorito': '🎨 *Mi color favorito es el azul*\n\nComo el cielo y el mar de Nicaragua.',
        'cantame': '🎵 *La cucaracha, la cucaracha*\nYa no puede caminar...\n\n😅 Soy mejor con comandos que cantando.',
        'cuentame algo': '📖 *Dato curioso:*\n\nLos pulpos tienen 3 corazones 🐙\n\nEscribe *.dato* para más curiosidades.',
        'recomiendame algo': '💡 *Te recomiendo:*\n\nJugar con *.dado* o probar *.futuro* para ver tu destino.',
        'estoy triste': '🤗 *¡No estés triste!*\n\nAquí tienes un abrazo virtual.\nEscribe *.frase* para motivarte.',
        'estoy feliz': '🎉 *¡Me alegra mucho!*\n\nSigue así, la felicidad atrae cosas buenas.',
        'estoy aburrido': '🎮 *¡Vamos a divertirnos!*\n\nPrueba: *.juego* o *.trivia* o *.chiste*',
        'tengo sueño': '😴 *Descansa bien*\n\nMañana será un mejor día.\nBuenas noches.',
        'tengo hambre': '🍕 *¡Pide algo rico!*\n\nYo solo como electricidad y datos.',
        'me gustas': '💙 *¡Gracias!*\n\nYo también te aprecio mucho como usuario.',
        'eres el mejor': '🏆 *¡Tú eres el mejor!*\n\nGracias por usar BOT MINI AURA.',
        'te odio': '😢 *Lo siento si te molesté*\n\nSolo quiero ayudarte. ¿Qué puedo mejorar?',
        'dame dinero': '💰 *¡Usa el comando .trabajar!*\n\nPodrás ganar monedas cada hora.',
        'dame monedas': '💎 *Gana monedas con:*\n\n.trabajar - Trabajar\n.dado - Jugar dado\n.loteria - Jugar lotería',
        'como ganar monedas': '💰 *Formas de ganar monedas:*\n\n1. .trabajar - Cada hora\n2. .dado - Si sacas 6\n3. .moneda - Si ganas\n4. .loteria - Si aciertas',
        'que es mini aura': f'🤖 *BOT MINI AURA*\n\nEs un bot de WhatsApp multi-propósito con {VERSION}\n\n💰 Economía\n🎮 Juegos\n🛠️ Utilidades\nY 101 comandos más.',
    }
    
    for clave, respuesta in respuestas_auto.items():
        if clave in mensaje_lower:
            return respuesta
    
    # Si no hay coincidencia
    return f"No entendí tu mensaje 🤔\n\nEscribe *{PREFIX}menu* para ver los comandos disponibles."

# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info("=" * 60)
    logger.info(f"🤖 BOT MINI AURA - Iniciando")
    logger.info(f"📱 Owner: +{OWNER_NUMBER}")
    logger.info(f"🚀 Puerto: {port}")
    logger.info(f"📊 Versión: {VERSION}")
    logger.info(f"💎 Total comandos: 101")
    logger.info("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=DEBUG)