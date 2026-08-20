def ejecutar(args=None, mencion=None):
    if not args:
        return "🧮 *Uso:* .calc [expresión]"
    try:
        return f"🧮 *Resultado:* {eval(' '.join(args))}"
    except:
        return "❌ Error en la operación"