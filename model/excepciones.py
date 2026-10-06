# Excepciones personalizadas
# model/excepciones.py

class HotelError(Exception):
    """Clase base para las excepciones del dominio del hotel."""
    pass

class HabitacionOcupadaError(HotelError):
    """Excepción lanzada cuando se intenta reservar una habitación sin disponibilidad."""
    pass

class AnticipoInsuficienteError(HotelError):
    """Excepción lanzada cuando se intenta hacer check-in sin el 50% de anticipo."""
    pass