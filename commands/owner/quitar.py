def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede quitar monedas*"
    if len(args) < 2:
        return "❌ *Uso:* .quitar [número] [cantidad]"
    return f"💸 *Quitaste {args[1]} monedas a +{args[0]}*"