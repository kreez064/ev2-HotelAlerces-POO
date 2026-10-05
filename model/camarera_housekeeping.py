from .empleado import Empleado

class CamareraHousekeeping(Empleado):
    def __init__(self, rut, nombre, telefono, correo, usuario):
        super().__init__(rut, nombre, telefono, correo, "Camarera Housekeeping", usuario)

    def cambiar_estado_limpieza(self, habitacion, estado):
        habitacion.estado_limpieza = estado
        return f"La camarera {self.nombre} ha marcado la Habitación {habitacion.numero} como '{estado}'."
