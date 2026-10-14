"""
Capa de Acceso a Datos (DAO) para la entidad Huesped.
Implementa operaciones CRUD completas utilizando exclusivamente consultas parametrizadas (?)
para prevenir vulnerabilidades de Inyección SQL (SQL Injection).
"""
from typing import List, Optional
from model.huesped import Huesped
from .conexion import ConexionBD


class HuespedDAO:
    """
    DAO para gestionar el ciclo de vida de los registros de huéspedes en SQLite.
    """
    def __init__(self, conexion_bd: Optional[ConexionBD] = None, db_path: Optional[str] = None):
        self._conexion_bd = conexion_bd or ConexionBD(db_path)

    def _get_connection(self):
        return self._conexion_bd.obtener_conexion()

    def crear(self, huesped: Huesped) -> bool:
        """
        C (Create): Inserta un nuevo huésped en la base de datos.
        Utiliza parámetros seguros con placeholders '?' (sin interpolación de strings).
        """
        sql = """
            INSERT INTO huespedes (rut, nombre, telefono, correo, documento)
            VALUES (?, ?, ?, ?, ?)
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                huesped.rut,
                huesped.nombre,
                huesped.telefono,
                huesped.correo,
                huesped.documento
            ))
            conn.commit()
            return True
        finally:
            conn.close()

    def obtener_por_rut(self, rut: str) -> Optional[Huesped]:
        """
        R (Read by ID): Obtiene un huésped por su RUT (identificador único primario).
        Utiliza parámetros seguros con placeholders '?'.
        """
        sql = "SELECT rut, nombre, telefono, correo, documento FROM huespedes WHERE rut = ?"
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (rut,))
            row = cursor.fetchone()
            if row:
                return Huesped(
                    rut=row["rut"],
                    nombre=row["nombre"],
                    telefono=row["telefono"],
                    correo=row["correo"],
                    documento=row["documento"]
                )
            return None
        finally:
            conn.close()

    def obtener_por_id(self, id_huesped: str) -> Optional[Huesped]:
        """Alias para cumplir con la especificación de búsqueda por ID."""
        return self.obtener_por_rut(id_huesped)

    def obtener_todos(self) -> List[Huesped]:
        """
        R (Read All): Obtiene todos los huéspedes almacenados en la base de datos.
        """
        sql = "SELECT rut, nombre, telefono, correo, documento FROM huespedes ORDER BY nombre ASC"
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                Huesped(
                    rut=r["rut"],
                    nombre=r["nombre"],
                    telefono=r["telefono"],
                    correo=r["correo"],
                    documento=r["documento"]
                )
                for r in rows
            ]
        finally:
            conn.close()

    def actualizar(self, huesped: Huesped) -> bool:
        """
        U (Update): Actualiza los datos de un huésped existente identificado por su RUT.
        Utiliza parámetros seguros con placeholders '?'.
        """
        sql = """
            UPDATE huespedes
            SET nombre = ?, telefono = ?, correo = ?, documento = ?
            WHERE rut = ?
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                huesped.nombre,
                huesped.telefono,
                huesped.correo,
                huesped.documento,
                huesped.rut
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def eliminar(self, rut: str) -> bool:
        """
        D (Delete): Elimina un registro de huésped identificado por su RUT.
        Utiliza parámetros seguros con placeholders '?'.
        """
        sql = "DELETE FROM huespedes WHERE rut = ?"
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (rut,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
