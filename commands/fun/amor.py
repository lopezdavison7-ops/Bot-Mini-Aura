import random

def ejecutar(args=None, mencion=None):
    if not args or len(args) < 2:
        return "❌ *Uso:* .amor nombre1 nombre2"
    return f"💑 *Compatibilidad*\n\n{args[0]} + {args[1]} = *{random.randint(50, 100)}%*"