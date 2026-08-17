# -*- coding: utf-8 -*-

"""
🔗 Sistema de Vinculación para BOT MINI AURA
Version: 2.0.0
"""

import random
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SistemaVinculacion:
    def __init__(self):
        self.archivo_sesiones = Path('src/data/json/sesiones_vinculacion.json')
        self.archivo_pendientes = Path('src/data/json/pendientes_vinculacion.json')
        self.archivo_sesiones.parent.mkdir(parents=True, exist_ok=True)
        self.sesiones = self.cargar_json(self.archivo_sesiones)
        self.pendientes = self.cargar_json(self.archivo_pendientes)
        self.codigos_pendientes = {}
    
    def cargar_json(self, archivo):
        """Cargar archivo JSON"""
        try:
            if archivo.exists():
                with open(archivo, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error cargando JSON: {e}")
            return {}
    
    def guardar_json(self, archivo, datos):
        """Guardar archivo JSON"""
        try:
            with open(archivo, 'w') as f:
                json.dump(datos, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error guardando JSON: {e}")
            return False
    
    def guardar_numero_pendiente(self, usuario, numero):
        """Guardar número pendiente de vinculación"""
        try:
            self.pendientes[usuario] = {
                'numero': numero,
                'fecha': datetime.now().isoformat()
            }
            self.guardar_json(self.archivo_pendientes, self.pendientes)
            return True
        except Exception as e:
            logger.error(f"Error guardando pendiente: {e}")
            return False
    
    def obtener_numero_pendiente(self, usuario):
        """Obtener número pendiente"""
        try:
            if usuario in self.pendientes:
                datos = self.pendientes[usuario]
                # Verificar expiración (5 minutos)
                fecha = datetime.fromisoformat(datos['fecha'])
                if datetime.now() - fecha < timedelta(minutes=5):
                    return datos['numero']
                else:
                    del self.pendientes[usuario]
                    self.guardar_json(self.archivo_pendientes, self.pendientes)
            return None
        except Exception as e:
            logger.error(f"Error obteniendo pendiente: {e}")
            return None
    
    def generar_codigo(self, numero_telefono):
        """Generar código de 8 dígitos"""
        try:
            codigo = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            
            self.codigos_pendientes[numero_telefono] = {
                'codigo': codigo,
                'fecha_creacion': datetime.now().isoformat(),
                'intentos': 0,
                'valido': True
            }
            
            return codigo
        except Exception as e:
            logger.error(f"Error generando código: {e}")
            return None
    
    def verificar_codigo(self, numero_telefono, codigo_ingresado):
        """Verificar código de vinculación"""
        try:
            if numero_telefono not in self.codigos_pendientes:
                return {
                    'valido': False,
                    'mensaje': '❌ *No hay código pendiente*\n\nPrimero solicita un código con ' + PREFIX + 'codigo'
                }
            
            datos_codigo = self.codigos_pendientes[numero_telefono]
            
            # Verificar expiración
            fecha_creacion = datetime.fromisoformat(datos_codigo['fecha_creacion'])
            if datetime.now() - fecha_creacion > timedelta(minutes=5):
                del self.codigos_pendientes[numero_telefono]
                return {
                    'valido': False,
                    'mensaje': '⏰ *Código expirado*\n\nEl código ha expirado. Solicita uno nuevo.'
                }
            
            # Verificar intentos
            if datos_codigo['intentos'] >= 3:
                del self.codigos_pendientes[numero_telefono]
                return {
                    'valido': False,
                    'mensaje': '❌ *Demasiados intentos fallidos*\n\nSolicita un nuevo código.'
                }
            
            # Verificar código
            if codigo_ingresado == datos_codigo['codigo']:
                # Vincular exitosamente
                self.sesiones[numero_telefono] = {
                    'vinculado': True,
                    'fecha_vinculacion': datetime.now().isoformat(),
                    'metodo': 'codigo'
                }
                self.guardar_json(self.archivo_sesiones, self.sesiones)
                
                # Limpiar pendiente
                del self.codigos_pendientes[numero_telefono]
                
                return {
                    'valido': True,
                    'mensaje': f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃ ✅ *¡VINCULACIÓN EXITOSA!* ✅ ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🎉 *¡Tu número ha sido vinculado!*

📱 *Número:* {numero_telefono}
🔗 *Método:* Código de 8 dígitos
📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y %H:%M')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 *BOT MINI AURA* está listo
Escribe *.menu* para comenzar
                    """
                }
            else:
                # Incrementar intentos
                self.codigos_pendientes[numero_telefono]['intentos'] += 1
                intentos_restantes = 3 - self.codigos_pendientes[numero_telefono]['intentos']
                
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
    
    def generar_qr(self, numero_telefono):
        """Generar QR para vinculación"""
        try:
            qr_data = {
                'numero': numero_telefono,
                'qr_code': f'MINI-AURA-{random.randint(100000, 999999)}',
                'fecha': datetime.now().isoformat()
            }
            
            # Simular vinculación exitosa
            self.sesiones[numero_telefono] = {
                'vinculado': True,
                'fecha_vinculacion': datetime.now().isoformat(),
                'metodo': 'qr'
            }
            self.guardar_json(self.archivo_sesiones, self.sesiones)
            
            return {
                'valido': True,
                'qr': qr_data['qr_code'],
                'mensaje': f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃ ✅ *¡VINCULACIÓN POR QR!* ✅ ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🎉 *¡Tu número ha sido vinculado!*

📱 *Número:* {numero_telefono}
🔗 *Método:* Código QR
📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y %H:%M')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 *BOT MINI AURA* está listo
Escribe *.menu* para comenzar
                """
            }
        except Exception as e:
            logger.error(f"Error generando QR: {e}")
            return {
                'valido': False,
                'mensaje': '⚠️ *Error generando QR*\n\nIntenta con el código de 8 dígitos.'
            }
    
    def esta_vinculado(self, numero_telefono):
        """Verificar si un número está vinculado"""
        return numero_telefono in self.sesiones and self.sesiones[numero_telefono].get('vinculado', False)
    
    def desvincular(self, numero_telefono):
        """Desvincular un número"""
        if numero_telefono in self.sesiones:
            del self.sesiones[numero_telefono]
            self.guardar_json(self.archivo_sesiones, self.sesiones)
            return True
        return False
    
    def obtener_info_vinculacion(self, numero_telefono):
        """Obtener información de vinculación"""
        if numero_telefono in self.sesiones:
            return self.sesiones[numero_telefono]
        return None