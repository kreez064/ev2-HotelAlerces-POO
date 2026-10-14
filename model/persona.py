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

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = valor

    def __str__(self):
        return f"{self._nombre} (RUT: {self._rut})"