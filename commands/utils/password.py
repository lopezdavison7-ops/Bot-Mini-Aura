import random
import string

def ejecutar(args=None, mencion=None):
    chars = string.ascii_letters + string.digits
    return f"🔑 *Contraseña:* `{''.join(random.choice(chars) for _ in range(12))}`"