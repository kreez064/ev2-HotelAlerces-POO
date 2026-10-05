class MedioPago:
    def __init__(self, id_medio, nombre):
        self._id_medio = id_medio
        self._nombre = nombre

    @property
    def nombre(self):
        return self._nombre
