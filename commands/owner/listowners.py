owners = ["50578391933"]

def ejecutar(mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede ver la lista*"
    texto = "👑 *LISTA DE OWNERS*\n\n"
    for i, owner in enumerate(owners, 1):
        texto += f"{i}️⃣ +{owner}\n"
    return texto