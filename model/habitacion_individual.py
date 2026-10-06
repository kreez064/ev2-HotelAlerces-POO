# Clase HabitacionIndividual
from .habitacion import Habitacion

class HabitacionIndividual(Habitacion):
    def __init__(self, numero, piso, precio_base):
        super().__init__(numero, piso, precio_base)
        self._capacidad_maxima = 1

    def obtener_capacidad(self):
        return f"Capacidad: {self._capacidad_maxima} persona - Ideal para viajeros de negocios."