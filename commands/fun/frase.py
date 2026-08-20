import random

def ejecutar(mencion=None):
    frases = [
        "🌟 *Frase:* El éxito es la suma de pequeños esfuerzos",
        "💪 *Frase:* Cree en ti y todo será posible",
        "🚀 *Frase:* Tu única limitación es tu mente",
        "⭐ *Frase:* El futuro pertenece a quienes creen en sus sueños",
        "🔥 *Frase:* La disciplina es el puente entre metas y logros"
    ]
    return random.choice(frases)