warnings = {}

def ejecutar(mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ Solo el owner puede ver advertencias."
    if not warnings:
        return "📊 No hay advertencias."
    texto = "⚠️ *ADVERTENCIAS*\n\n"
    for user, cant in warnings.items():
        texto += f"├─ {user}: {cant}\n"
    return texto