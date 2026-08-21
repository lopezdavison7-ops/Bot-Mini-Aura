def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede enviar anuncios*"
    if not args:
        return "❌ *Uso:* .broadcast [mensaje]"
    return f"📢 *ANUNCIO:* {' '.join(args)}"