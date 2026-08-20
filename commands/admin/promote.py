def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede usar este comando*"
    if not args:
        return "❌ *Uso:* .promover [número]"
    return f"⬆️ *Usuario promovido a admin:* +{args[0]}"