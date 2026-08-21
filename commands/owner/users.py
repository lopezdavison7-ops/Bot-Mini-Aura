users_list = []

def ejecutar(mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede ver usuarios*"
    if not users_list:
        return "📊 *No hay usuarios registrados*"
    texto = "👥 *USUARIOS*\n\n"
    for user in users_list[:10]:
        texto += f"├─ {user}\n"
    return texto