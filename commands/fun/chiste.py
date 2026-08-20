import random

def ejecutar(mencion=None):
    chistes = [
        "😂 ¿Por qué los pájaros no usan Facebook?\nPorque ya tienen Twitter",
        "😂 ¿Qué le dice un semáforo a otro?\nNo me mires, me estoy cambiando",
        "😂 ¿Por qué el libro de matemáticas estaba triste?\nPorque tenía muchos problemas",
        "😂 ¿Qué hace una abeja en el gimnasio?\n¡Zum-ba!",
        "😂 ¿Por qué los esqueletos no pelean?\nPorque no tienen agallas"
    ]
    return random.choice(chistes)