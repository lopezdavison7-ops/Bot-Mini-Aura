antispam_activo = True

def ejecutar(args=None, mencion=None, usuario=None):
    global antispam_activo
    if usuario != "50578391933":
        return "❌ Solo el owner puede usar este comando."
    if not args:
        return f"🛡️ Anti-spam: {'activado' if antispam_activo else 'desactivado'}"
    opcion = args[0].lower()
    if opcion in ['on', 'activar']:
        antispam_activo = True
        return "✅ Anti-spam activado."
    elif opcion in ['off', 'desactivar']:
        antispam_activo = False
        return "❌ Anti-spam desactivado."
    return "❌ Opción inválida. Usa .antispam on/off"