def ejecutar(args=None, mencion=None):
    if not args:
        return "⬇️ *Uso:* .minus [texto]"
    return f"⬇️ *Minúsculas:* {' '.join(args).lower()}"