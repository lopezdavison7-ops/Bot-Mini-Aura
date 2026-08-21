banned = []

def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede banear usuarios*"
    if not args:
        return "❌ *Uso:* .banuser [número]"
    banned.append(args[0])
    return f"🔨 *Usuario baneado:* +{args[0]}"