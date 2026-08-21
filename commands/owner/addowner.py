owners = ["50578391933"]

def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner principal puede agregar owners*"
    if not args:
        return "❌ *Uso:* .addowner [número]"
    if args[0] not in owners:
        owners.append(args[0])
        return f"✅ *Owner agregado:* +{args[0]}"
    return "❌ Ya es owner"