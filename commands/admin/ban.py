def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede usar este comando*"
    if not args:
        return "❌ *Uso:* .ban [número]"
    return f"🔨 *Usuario baneado:* +{args[0]}"