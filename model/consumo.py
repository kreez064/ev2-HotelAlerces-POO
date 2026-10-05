class Consumo:
    def __init__(self, servicio, cantidad):
        self._servicio = servicio
        self._cantidad = cantidad

    @property
    def servicio(self):
        return self._servicio

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def total_usd(self):
        return self._servicio.precio_usd * self._cantidad

    def __str__(self):
        return f"{self._servicio.nombre} (x{self._cantidad}) = ${self.total_usd} USD"
