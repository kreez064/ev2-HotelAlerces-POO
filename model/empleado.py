from .persona import Persona

class Empleado(Persona):
    def __init__(self, rut, nombre, telefono, correo, cargo, usuario):
        super().__init__(rut, nombre, telefono, correo)
        self._cargo = cargo
        self._usuario = usuario

    @property
    def cargo(self):
        return self._cargo

    @property
    def usuario(self):
        return self._usuario
