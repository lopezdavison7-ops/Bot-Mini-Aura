import random

def ejecutar(args=None, mencion=None):
    if not args:
        return "🔮 *Uso:* .8ball [pregunta]"
    
    respuestas = [
        "Sí ✅",
        "No ❌",
        "Quizás 🤔",
        "Definitivamente 💯",
        "No cuentes con ello",
        "Pregunta de nuevo más tarde"
    ]
    return random.choice(respuestas)