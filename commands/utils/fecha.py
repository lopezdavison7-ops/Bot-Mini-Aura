from datetime import datetime

def ejecutar(mencion=None):
    return f"📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y')}"