def ejecutar(args=None, mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede configurar bienvenida*"
    if not args:
        return "❌ *Uso:* .bienvenida [mensaje]"
    return f"✅ *Bienvenida configurada:* {' '.join(args)}"