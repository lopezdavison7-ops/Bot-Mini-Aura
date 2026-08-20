import random

def ejecutar(args=None, mencion=None, usuario=None):
    if not args:
        return "❌ *Uso:* .robar [número]"
    objetivo = args[0]
    if objetivo not in users:
        return "❌ Ese usuario no tiene cuenta."
    if users[objetivo] < 100:
        return "❌ No tiene suficientes monedas."
    if random.random() < 0.3:
        cantidad = random.randint(10, users[objetivo] // 2)
        users[objetivo] -= cantidad
        users[usuario] = users.get(usuario, 100) + cantidad
        return f"🦹 *{mencion}*\n\n¡Robaste {cantidad} monedas a {objetivo}!"
    else:
        multa = random.randint(20, 50)
        users[usuario] = users.get(usuario, 100) - multa
        return f"👮 *{mencion}*\n\nFallaste y pagaste {multa} monedas de multa."