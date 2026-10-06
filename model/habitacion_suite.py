# Clase HabitacionSuite
from .habitacion import Habitacion

class HabitacionSuite(Habitacion):
    def __init__(self, numero, piso, precio_base):
        super().__init__(numero, piso, precio_base)
        self._capacidad_maxima = 4

    def obtener_capacidad(self):
        return f"Capacidad: {self._capacidad_maxima} personas - Incluye sala de estar, jacuzzi y servicios premium."