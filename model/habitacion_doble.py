# Clase HabitacionDoble
from .habitacion import Habitacion

class HabitacionDoble(Habitacion):
    def __init__(self, numero, piso, precio_base):
        super().__init__(numero, piso, precio_base)
        self._capacidad_maxima = 2

    def obtener_capacidad(self):
        return f"Capacidad: {self._capacidad_maxima} personas - Cama matrimonial o dos camas individuales."