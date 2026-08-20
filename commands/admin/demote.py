def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede usar este comando*"
    if not args:
        return "❌ *Uso:* .demover [número]"
    return f"⬇️ *Admin degradado:* +{args[0]}"