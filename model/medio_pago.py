class MedioPago:
    def __init__(self, id_medio, nombre):
        self._id_medio = id_medio
        self._nombre = nombre

    @property
    def id_medio(self):
        return self._id_medio

    @property
    def nombre(self):
        return self._nombre

    def __str__(self):
        return f"{self._nombre}"
