def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede dar monedas*"
    if len(args) < 2:
        return "❌ *Uso:* .dar [número] [cantidad]"
    return f"💰 *Diste {args[1]} monedas a +{args[0]}*"