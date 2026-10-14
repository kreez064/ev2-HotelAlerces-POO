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
        """
        Valida que el documento (RUT o Pasaporte) tenga formato válido, no esté vacío
        y contenga al menos 8 caracteres. Lanza ValueError con un mensaje descriptivo si no es válido.
        """
        if valor is None:
            raise ValueError("Error de validación: El documento (RUT o Pasaporte) no puede ser nulo.")

        valor_limpio = str(valor).strip()
        if not valor_limpio:
            raise ValueError("Error de validación: El documento (RUT o Pasaporte) no puede estar vacío.")

        if len(valor_limpio) < 8:
            raise ValueError(
                f"Error de validación: El documento o RUT '{valor_limpio}' debe tener al menos 8 caracteres válidos."
            )

        self._documento = valor_limpio

    def historial_reservas(self):
        return f"Consultando historial de reservas para el huésped {self.nombre}."