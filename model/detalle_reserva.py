class DetalleReserva:
    def __init__(self, habitacion, noches, tarifa_noche):
        self._habitacion = habitacion
        self._noches = noches
        self._tarifa_noche = tarifa_noche

    @property
    def habitacion(self):
        return self._habitacion

    @property
    def noches(self):
        return self._noches

    @property
    def tarifa_noche(self):
        return self._tarifa_noche

    @property
    def subtotal(self):
        return self._noches * self._tarifa_noche

    def __str__(self):
        return f"Habitación {self._habitacion.numero} | {self._noches} noches @ ${self._tarifa_noche} USD/noche = ${self.subtotal} USD"
