import random

def ejecutar(args=None, mencion=None):
    if not args:
        return "✊ *Uso:* .ppt piedra/papel/tijera"
    
    opciones = ['piedra', 'papel', 'tijera']
    bot_opcion = random.choice(opciones)
    user_opcion = args[0].lower()
    
    if user_opcion not in opciones:
        return "❌ Opción inválida"
    
    if user_opcion == bot_opcion:
        return f"🤝 *Empate!*\n\nBot: {bot_opcion}\nTú: {user_opcion}"
    elif (user_opcion == 'piedra' and bot_opcion == 'tijera') or \
         (user_opcion == 'papel' and bot_opcion == 'piedra') or \
         (user_opcion == 'tijera' and bot_opcion == 'papel'):
        return f"🎉 *¡GANASTE!*\n\nBot: {bot_opcion}\nTú: {user_opcion}"
    else:
        return f"😢 *Perdiste*\n\nBot: {bot_opcion}\nTú: {user_opcion}"