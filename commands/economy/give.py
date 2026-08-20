users = {}

def ejecutar(args=None, mencion=None, usuario=None):
    if len(args) < 2 or not args[1].isdigit():
        return "❌ *Uso:* .regalar [número] [cantidad]"
    objetivo = args[0]
    cantidad = int(args[1])
    if users.get(usuario, 100) < cantidad:
        return "❌ No tienes suficientes monedas."
    users[usuario] -= cantidad
    users[objetivo] = users.get(objetivo, 100) + cantidad
    return f"💸 *{mencion}*\n\nTransferiste {cantidad} monedas a {objetivo}."