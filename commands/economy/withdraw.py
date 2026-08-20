users = {}
bank = {}

def ejecutar(args=None, mencion=None, usuario=None):
    if not args or not args[0].isdigit():
        return "❌ *Uso:* .retirar [cantidad]"
    cantidad = int(args[0])
    if bank.get(usuario, 0) < cantidad:
        return "❌ No tienes suficientes monedas en el banco."
    bank[usuario] -= cantidad
    users[usuario] = users.get(usuario, 100) + cantidad
    return f"🏦 *{mencion}*\n\nRetiraste {cantidad} monedas. Balance: {users[usuario]}"