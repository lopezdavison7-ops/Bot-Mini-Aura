def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede usar este comando*"
    if not args:
        return "❌ *Uso:* .kick [número]"
    return f"👢 *Usuario expulsado:* +{args[0]}"