import random
from datetime import datetime, timedelta

users = {}
last_work = {}

def ejecutar(mencion=None, usuario=None):
    if usuario in last_work:
        diff = datetime.now() - last_work[usuario]
        if diff < timedelta(hours=1):
            mins = int((timedelta(hours=1) - diff).seconds // 60)
            return f"⏰ *{mencion}*\n\nDebes esperar {mins} minutos para trabajar de nuevo."
    
    ganancia = random.randint(10, 50)
    users[usuario] = users.get(usuario, 100) + ganancia
    last_work[usuario] = datetime.now()
    return f"💼 *{mencion}*\n\nTrabajaste y ganaste *{ganancia}* monedas."