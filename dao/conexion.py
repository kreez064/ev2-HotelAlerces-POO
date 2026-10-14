"""
Módulo de conexión y gestión de la base de datos SQLite local.
Garantiza el soporte de claves foráneas y la creación de tablas iniciales.
"""
import os
import sqlite3
from typing import Optional

# Ruta absoluta al archivo hotel.db en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH_POR_DEFECTO = os.path.join(BASE_DIR, "hotel.db")


class ConexionBD:
    """
    Administrador centralizado de la conexión a la base de datos SQLite local (hotel.db).
    """
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DB_PATH_POR_DEFECTO

    def obtener_conexion(self) -> sqlite3.Connection:
        """
        Retorna un objeto de conexión SQLite configurado con soporte para
        claves foráneas activadas y row_factory para acceso por nombre de columna.
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    def inicializar_bd(self) -> None:
        """
        Crea las tablas necesarias en la base de datos si no existen:
        - huespedes
        - reservas
        - detalles_reserva
        """
        conn = self.obtener_conexion()
        try:
            cursor = conn.cursor()
            
            # 1. Tabla de Huéspedes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS huespedes (
                    rut TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    telefono TEXT,
                    correo TEXT,
                    documento TEXT NOT NULL
                );
            """)

            # 2. Tabla de Reservas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservas (
                    id_reserva INTEGER PRIMARY KEY,
                    rut_huesped TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    total_alojamiento REAL DEFAULT 0.0,
                    FOREIGN KEY (rut_huesped) REFERENCES huespedes (rut) ON DELETE CASCADE
                );
            """)

            # 3. Tabla de Detalles de Reserva
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detalles_reserva (
                    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_reserva INTEGER NOT NULL,
                    numero_habitacion INTEGER NOT NULL,
                    noches INTEGER NOT NULL,
                    tarifa_noche REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (id_reserva) REFERENCES reservas (id_reserva) ON DELETE CASCADE
                );
            """)

            conn.commit()
        finally:
            conn.close()


def obtener_conexion(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Función de conveniencia para obtener conexión rápida."""
    return ConexionBD(db_path).obtener_conexion()


def inicializar_bd(db_path: Optional[str] = None) -> None:
    """Función de conveniencia para inicializar la base de datos."""
    ConexionBD(db_path).inicializar_bd()
