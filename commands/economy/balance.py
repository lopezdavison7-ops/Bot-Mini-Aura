# Base de datos en memoria (se pierde al reiniciar)
# Para persistencia real, conectar a SQLite
users = {}

def ejecutar(mencion=None, usuario=None):
    if usuario not in users:
        users[usuario] = 100  # monedas iniciales
    return f"💰 *{mencion}*\n\nMonedas: *{users[usuario]}*"