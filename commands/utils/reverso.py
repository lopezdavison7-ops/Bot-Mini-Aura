def ejecutar(args=None, mencion=None):
    if not args:
        return "🔄 *Uso:* .reverso [texto]"
    return f"🔄 *Invertido:* {' '.join(args)[::-1]}"