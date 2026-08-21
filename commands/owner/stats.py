import time

def ejecutar(mencion=None, usuario=None):
    if usuario != "50578391933":
        return "❌ *Solo el owner puede ver estadísticas*"
    return f"""
╭┈ ↷
│ ✐ *ESTADÍSTICAS DEL BOT*
│ 👥 Usuarios: 0
│ ⚡ Comandos ejecutados: 0
│ 📊 Versión: 4.0.0
│ ⏰ Tiempo activo: Online
╰─────────────────────────────────────
"""