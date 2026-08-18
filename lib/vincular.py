# -*- coding: utf-8 -*-

"""
🔗 Sistema de Vinculación para BOT MINI AURA
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
        self.archivo_vinculados = Path('data/vinculados.json')
        self.archivo_vinculados.parent.mkdir(parents=True, exist_ok=True)
        self.vinculados = self.cargar_vinculados()
        self.codigos_activos = {}
        
    def cargar_vinculados(self):
        """Cargar usuarios vinculados desde JSON"""
        try:
            if self.archivo_vinculados.exists():
                with open(self.archivo_vinculados, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            return set()
        except Exception as e:
            logger.error(f"Error cargando vinculados: {e}")
            return set()
    
    def guardar_vinculados(self):
        """Guardar usuarios vinculados en JSON"""
        try:
            with open(self.archivo_vinculados, 'w', encoding='utf-8') as f:
                json.dump(list(self.vinculados), f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error guardando vinculados: {e}")
            return False
    
    def generar_codigo(self, usuario):
        """Generar código de 8 dígitos"""
        try:
            codigo = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            
            self.codigos_activos[usuario] = {
                'codigo': codigo,
                'fecha_creacion': datetime.now(),
                'intentos': 0
            }
            
            logger.info(f"Código generado para {usuario}: {codigo}")
            return codigo
        except Exception as e:
            logger.error(f"Error generando código: {e}")
            return None
    
    def verificar_codigo(self, usuario, codigo_ingresado):
        """Verificar código de 8 dígitos"""
        try:
            if usuario not in self.codigos_activos:
                return {
                    'valido': False,
                    'mensaje': '❌ *No hay código pendiente*\n\nEscribe .codigo para recibir uno.'
                }
            
            datos = self.codigos_activos[usuario]
            
            # Verificar expiración (5 minutos)
            if datetime.now() - datos['fecha_creacion'] > timedelta(minutes=5):
                del self.codigos_activos[usuario]
                return {
                    'valido': False,
                    'mensaje': '⏰ *Código expirado*\n\nEscribe .codigo para recibir uno nuevo.'
                }
            
            # Verificar intentos máximos
            if datos['intentos'] >= 3:
                del self.codigos_activos[usuario]
                return {
                    'valido': False,
                    'mensaje': '❌ *Demasiados intentos*\n\nEscribe .codigo para recibir uno nuevo.'
                }
            
            # Verificar código
            if codigo_ingresado == datos['codigo']:
                # Vincular exitosamente
                self.vinculados.add(usuario)
                self.guardar_vinculados()
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
        """Verificar si un usuario está vinculado"""
        return usuario in self.vinculados
    
    def desvincular(self, usuario):
        """Desvincular un usuario"""
        try:
            if usuario in self.vinculados:
                self.vinculados.remove(usuario)
                self.guardar_vinculados()
                return True
            return False
        except Exception as e:
            logger.error(f"Error desvinculando: {e}")
            return False
    
    def obtener_total_vinculados(self):
        """Obtener total de usuarios vinculados"""
        return len(self.vinculados)