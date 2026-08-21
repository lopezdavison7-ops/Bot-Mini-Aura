def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede resetear usuarios*"
    if not args:
        return "❌ *Uso:* .reset [número]"
    return f"🔄 *Usuario reseteado:* +{args[0]}"