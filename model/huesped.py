# Clase Huesped
# model/huesped.py
from .persona import Persona

class Huesped(Persona):
    def __init__(self, rut, nombre, telefono, correo, documento):
        super().__init__(rut, nombre, telefono, correo)
        # Al asignar aquí, se invoca automáticamente el setter que valida el dato
        self.documento = documento 

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        # Validación: El documento (RUT o Pasaporte) no puede estar vacío y debe tener un mínimo de caracteres
        if not valor or len(str(valor).strip()) < 8:
            raise ValueError("Error de validación: El documento o RUT debe tener al menos 8 caracteres válidos.")
        self._documento = valor

    def historial_reservas(self):
        return f"Consultando historial de reservas para el huésped {self.nombre}."