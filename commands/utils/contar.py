def ejecutar(args=None, mencion=None):
    if not args:
        return "📊 *Uso:* .contar [texto]"
    return f"📊 *Caracteres:* {len(' '.join(args))}"