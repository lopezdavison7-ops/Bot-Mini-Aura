users = {}
bank = {}

def ejecutar(args=None, mencion=None, usuario=None):
    if not args or not args[0].isdigit():
        return "❌ *Uso:* .depositar [cantidad]"
    cantidad = int(args[0])
    if users.get(usuario, 100) < cantidad:
        return "❌ No tienes suficientes monedas."
    users[usuario] = users.get(usuario, 100) - cantidad
    bank[usuario] = bank.get(usuario, 0) + cantidad
    return f"🏦 *{mencion}*\n\nDepositaste {cantidad} monedas. Banco: {bank[usuario]}"