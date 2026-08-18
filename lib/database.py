# -*- coding: utf-8 -*-

"""
🗄️ Base de Datos para BOT MINI AURA
Versión: 3.0.0
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db_path = Path('data/bot.db')
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize(self):
        """Inicializar base de datos con todas las tablas"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telefono TEXT UNIQUE NOT NULL,
                    nombre TEXT DEFAULT 'Usuario',
                    monedas INTEGER DEFAULT 100,
                    banco INTEGER DEFAULT 0,
                    nivel INTEGER DEFAULT 1,
                    exp INTEGER DEFAULT 0,
                    ultimo_trabajo DATETIME,
                    ultimo_robo DATETIME,
                    baneado BOOLEAN DEFAULT 0,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de actividad
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS actividad (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telefono TEXT,
                    nombre TEXT,
                    mensaje TEXT,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Base de datos inicializada correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando base de datos: {e}")
    
    def crear_usuario(self, telefono, nombre='Usuario'):
        """Crear nuevo usuario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO usuarios (telefono, nombre, monedas)
                VALUES (?, ?, ?)
            ''', (telefono, nombre, 100))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error creando usuario: {e}")
            return False
    
    def obtener_usuario(self, telefono):
        """Obtener datos de usuario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE telefono = ?', (telefono,))
            usuario = cursor.fetchone()
            conn.close()
            return dict(usuario) if usuario else None
        except Exception as e:
            logger.error(f"Error obteniendo usuario: {e}")
            return None
    
    def actualizar_monedas(self, telefono, cantidad):
        """Actualizar monedas de usuario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE usuarios SET monedas = monedas + ? WHERE telefono = ?',
                          (cantidad, telefono))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error actualizando monedas: {e}")
            return False
    
    def actualizar_banco(self, telefono, cantidad):
        """Actualizar banco de usuario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE usuarios SET banco = banco + ? WHERE telefono = ?',
                          (cantidad, telefono))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error actualizando banco: {e}")
            return False
    
    def actualizar_ultimo_trabajo(self, telefono):
        """Actualizar timestamp de último trabajo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE usuarios SET ultimo_trabajo = ? WHERE telefono = ?',
                          (datetime.now().isoformat(), telefono))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error actualizando trabajo: {e}")
            return False
    
    def actualizar_ultimo_robo(self, telefono):
        """Actualizar timestamp de último robo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE usuarios SET ultimo_robo = ? WHERE telefono = ?',
                          (datetime.now().isoformat(), telefono))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error actualizando robo: {e}")
            return False
    
    def agregar_exp(self, telefono, cantidad):
        """Agregar experiencia"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE usuarios SET 
                    exp = exp + ?,
                    nivel = CASE WHEN exp + ? >= 100 THEN nivel + 1 ELSE nivel END,
                    exp = CASE WHEN exp + ? >= 100 THEN 0 ELSE exp + ? END
                WHERE telefono = ?
            ''', (cantidad, cantidad, cantidad, cantidad, telefono))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error agregando exp: {e}")
            return False
    
    def obtener_ranking(self, limite=10):
        """Obtener ranking de usuarios"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT nombre, monedas, nivel FROM usuarios 
                WHERE baneado = 0 ORDER BY monedas DESC LIMIT ?
            ''', (limite,))
            usuarios = cursor.fetchall()
            conn.close()
            return [dict(u) for u in usuarios]
        except Exception as e:
            logger.error(f"Error obteniendo ranking: {e}")
            return []
    
    def registrar_actividad(self, telefono, nombre, mensaje):
        """Registrar actividad"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO actividad (telefono, nombre, mensaje) VALUES (?, ?, ?)',
                          (telefono, nombre, mensaje))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error registrando actividad: {e}")
            return False
    
    def contar_usuarios(self):
        """Contar usuarios registrados"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM usuarios')
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return 0
    
    def contar_comandos(self):
        """Contar comandos ejecutados"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM actividad')
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return 0