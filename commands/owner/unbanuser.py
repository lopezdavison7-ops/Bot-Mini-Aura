banned = []

def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede desbanear usuarios*"
    if not args:
        return "❌ *Uso:* .unbanuser [número]"
    if args[0] in banned:
        banned.remove(args[0])
        return f"✅ *Usuario desbaneado:* +{args[0]}"
    return "❌ No está baneado"