import random

def ejecutar(mencion=None):
    predicciones = [
        "🔮 *Predicción:* Veo éxito en tu futuro",
        "🌟 *Predicción:* Algo bueno viene pronto",
        "💫 *Predicción:* Una sorpresa te espera",
        "💰 *Predicción:* El dinero llegará a tu vida",
        "💑 *Predicción:* El amor tocará tu puerta"
    ]
    return random.choice(predicciones)