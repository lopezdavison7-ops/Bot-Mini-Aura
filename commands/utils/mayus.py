def ejecutar(args=None, mencion=None):
    if not args:
        return "⬆️ *Uso:* .mayus [texto]"
    return f"⬆️ *Mayúsculas:* {' '.join(args).upper()}"