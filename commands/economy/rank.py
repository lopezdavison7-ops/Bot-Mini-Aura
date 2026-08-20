def ejecutar(mencion=None, usuario=None):
    if not users:
        return "📊 *Ranking*\n\nAún no hay usuarios."
    sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)[:10]
    texto = "🏆 *TOP 10 RICOS*\n\n"
    medallas = ['🥇', '🥈', '🥉']
    for i, (user, monedas) in enumerate(sorted_users):
        medalla = medallas[i] if i < 3 else f"{i+1}️⃣"
        texto += f"{medalla} *{user}*: {monedas} monedas\n"
    return texto