import random

def ejecutar(mencion=None):
    datos = [
        "🐙 *Dato curioso:* Los pulpos tienen 3 corazones",
        "🍯 *Dato curioso:* La miel nunca caduca",
        "🦩 *Dato curioso:* Los flamencos son rosados por su comida",
        "🌍 *Dato curioso:* Un día en Venus dura más que un año",
        "🐝 *Dato curioso:* Las abejas pueden reconocer rostros humanos",
        "🌙 *Dato curioso:* La Luna se aleja de la Tierra 3.8 cm cada año"
    ]
    return random.choice(datos)