owners = ["50578391933"]

def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner principal puede quitar owners*"
    if not args:
        return "❌ *Uso:* .delowner [número]"
    if args[0] == "50578391933":
        return "❌ No puedes quitar al owner principal"
    if args[0] in owners:
        owners.remove(args[0])
        return f"✅ *Owner eliminado:* +{args[0]}"
    return "❌ No es owner"