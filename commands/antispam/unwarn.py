warnings = {}

def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ Solo el owner puede quitar advertencias."
    if not args:
        return "❌ *Uso:* .unwarn [número]"
    objetivo = args[0]
    if objetivo in warnings and warnings[objetivo] > 0:
        warnings[objetivo] -= 1
        return f"✅ Advertencia quitada a {objetivo}. Restantes: {warnings[objetivo]}"
    return "❌ No tiene advertencias."