"""
Capa de Acceso a Datos (DAO) para la entidad Reserva y sus líneas de DetalleReserva.
Garantiza atomicidad transaccional mediante commit y rollback explícito,
utilizando exclusivamente consultas parametrizadas con placeholders '?' para máxima seguridad.
"""
from typing import Any, Dict, List, Optional
from model.reserva import Reserva
from .conexion import ConexionBD


class ReservaDAO:
    """
    DAO para gestionar la persistencia atómica de Reservas y sus Detalles en SQLite.
    """
    def __init__(self, conexion_bd: Optional[ConexionBD] = None, db_path: Optional[str] = None):
        self._conexion_bd = conexion_bd or ConexionBD(db_path)

    def _get_connection(self):
        return self._conexion_bd.obtener_conexion()

    def guardar_reserva(self, reserva: Reserva) -> bool:
        """
        Guarda la Reserva y sus líneas de DetalleReserva en una única transacción atómica.
        
        Si cualquier inserción falla, se ejecuta conn.rollback() dejando la base de datos
        en un estado íntegro y consistente. Si todo es exitoso, se ejecuta conn.commit().
        
        Todas las sentencias utilizan placeholders (?) sin concatenación de cadenas.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            # 1. Inserción o actualización de la cabecera de la Reserva
            sql_reserva = """
                INSERT INTO reservas (id_reserva, rut_huesped, estado, total_alojamiento)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id_reserva) DO UPDATE SET
                    rut_huesped = excluded.rut_huesped,
                    estado = excluded.estado,
                    total_alojamiento = excluded.total_alojamiento
            """
            cursor.execute(sql_reserva, (
                reserva.id_reserva,
                reserva.huesped.rut,
                reserva.estado,
                reserva.calcular_total_alojamiento()
            ))

            # 2. Eliminación de detalles previos para permitir reescritura consistente si ya existía
            sql_delete_detalles = "DELETE FROM detalles_reserva WHERE id_reserva = ?"
            cursor.execute(sql_delete_detalles, (reserva.id_reserva,))

            # 3. Inserción de cada una de las líneas de DetalleReserva
            sql_detalle = """
                INSERT INTO detalles_reserva (id_reserva, numero_habitacion, noches, tarifa_noche, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """
            for detalle in reserva.detalles:
                cursor.execute(sql_detalle, (
                    reserva.id_reserva,
                    detalle.habitacion.numero,
                    detalle.noches,
                    detalle.tarifa_noche,
                    detalle.subtotal
                ))

            # 4. Commit atómico: Se confirman todas las operaciones en conjunto
            conn.commit()
            return True

        except Exception as e:
            # Rollback: Revierte cualquier cambio en caso de excepción técnica
            conn.rollback()
            raise e
        finally:
            conn.close()

    def obtener_por_id(self, id_reserva: int) -> Optional[Dict[str, Any]]:
        """
        Recupera una reserva y sus detalles asociados mediante consulta parametrizada.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            sql_reserva = "SELECT id_reserva, rut_huesped, estado, total_alojamiento FROM reservas WHERE id_reserva = ?"
            cursor.execute(sql_reserva, (id_reserva,))
            reserva_row = cursor.fetchone()
            if not reserva_row:
                return None

            sql_detalles = """
                SELECT id_detalle, id_reserva, numero_habitacion, noches, tarifa_noche, subtotal
                FROM detalles_reserva
                WHERE id_reserva = ?
                ORDER BY id_detalle ASC
            """
            cursor.execute(sql_detalles, (id_reserva,))
            detalles_rows = cursor.fetchall()

            return {
                "id_reserva": reserva_row["id_reserva"],
                "rut_huesped": reserva_row["rut_huesped"],
                "estado": reserva_row["estado"],
                "total_alojamiento": reserva_row["total_alojamiento"],
                "detalles": [dict(d) for d in detalles_rows]
            }
        finally:
            conn.close()

    def obtener_todas(self) -> List[Dict[str, Any]]:
        """
        Retorna la lista de todas las reservas registradas en la base de datos.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_reserva, rut_huesped, estado, total_alojamiento FROM reservas ORDER BY id_reserva ASC")
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def eliminar(self, id_reserva: int) -> bool:
        """
        Elimina una reserva y sus detalles en cascada dentro de una transacción.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM detalles_reserva WHERE id_reserva = ?", (id_reserva,))
            cursor.execute("DELETE FROM reservas WHERE id_reserva = ?", (id_reserva,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
