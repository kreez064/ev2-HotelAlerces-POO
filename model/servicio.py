class Servicio:
    def __init__(self, id_servicio, nombre, precio_usd):
        self._id_servicio = id_servicio
        self._nombre = nombre
        self._precio_usd = precio_usd

    @property
    def id_servicio(self):
        return self._id_servicio

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_usd(self):
        return self._precio_usd

    def __str__(self):
        return f"Servicio #{self._id_servicio}: {self._nombre} (${self._precio_usd} USD)"
