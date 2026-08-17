# -*- coding: utf-8 -*-

"""
🔗 Sistema de Vinculación REAL para BOT MINI AURA
Versión: 3.0.0
"""

import random
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SistemaVinculacion:
    def __init__(self):
        self.archivo_vinculados = Path('src/data/json/vinculados.json')
        self.archivo_codigos = Path('src/data/json/codigos_pendientes.json')
        self.archivo_vinculados.parent.mkdir(parents=True, exist_ok=True)
        
        self.vinculados = self.cargar_json(self.archivo_vinculados)
        self.codigos = self.cargar_json(self.archivo_codigos)
        self.codigos_activos = {}
        
    def cargar_json(self, archivo):
        """Cargar archivo JSON"""
        try:
            if archivo.exists():
                with open(archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error cargando JSON: {e}")
            return {}
    
    def guardar_json(self, archivo, datos):
        """Guardar archivo JSON"""
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error guardando JSON: {e}")
            return False
    
    def guardar_numero_pendiente(self, usuario, numero):
        """Guardar número pendiente"""
        try:
            self.vinculados[usuario] = {
                'numero': numero,
                'estado': 'pendiente',
                'fecha': datetime.now().isoformat()
            }
            self.guardar_json(self.archivo_vinculados, self.vinculados)
            return True
        except Exception as e:
            logger.error(f"Error guardando pendiente: {e}")
            return False
    
    def generar_codigo(self, usuario, codigo=None):
        """Generar o guardar código de 8 dígitos"""
        try:
            if not codigo:
                codigo = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            
            self.codigos_activos[usuario] = {
                'codigo': codigo,
                'fecha_creacion': datetime.now().isoformat(),
                'intentos': 0
            }
            
            # Guardar en archivo
            self.codigos[usuario] = self.codigos_activos[usuario]
            self.guardar_json(self.archivo_codigos, self.codigos)
            
            return codigo
        except Exception as e:
            logger.error(f"Error generando código: {e}")
            return None
    
    def verificar_codigo(self, usuario, codigo_ingresado):
        """Verificar código de 8 dígitos"""
        try:
            # Verificar si hay código pendiente
            if usuario not in self.codigos_activos:
                return {
                    'valido': False,
                    'mensaje': '❌ *No hay código pendiente*\n\nEscribe .codigo para recibir uno.'
                }
            
            datos_codigo = self.codigos_activos[usuario]
            
            # Verificar expiración (5 minutos)
            fecha_creacion = datetime.fromisoformat(datos_codigo['fecha_creacion'])
            if datetime.now() - fecha_creacion > timedelta(minutes=5):
                del self.codigos_activos[usuario]
                return {
                    'valido': False,
                    'mensaje': '⏰ *Código expirado*\n\nEscribe .codigo para recibir uno nuevo.'
                }
            
            # Verificar intentos
            if datos_codigo['intentos'] >= 3:
                del self.codigos_activos[usuario]
                return {
                    'valido': False,
                    'mensaje': '❌ *Demasiados intentos*\n\nEscribe .codigo para recibir uno nuevo.'
                }
            
            # Verificar código
            if codigo_ingresado == datos_codigo['codigo']:
                # Vincular exitosamente
                self.vinculados[usuario] = {
                    'numero': usuario,
                    'estado': 'vinculado',
                    'fecha_vinculacion': datetime.now().isoformat()
                }
                self.guardar_json(self.archivo_vinculados, self.vinculados)
                
                # Limpiar código
                del self.codigos_activos[usuario]
                
                return {
                    'valido': True,
                    'mensaje': f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃ ✅ *¡VINCULACIÓN EXITOSA!* ✅ ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🎉 *¡Tu número ha sido vinculado!*

📱 *Número:* {usuario}
📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y %H:%M')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 *BOT MINI AURA* está listo
Escribe .menu para comenzar
                    """
                }
            else:
                # Incrementar intentos
                self.codigos_activos[usuario]['intentos'] += 1
                intentos_restantes = 3 - self.codigos_activos[usuario]['intentos']
                
                return {
                    'valido': False,
                    'mensaje': f"❌ *Código incorrecto*\n\nTe quedan {intentos_restantes} intentos."
                }
                
        except Exception as e:
            logger.error(f"Error verificando código: {e}")
            return {
                'valido': False,
                'mensaje': '⚠️ *Error interno*\n\nIntenta de nuevo.'
            }
    
    def esta_vinculado(self, usuario):
        """Verificar si está vinculado"""
        return usuario in self.vinculados and self.vinculados[usuario].get('estado') == 'vinculado'