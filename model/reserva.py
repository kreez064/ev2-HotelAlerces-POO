from .excepciones import HabitacionOcupadaError, AnticipoInsuficienteError
from .detalle_reserva import DetalleReserva
from .consumo import Consumo
from .pago import Pago

class Reserva:
    def __init__(self, id_reserva, huesped):
        self._id_reserva = id_reserva
        self._huesped = huesped
        self._detalles = [] 
        self._consumos = [] 
        self._pagos = []
        self._estado = "PENDIENTE"

    @property
    def id_reserva(self):
        return self._id_reserva

    @property
    def huesped(self):
        return self._huesped

    @property
    def estado(self):
        return self._estado

    @property
    def detalles(self):
        return self._detalles

    @property
    def consumos(self):
        return self._consumos

    def agregar_detalle(self, habitacion, noches, tarifa_noche):
        if not habitacion.disponible:
            raise HabitacionOcupadaError(f"Operación bloqueada: La Habitación {habitacion.numero} ya se encuentra reservada/ocupada.")
        
        detalle = DetalleReserva(habitacion, noches, tarifa_noche)
        self._detalles.append(detalle)
        habitacion.disponible = False
        return detalle

    def agregar_consumo(self, servicio, cantidad):
        consumo = Consumo(servicio, cantidad)
        self._consumos.append(consumo)
        return consumo

    def registrar_pago(self, monto_usd, medio_pago):
        pago = Pago(monto_usd, medio_pago)
        self._pagos.append(pago)
        return pago

    def calcular_total_alojamiento(self):
        return sum(d.subtotal for d in self._detalles)

    def calcular_total_consumos(self):
        return sum(c.total_usd for c in self._consumos)

    def calcular_total_general(self):
        return self.calcular_total_alojamiento() + self.calcular_total_consumos()

    def total_pagado(self):
        return sum(p.monto for p in self._pagos)

    def realizar_check_in(self):
        total_alojamiento = self.calcular_total_alojamiento()
        anticipo_minimo = total_alojamiento * 0.5
        
        if self.total_pagado() < anticipo_minimo:
            raise AnticipoInsuficienteError(
                f"Check-in bloqueado: Se requiere un anticipo mínimo del 50% (${anticipo_minimo} USD). "
                f"Monto actual pagado: ${self.total_pagado()} USD."
            )
        self._estado = "CHECKED_IN"
        return True
