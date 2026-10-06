# Clase Persona
# model/persona.py

class Persona:
    def __init__(self, rut, nombre, telefono, correo):
        self._rut = rut
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo

    @property
    def rut(self):
        return self._rut

    @property
    def nombre(self):
        return self._nombre

    def __str__(self):
        return f"{self._nombre} (RUT: {self._rut})"