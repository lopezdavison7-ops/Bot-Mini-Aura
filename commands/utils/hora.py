from datetime import datetime

def ejecutar(mencion=None):
    return f"⏰ *Hora:* {datetime.now().strftime('%H:%M:%S')}"