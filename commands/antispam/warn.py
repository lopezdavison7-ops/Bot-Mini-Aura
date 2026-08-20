warnings = {}

def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ Solo el owner puede advertir."
    if not args:
        return "❌ *Uso:* .warn [número]"
    objetivo = args[0]
    warnings[objetivo] = warnings.get(objetivo, 0) + 1
    return f"⚠️ *{mencion}*\n\nAdvertencia enviada a {objetivo}. Total: {warnings[objetivo]}"