# Clase Habitacion
# model/habitacion.py

class Habitacion:
    def __init__(self, numero, piso, precio_base):
        self._numero = numero
        self._piso = piso
        self._precio_base = precio_base
        self._estado_limpieza = "Limpia"
        self._disponible = True

    @property
    def numero(self):
        return self._numero

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = valor
        
    @property
    def precio_base(self):
        return self._precio_base

    def obtener_capacidad(self):
        """Método que será sobrescrito (polimorfismo) por los subtipos."""
        pass