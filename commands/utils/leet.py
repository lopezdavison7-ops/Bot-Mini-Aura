def ejecutar(args=None, mencion=None):
    if not args:
        return "🔡 *Uso:* .leet [texto]"
    
    leet_dict = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    texto = ' '.join(args).lower()
    resultado = ''.join(leet_dict.get(c, c) for c in texto)
    return f"🔡 *Leet:* {resultado}"